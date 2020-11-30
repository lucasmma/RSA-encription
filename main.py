#!usr/bin
#coding: utf8
import RSAencryption as RSAenc
import base64
import SHA3

def getFileMSG():
    filename = str(input("Digite o path para o arquivo: "))
    return openFile(filename)

def openFile(filename):
    try:
        with open(filename, 'rb') as f:
            content = f.read()
            contentbit = RSAenc.bytes_to_bits(content)
            return SHA3.fromBits(contentbit)
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
    
    print("Mensagem cifrada : \t", RSAenc.int_to_bytes(hashcifrado).hex())

    documentoassinado = str(hash.hex()) + str(RSAenc.int_to_bytes(hashcifrado).hex()) + msg

    createFile(documentoassinado)

    hashparsedhex = documentoassinado[:64]
    hashcifradohex = documentoassinado[64:576]
    mensagem = documentoassinado[576:]

    hashdecifradohex = RSAenc.decrypt(RSAenc.int_from_bytes(SHA3.getBytesFromBitArray(SHA3.hexStringToBitArray(hashcifradohex))) , d, n).hex()

    if hashparsedhex == hashdecifradohex:
        print("Hash é valido")

if __name__ == '__main__':
    main()