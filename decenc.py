#!/usr/bin/env python

import sys
import Crypto.Cipher
import hashlib
from importlib import import_module

#Jacob Holcomb, Security Analyst @ Independent Security Evaluators
#Twitter: @rootHak42
#Github: https://github.com/Gimppy042
#2015
#decenc is a tool for performing cryptographic routines (i.e., encrypt and decrypt (Hashing also supported)
#python dependency pycrypto is required.

#
#Software License
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by 
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#  
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.       
#                                                       
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/> 
#



def new_crypto_obj(alg, mode, key, iv, operation):
	if operation == "-d" or operation == "-e":
		enc_mode = "MODE_" + mode.upper()
		mode = getattr(alg, enc_mode)
		dec_key_iv = alg.new(key.decode("hex"), mode, iv.decode("hex"))
	elif operation == "-h":
		dec_key_iv = alg.new()
	return dec_key_iv

def encrypt(crypto_obj, plain_text, padding):
	cipher_text = crypto_obj.encrypt((plain_text + padding))
	return cipher_text
	
def decrypt(crypto_obj, cipher_text):
	plain_text = crypto_obj.decrypt(cipher_text.decode("hex"))
	return plain_text

def hashing(crypto_obj, plain_text):
	crypto_obj.update(plain_text)
	return crypto_obj.hexdigest()

def algorithm(selected_alg, operation):
	alg = selected_alg.lower()

	if operation == "-d" or operation == "-e":
		if alg == "blowfish":
			return "Blowfish"
		elif alg == "aes":
			return "AES"
		elif alg == "des":
			return "DES"
		elif alg == "3des":
			return "DES3"
		else:
			supported_ciphers()
			sys.exit(1)

	elif operation == "-h":
		if alg == "md2":
			return "MD2"
		elif alg == "md4":
			return "MD4"
		elif alg == "md5":
			return "MD5"
		elif alg == "sha":
			return "SHA"
		elif alg == "sha256":
			return "SHA256"
		elif alg == "sha512":
			return "SHA512"
		else:
			supported_ciphers()
			sys.exit(1)

def supported_ciphers():
	ciphers = "\n\n[*] Supported Crypto Ciphers [*]\n\n"
	ciphers += "\t- AES\n"
	ciphers += "\t- Blowfish\n"
	ciphers += "\t- DES\n"
	ciphers += "\t- 3DES\n\n"
	ciphers += "\n[*] Supported Hashing Algorithms [*]\n\n"
	ciphers += "\t- SHA (SHA-1)\n"
	ciphers += "\t- SHA224 (SHA-2)\n"
	ciphers += "\t- SHA256 (SHA-2)\n"
	ciphers += "\t- SHA384 (SHA-2)\n"
	ciphers += "\t- SHA512 (SHA-2)\n\n"
	print ciphers
	
def usage(program):
	instructions = "\n\n[*] Program Usage: {0} <-e|-d|-h> <plain|cipher text> <key> <iv> <algorithm> <mode> [*]\n\n".format(program)
	instructions += "- Decrypt Example: {0} -d <ciphertext> 04B915BA43FEB5B6 c645ad903fe4b247 blowfish cbc\n".format(program)
	instructions += "- Encrypt Example: {0} -e <plaintext> 04B915BA43FEB5B6 c645ad903fe4b247 blowfish cbc\n".format(program)
	instructions += "- Hashing Example: {0} -h <plaintext> md5\n\n".format(program)
	print instructions
	sys.exit(1)


def main():

	if len(sys.argv) < 3:
		usage(sys.argv[0])

	try:
		operation = sys.argv[1]
		crypto_text = sys.argv[2]
	except Exception as error:
		print "\n [!!!] ERROR! {0} {1} [!!!]\n".format(type(error), error)
		sys.exit(1)

	if operation != "-e" and operation != "-d" and operation != "-h":
		usage(sys.argv[0])


	if operation == "-e" or operation == "-d":
		try:
			enc_key = sys.argv[3]
			enc_iv =  sys.argv[4]
			enc_mode = sys.argv[6]
		except Exception as error:
			print "\n [!!!] ERROR! {0} {1} [!!!]\n".format(type(error), error)
			sys.exit(1)
	elif operation == "-h":
		enc_key = None
		enc_iv = None
		enc_mode = None


	if operation == "-e":
		#Encrypt
		try:
			enc_alg = import_module("Crypto.Cipher." + algorithm(sys.argv[5], operation))
			crypto = new_crypto_obj(enc_alg, enc_mode, enc_key, enc_iv, operation)
			padding = "\x00" * (8 - (len(crypto_text) % 8))
			cipher_text = encrypt(crypto, crypto_text, padding)
			print "\nEncryption Algorithm: {0}\n\nEncryption IV: {1}\nEncrypted Plaintext: {2}\n\nIV + Ciphertext: {3}\n\n".\
			format(enc_alg.__name__, enc_iv, cipher_text.encode("hex"), enc_iv + cipher_text.encode("hex"))
		except Exception as error:
			print "\n [!!!] ERROR! {0} {1} [!!!]\n".format(type(error), error)
			sys.exit(1)
	elif operation == "-d":
		#Decrypt
		try:
			enc_alg = import_module("Crypto.Cipher." + algorithm(sys.argv[5], operation))
			crypto = new_crypto_obj(enc_alg, enc_mode, enc_key, enc_iv, operation)
			text = decrypt(crypto, crypto_text)
			print "\nEncryption Algorithm: {0}\nDecrypted Ciphertext: {1}\n\n".format(enc_alg.__name__, text)
		except Exception as error:
			print "\n [!!!] ERROR! {0} {1} [!!!]\n".format(type(error), error)
			sys.exit(1)
	elif operation == "-h":
		#Hashing
		try:
			enc_alg = import_module("Crypto.Hash." + algorithm(sys.argv[3], operation))
			crypto = new_crypto_obj(enc_alg, enc_mode, enc_key, enc_iv, operation)
			text = hashing(crypto, crypto_text)
			print "\nHashing Algorithm: {0}\nHashed Text: {1}\n\n".format(enc_alg.__name__, text)
		except Exception as error:
			print "\n [!!!] ERROR! {0} {1} [!!!]\n".format(type(error), error)
			sys.exit(1)
	else:
		usage(sys.argv[0])

if __name__ == "__main__":
	main()

