#!usr/bin
#coding: utf8
import RSAencryption as RSAenc
import base64

import SHA3

def main():

    msg = str(input("Enter a message to cipher: "))

    e, d, n = RSAenc.generateKeys()

    print("ENC: \t", e)
    print("DEC: \t", d)
    print("N: \t", n)
    
    hash = SHA3.final_sha3(SHA3.organizeInputMessage(msg, 1088),1088)

    print("SHA3: \t", hash.hex())

    msgcifrada = RSAenc.encrypt(hash, e, n)
    
    print("Mensagem cifrada : \t", msgcifrada)

    documentoassinado = str(hash.hex()) + str(msgcifrada) + msg

    print(documentoassinado)

    msgdecifrada = RSAenc.decrypt(msgcifrada, d, n)

    print("Mensagem decifrada : \t", msgdecifrada.hex())

    if hash == msgdecifrada:
        print("Hash é valido")

if __name__ == '__main__':
    main()