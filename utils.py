# Utility Functions
import numpy as np

def stringToMat(s):
    ret = []
    interkey = []
    for i in range(len(s)):
        interkey.append(ord(s[i]))
        if i % 4 == 3:
            ret.append(interkey)
            interkey = []
    return np.transpose(ret).tolist()

def matToString(s):
    s = np.transpose(s)
    s = np.ravel(s)
    return ''.join(chr(i) for i in s)

def xorMatrix(a, b):
    return [[a[i][j] ^ b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
