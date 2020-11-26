#!usr/bin
import HandlePrimes as primes
import base64
import sympy 


def getPairPrimes():
    """
        function that generate a pair of large primes
    """
    p = primes.generate_prime_number(length=1024)
    q = primes.generate_prime_number(length=1024)

    return p,q

def generateKeys(): 

    p, q = getPairPrimes()

    n = multiplyLargeNumber(p, q) #multiplicar os numeros primos

    totiente = multiplyLargeNumber(p-1, q-1)

    e = getFirstCoPrime(totiente)

    d = sympy.mod_inverse(e, totiente)

    # print("Primeiro Primo p:\t", p)
    # print("Segundo Primo q:\t", q)
    # print("Valor de n:\t", n)
    # print("Valor do totiente:\t", totiente)
    # print("Valor da chave e:\t", e)
    # print("Valor da chave d:\t", d)

    return e,d,n

def multiplyLargeNumber(n1, n2):
    return n1*n2

def gcd(a,b):
    """
        Find greater common divisor
    """
    while b !=0:
        resto = a % b
        a = b
        b = resto

    return a

def getFirstCoPrime(totiente):
    for i in range(2**1024, totiente + 1):
        mdc = gcd(i, totiente)
        # print("Number: ", i , "\tMDC:  ", mdc)
        if mdc == 1:
            # print("First CoPrime: ", i, "\tTotiente:   ", totiente)
            return i

def encrypt(msg, e, n):
    """
        Encrypt function
    """

    b = int.from_bytes(msg.encode(), "big")

    msgcifrada = pow(b, e, n)

    return msgcifrada

def decrypt(msg, d, n):
    """
        Decrypt function
    """

    msgdecifrada = int_to_bytes(pow(msg, d, n)).decode("utf-8")

    return msgdecifrada

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')