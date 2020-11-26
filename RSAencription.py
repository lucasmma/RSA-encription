#!usr/bin
import HandlePrimes as primes
import gmpy2


def getPairPrimes():
    """
        function that generate a pair of large primes
    """
    p = primes.generate_prime_number(length=1024)
    q = primes.generate_prime_number(length=1024)

    return p,q

def rsaEncryption(): 

    p, q = getPairPrimes()

    n = multiplyLargeNumber(p, q) #multiplicar os numeros primos

    totiente = multiplyLargeNumber(p-1, q-1)

    e = getFirstCoPrime(totiente)

    d = modinv(e, n)

    print("Primeiro Primo p:\t", p)
    print("Segundo Primo q:\t", q)
    print("Valor de n:\t", n)
    print("Valor do totiente:\t", totiente)
    print("Valor da chave e:\t", e)
    print("Valor da chave d:\t", d)
    print("Valor igual: d=gmpy", gmpy2.invert(e, n) == d)



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
    for i in range(2, totiente + 1):
        mdc = gcd(i, totiente)
        # print("Number: ", i , "\tMDC:  ", mdc)
        if mdc == 1:
            print("First CoPrime: ", i, "\tTotiente:   ", totiente)
            return i


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    """
        Calculate the modular inverse
    """
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


rsaEncryption()