"""
Based on http://downloads.joelinoff.com/mycrypt.py
"""

import os
import base64

from hashlib import sha512
from Crypto.Cipher import AES
from cryptography.hazmat.backends.openssl.backend import Backend
from cryptography.hazmat.primitives import hashes


class AESCipher(object):
    """
    Implement openssl compatible AES-256 CBC mode encryption/decryption.
     
    This module provides encrypt() and decrypt() functions that are compatible
    with the OpenSSL algorithms.
    """

    def EVP_ByteToKey(self, password, salt, key_len = 32, iv_len = 16):
        """
        Derive the key and the IV from the given password and salt.
        See http://stackoverflow.com/questions/13907841/implement-openssl-aes-encryption-in-python

        :param password: The password to use as the seed
        :param salt:     The salt
        :param key_len:  The key length
        :param iv_len:   The initialization vector length
        :returns:        key, iv
        """
        try:
            maxlen = key_len + iv_len
            key_iv = sha512(password + salt).digest()
            tmp    = [key_iv]
            while len(tmp) < maxlen:
                tmp.append(sha512(tmp[-1] + password + salt).digest())
                key_iv += tmp[-1]
                key = key_iv[:key_len]
                iv  = key_iv[key_len:key_len + iv_len]
            return key, iv
        except UnicodeDecodeError:
            return None, None


    def encrypt(self, password, plaintext, chunkIt=True):
        """
        The steps for encrypting are:

        1. Generate 8 bytes of random data as salt
        2. Derive AES key and IV from password using the salt from step 1
        3. Pad the input data with PKCS#7
        4. Encrypt the padded using AES-256 in CBC mode with the key and the IV from step 2
        5. Encode in Base64 and output the salt from step 1
        6. Encode in Base64 and output the encrypted data from step 4

        :param password:  The password
        :param plaintext: The plaintext to encrypt
        :param chunkIt:   Flag that tells encrypt to split the ciphertext into 64 character (MIME encoded) lines
        """
        salt    = os.urandom(8)
        key, iv = get_key_and_iv(password, salt)
        if key is None:
            return None

        # PKCS#7 padding
        padding_len      = 16 - (len(plaintext) % 16)
        padded_plaintext = plaintext + (chr(padding_len) * padding_len)

        # Encrypt
        cipher     = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(padded_plaintext)

        # Make openssl compatible
        openssl_ciphertext = 'Salted__' + salt + ciphertext
        b64                = base64.b64encode(openssl_ciphertext)
        if not chunkIt:
            return b64
        else:
            LINELEN = 64
            chunk   = lambda s: '\n'.join(s[i:min(i+LINELEN, len(s))]
                                for i in xrange(0, len(s), LINELEN))
            return chunk(b64)


    def decrypt(password, ciphertext):
        """
        The steps from decrypting are:

        1. Decode the input data from Base64 into a binary string.
        2. Treat the first 8 bytes of the decoded data as salt.
        3. Derive AES key and IV from password using the salt from step 1.
        4. Decrypt the remaining decoded data using the AES key and the IV from step 3.
        5. Verify and remove the PKCS#7 padding from the result.

        :param password:   The password
        :param ciphertext: The ciphertext to decrypt
        """
        # Base64 decode
        raw  = base64.b64decode(ciphertext)
        assert( raw[:8] == 'Salted__' )
        salt = raw[8:16]

        # Now create the key and iv.
        key, iv = get_key_and_iv(password, salt)
        if key is None:
            return None

        # The original ciphertext
        ciphertext = raw[16:]

        # Decrypt
        cipher           = AES.new(key, AES.MODE_CBC, iv)
        padded_plaintext = cipher.decrypt(ciphertext)
        padding_len      = ord(padded_plaintext[-1])
        plaintext        = padded_plaintext[:-padding_len]
        return plaintext


class DigestUtil(object):

    @classmethod
    def hash_password(_class, password, salt=None):
        if salt is None:
            salt = os.urandom(32)
        else:
            salt = base64.b64decode(salt.encode('utf-8'))
        digest = hashes.Hash(hashes.SHA512(), backend=Backend())
        digest.update(salt + password.encode('utf-8'))
        salt = base64.b64encode(salt)
        hash = base64.b64encode(digest.finalize())
        return salt.decode('utf-8'), hash.decode('utf-8')

    @classmethod
    def check(_class, password, salt, hash):
        return DigestUtil.hash_password(password, salt)[1] == hash
