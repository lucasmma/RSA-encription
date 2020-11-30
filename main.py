#!usr/bin
#coding: utf8
import RSAencryption as RSAenc
import base64
import SHA3
from Utils import bits_from_bytes, string_from_bits, bytes_from_int, bytes_from_bits, bits_from_hexadecimal

def getFileMSG():
    filename = str(input("Digite o path para o arquivo: "))
    return openFile(filename)

def openFile(filename):
    try:
        with open(filename, 'rb') as f:
            content = f.read()
            contentbit = bits_from_bytes(content)
            return string_from_bits(contentbit)
    except FileNotFoundError:
        print("Arquivo não encontrado, digite outro path.")
        return getFileMSG()
        

def createFile(assinatura):
    f = open("signed.txt", "w")
    f.write(assinatura)
    print("Cheque o arquivo signed.txt para visualizar o documento assinado.")

def main():

    msg = getFileMSG()

    e, d, n = RSAenc.generateKeys()

    print("ENC: \t", e)
    print("DEC: \t", d)
    print("N: \t", n)
    
    hash = SHA3.sha3(msg, 1088,256)

    print("SHA3: \t", hash.hex())

    hashcifrado = RSAenc.encrypt(hash, e, n)
    
    print("Mensagem cifrada : \t", bytes_from_int(hashcifrado).hex())

    documentoassinado = str(hash.hex()) + str(bytes_from_int(hashcifrado).hex()) + msg

    createFile(documentoassinado)

    hashparsedhex = documentoassinado[:64]
    hashcifradohex = documentoassinado[64:576]
    mensagem = documentoassinado[576:]

    hashdecifradohex = RSAenc.decrypt(RSAenc.int_from_bytes(bytes_from_bits(bits_from_hexadecimal(hashcifradohex))) , d, n).hex()

    if hashparsedhex == hashdecifradohex:
        print("Hash é valido")

if __name__ == '__main__':
    main()