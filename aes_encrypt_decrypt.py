# Encryption & Decryption Functions
from aes_core import *
from key_expansion import *
from sbox_and_rcon import *


def AES128(state, cypherkey):
    roundKey = keyExpansion128(
        cypherkey, sbox=sbox, rcon=rcon)

    result = list.copy(state)

    for i in range(0, 4):
        for j in range(0, 4):
            result[i][j] = state[i][j] ^ roundKey[0][i][j]

    for q in range(1, 10):
        result = subBytes(result, sbox)
        result = shiftRows(result)
        result = gMixColumns(result)
        for i in range(0, 4):
            for j in range(0, 4):
                result[i][j] = result[i][j] ^ roundKey[q][i][j]

    result = subBytes(result, sbox)
    result = shiftRows(result)
    for i in range(0, 4):
        for j in range(0, 4):
            result[i][j] = result[i][j] ^ roundKey[10][i][j]

    return result


def AES192(state, cypherkey):
    roundKey = keyExpansion192(
        cypherkey, sbox=sbox, rcon=rcon)

    print(roundKey)
    result = list.copy(state)

    for i in range(0, 4):
        for j in range(0, 4):
            result[i][j] = state[i][j] ^ roundKey[0][i][j]

    for q in range(1, 12):
        result = subBytes(result, sbox)
        result = shiftRows(result)
        result = gMixColumns(result)
        for i in range(0, 4):
            for j in range(0, 4):
                result[i][j] = result[i][j] ^ roundKey[q][i][j]

    result = subBytes(result, sbox)
    result = shiftRows(result)
    for i in range(0, 4):
        for j in range(0, 4):
            result[i][j] = result[i][j] ^ roundKey[12][i][j]

    return result


def AES256(state, cypherkey):
    roundKey = keyExpansion256(
        cypherkey, sbox=sbox, rcon=rcon)

    result = list.copy(state)

    for i in range(0, 4):
        for j in range(0, 4):
            result[i][j] = state[i][j] ^ roundKey[0][i][j]

    for q in range(1, 14):
        result = subBytes(result, sbox)
        result = shiftRows(result)
        result = gMixColumns(result)
        for i in range(0, 4):
            for j in range(0, 4):
                result[i][j] = result[i][j] ^ roundKey[q][i][j]

    result = subBytes(result, sbox)
    result = shiftRows(result)
    for i in range(0, 4):
        for j in range(0, 4):
            result[i][j] = result[i][j] ^ roundKey[14][i][j]

    return result


def AES128_decrypt(state, cypherkey):

    roundKey = keyExpansion128(cypherkey, sbox, rcon)

    result = list.copy(state)

    for i in range(0, 4):
        for j in range(0, 4):
            result[i][j] = state[i][j] ^ roundKey[10][i][j]

    for q in range(9, 0, -1):
        result = invShiftRows(result)
        result = invSubBytes(result, rbox)
        for i in range(0, 4):
            for j in range(0, 4):
                result[i][j] = result[i][j] ^ roundKey[q][i][j]
        result = gInvMixColumns(result)

    result = invShiftRows(result)
    result = invSubBytes(result, rbox)
    for i in range(0, 4):
        for j in range(0, 4):
            result[i][j] = result[i][j] ^ roundKey[0][i][j]

    return result


def AES192_decrypt(state, cypherkey):

    roundKey = keyExpansion192(cypherkey, sbox, rcon)

    result = list.copy(state)

    for i in range(0, 4):
        for j in range(0, 4):
            result[i][j] = state[i][j] ^ roundKey[12][i][j]

    for q in range(11, 0, -1):
        result = invShiftRows(result)
        result = invSubBytes(result, rbox)
        for i in range(0, 4):
            for j in range(0, 4):
                result[i][j] = result[i][j] ^ roundKey[q][i][j]
        result = gInvMixColumns(result)

    result = invShiftRows(result)
    result = invSubBytes(result, rbox)
    for i in range(0, 4):
        for j in range(0, 4):
            result[i][j] = result[i][j] ^ roundKey[0][i][j]

    return result


def AES256_decrypt(state, cypherkey):

    roundKey = keyExpansion256(cypherkey, sbox, rcon)

    result = list.copy(state)

    for i in range(0, 4):
        for j in range(0, 4):
            result[i][j] = state[i][j] ^ roundKey[14][i][j]

    for q in range(13, 0, -1):
        result = invShiftRows(result)
        result = invSubBytes(result, rbox)
        for i in range(0, 4):
            for j in range(0, 4):
                result[i][j] = result[i][j] ^ roundKey[q][i][j]
        result = gInvMixColumns(result)

    result = invShiftRows(result)
    result = invSubBytes(result, rbox)
    for i in range(0, 4):
        for j in range(0, 4):
            result[i][j] = result[i][j] ^ roundKey[0][i][j]

    return result
