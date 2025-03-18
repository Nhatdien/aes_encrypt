# AES Core Functions

import numpy as np

from galois_multiplication import *
from sbox_and_rcon import *


def addRoundKey(state, key):
    return [[state[i][j] ^ key[i][j] for j in range(4)] for i in range(4)]


def subBytes(state, sbox):
    return [[sbox[byte] for byte in row] for row in state]


def gMixColumn(r):

    a = [0, 0, 0, 0]  # [0 for i in range(4)]
    b = [0, 0, 0, 0]  # [0 for i in range(4)]
    r1 = [0, 0, 0, 0]

    for c in range(0, 4):
        a[c] = r[c]
        h = (r[c] >> 7) & 1
        b[c] = r[c] << 1
        b[c] ^= h * 0x1B

    r1[0] = (b[0] ^ a[3] ^ a[2] ^ b[1] ^ a[1]) % 256
    r1[1] = (b[1] ^ a[0] ^ a[3] ^ b[2] ^ a[2]) % 256
    r1[2] = (b[2] ^ a[1] ^ a[0] ^ b[3] ^ a[3]) % 256
    r1[3] = (b[3] ^ a[2] ^ a[1] ^ b[0] ^ a[0]) % 256

    return r1


def gMixColumns(d):
    r = list.copy(d)
    r = np.transpose(r)
    r = r.tolist()
    r1 = []

    for i in range(0, 4):
        r[i] = gMixColumn(r[i])
        r1.append(r[i])

    r1 = np.transpose(r1)
    r1 = r1.tolist()
    return r1


def shiftRows(state):
    state[1] = state[1][1:] + state[1][:1]
    state[2] = state[2][2:] + state[2][:2]
    state[3] = state[3][3:] + state[3][:3]
    return state


def invSubBytes(state, rbox):
    return [[rbox[byte] for byte in row] for row in state]


def gInvMixColumn(r):

    a = mul9(r)
    b = mul11(r)
    c = mul13(r)
    d = mul14(r)

    ret = [0, 0, 0, 0]

    ret[0] = (d[0] ^ b[1] ^ c[2] ^ a[3]) % 256
    ret[1] = (a[0] ^ d[1] ^ b[2] ^ c[3]) % 256
    ret[2] = (c[0] ^ a[1] ^ d[2] ^ b[3]) % 256
    ret[3] = (b[0] ^ c[1] ^ a[2] ^ d[3]) % 256

    return ret


def gInvMixColumns(d):

    r = list.copy(d)
    r = np.transpose(r)
    r = r.tolist()
    r1 = []

    for i in range(0, 4):
        r[i] = gInvMixColumn(r[i])
        r1.append(r[i])

    r1 = np.transpose(r1)
    r1 = r1.tolist()
    return r1


def invShiftRows(state):
    state[1] = state[1][-1:] + state[1][:-1]
    state[2] = state[2][-2:] + state[2][:-2]
    state[3] = state[3][-3:] + state[3][:-3]
    return state
