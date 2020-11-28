#!usr/bin
#coding: utf-8

import numpy as np
import math
import RSAencryption as RSA
from bitstring import BitArray

RHO_MATRICES = {tuple(np.linalg.matrix_power(np.array([[0,1],[2,3]]), t).dot(np.array([1,0])) % 5): t for t in range(0,24)}
RHO_MATRICES[(0,0)] = -1

def xorArrays(array1,array2):
    newArray = [0 for _ in range(64)]
    for i in range(64):
        newArray[i] = (array1[i] + array2[i]) % 2
    return newArray

def andArrays(array1,array2):
    newArray = [0 for _ in range(64)]
    for i in range(64):
        if (array1[i] + array2[i]) == 2:
            newArray[i] = 1
        else:
            newArray[i] = 0
    return newArray

def negateArray(array):
    newArray = [0 for _ in range(64)]
    for i in range(64):
        if array[i] == 1:
            newArray[i] = 0
        else:
            newArray[i] = 1
    return newArray

def rotateArray(arr,n):
    newArray = arr.copy()
    for i in range(0, n):      
        first = newArray[0];    
            
        for j in range(0, len(arr)-1):      
            newArray[j] = newArray[j+1];    
                  
        newArray[len(newArray)-1] = first; 
    return newArray   


def arrTransform1(arr):
    output = [[[0 for _ in range(64)] for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            for k in range(64):
                output[i][j][k] = arr[64*(5*j + i)+k]
            
            bitarrayk = output[i][j]
            inversebyte = []
            for z in range(0, 8):
                inversebyte = inversebyte + (bitarrayk[64-((z+1)*8):64-(z*8)])

            output[i][j] = inversebyte

    return output

def arrTransform2(arr):
    output = [0]*1600
    for i in range(5):
        for j in range(5):
            bitarrayk = arr[i][j]
            inversebyte = []
            for z in range(0, 8):
                inversebyte = inversebyte + (bitarrayk[64-((z+1)*8):64-(z*8)])

            arr[i][j] = inversebyte
            
            for k in range(64):
                output[64*(5*j + i)+k] = arr[i][j][k]
            
    return output

def theta(A_in):
    A_out = [[[0 for _ in range(64)] for _ in range(5)] for _ in range(5)]
    c = [[0 for _ in range(64)] for _ in range(5)]
    d = [[0 for _ in range(64)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            c[i] = xorArrays(c[i],A_in[i][j])
    
    for i in range(5):
        d[i] = xorArrays(c[(i-1) % 5],rotateArray(c[(i + 1) % 5],1))         
        for j in range(5):
            A_out[i][j] = xorArrays(A_in[i][j],d[i])    

    return A_out

rhomatrix=[[0,36,3,41,18],[1,44,10,45,2],[62,6,43,15,61],[28,55,25,21,56],[27,20,39,8,14]]
def rho(A_in):
    A_out = [[[0 for _ in range(64)] for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            for k in range(64):
                t = RHO_MATRICES[(i,j)]
                b = A_in[i][j][k - rhomatrix[i][j]]
                A_out[i][j][k] = b

    return A_out

def pi(A_in):
    A_out = [[[0 for _ in range(64)] for _ in range(5)] for _ in range(5)]
    x = 1
    y = 0
    current = A_in[x][y]
    for t in range(24):
        X = y
        Y = (2*x + 3*y) % 5
        tmp = A_in[X][Y]
        A_in[X][Y] = rotateArray(current,int((((t+1)*(t+2))/2) % 64))
        current = tmp
        x = X
        y = Y
    return A_in

def chi(A_in):
    for y in range(5):
        c = A_in.copy()
        for x in range(5):
            c[x] = A_in[x][y]
        for x in range(5):
            A_in[x][y] = xorArrays(c[x],andArrays(negateArray(c[(x+1)%5]),c[(x+2)%5]))
    return A_in

def iota(A_in, round):
    RC = [   "0x0000000000000001","0x0000000000008082","0x800000000000808a"
            ,"0x8000000080008000","0x000000000000808b","0x0000000080000001"
            ,"0x8000000080008081","0x8000000000008009","0x000000000000008a"
            ,"0x0000000000000088","0x0000000080008009","0x000000008000000a"
            ,"0x000000008000808b","0x800000000000008b","0x8000000000008089"
            ,"0x8000000000008003","0x8000000000008002","0x8000000000000080"
            ,"0x000000000000800a","0x800000008000000a","0x8000000080008081"
            ,"0x8000000000008080","0x0000000080000001","0x8000000080008008",]
    A_out = A_in.copy()
    A_out[0][0] = xorArrays(A_out[0][0],hexStringToBitArray(RC[round]))

    return A_out

def hexStringToBitArray(word): 
    bit_string = BitArray(hex=word).bin
    return [int(char) for char in bit_string]

#  ι ◦ χ ◦ π ◦ ρ ◦ θ
def sha3(A_in):
    roundOut = arrTransform1(A_in)

    for r in range(24):

        roundOut = theta(roundOut)
        roundOut = pi(roundOut)
        roundOut = chi(roundOut)
        roundOut = iota(roundOut, r)

    ans = arrTransform2(roundOut)
    return ans


def final_sha3(A_in, blocksize):
    currentState = [0] * 1600
    # currentState = sha3(A_in[0])
    for i in A_in:
        currentState = sha3_xor(currentState, i, blocksize)
        currentState = sha3(currentState)

    return getStringFromBitArray(currentState[0:256])

def sha3_xor(aone, atwo, blocksize):
    for i in range(0, 1600):
        if aone[i] == atwo[i]:
            aone[i] = 0
        else:
            aone[i] = 1

    return aone


def organizeInputMessage(msg, blocksize):
    arrayofbits = toBits(msg)

    numberOfChunks = math.ceil(len(arrayofbits)/blocksize)

    if numberOfChunks == 0:
        numberOfChunks = 1
    
    matriz = []
    arrayCapacity = [0] * (1600-blocksize)

    for i in range(0, numberOfChunks):
        firstIndex = i * blocksize
        lastIndex = (i+1) * blocksize
        newArray = arrayofbits[firstIndex : lastIndex]
        tamanhoArray = len(newArray)

        if tamanhoArray < blocksize:
            paddingsize = blocksize - tamanhoArray
            if paddingsize == 8:
                newArray = newArray + [1, 0, 0, 0, 0, 1, 1, 0]
            elif paddingsize == 16:
                newArray = newArray + [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0]
            else:
                newArray = newArray + [0, 0, 0, 0, 0, 1, 1, 0] + ([0] * (paddingsize - 16)) + [1, 0, 0, 0, 0, 0, 0, 0]

        finalArray = newArray + arrayCapacity

        matriz.append(finalArray)
    
    return matriz


def toBits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def fromBits(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def getStringFromBitArray(bitArray):

    value = 0

    for bit in bitArray:
        value = (value << 1) | bit

    return RSA.int_to_bytes(value)

def getBytesFromBitArray(bitArray):

    value = 0

    for bit in bitArray:
        value = (value << 1) | bit

    return RSA.int_to_bytes(value)

def printMatriz3D(A_in):
    for i in range(0,5):
        print("||||")
        for x in range(0,5):
            print(getStringFromBitArray(A_in[i][x]).hex())

def printArray3D(A_in):
        print(getStringFromBitArray(A_in).hex())