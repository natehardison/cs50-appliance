#!/usr/bin/python

from Crypto.Cipher import AES
from Crypto.Hash import MD5
import getpass
import pexpect
import string

# Pull passphrases out of encrypted file
# Expect file encrypted with: `openssl aes-256-cbc -salt`
passphrase_file = open(".passphrases", "rU")
ciphertext = passphrase_file.read()

# First 8 bytes should be "SALTED__", so we can throw away
salt = ciphertext[8:16]
data = ciphertext[16:]
secret = getpass.getpass("Password: ")

# AES-256's KDF:
key = MD5.new(secret + salt).digest()
key += MD5.new(key + secret + salt).digest()
iv = MD5.new(key[16:] + secret + salt).digest()

plaintext = AES.new(key, AES.MODE_CBC, iv).decrypt(data)

# Each line of plaintext should be in private_key: passphrase format
for line in plaintext.split('\n'):
    # openssl uses \x02 to pad, so get rid of it
    line = line.strip('\x02')

    # Need to split on ": " in case passphrase has ':'s in it
    private_key, passphrase = map(string.strip, line.split(": "))
    
    # Use pexpect since pipes won't work
    ssh_agent = pexpect.spawn("ssh-add %s" % private_key)
    ssh_agent.expect_exact("Enter passphrase for %s: " % private_key)
    ssh_agent.sendline(passphrase)
    ssh_agent.expect(pexpect.EOF)
