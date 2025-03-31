# Key Expansion Functions
import numpy as np


def rotWord(r):
    r[0], r[1], r[2], r[3] = r[1], r[2], r[3], r[0]
    return r


def keyExpansion128(key, sbox, rcon):
    retkey = [list.copy(key)]
    for i in range(10):
        newkey = []
        interkey = np.transpose(retkey[-1]).tolist()
        rconarr = [rcon[i], 0, 0, 0]

        # rotWord Function rotate word for 1 byte to left
        workingarr = rotWord(list.copy(interkey[-1]))

        # Subword using sbox array
        for q in range(4):
            workingarr[q] = sbox[workingarr[q]]

        # XOR with rcon to caculate 'G" funcion and xor with inter
        for j in range(len(workingarr)):
            workingarr[j] = workingarr[j] ^ interkey[0][j] ^ rconarr[j]

        newkey.append(list.copy(workingarr))
        for k in range(1, 4):
            for j in range(4):
                workingarr[j] = workingarr[j] ^ interkey[k][j]
            newkey.append(list.copy(workingarr))
        newkey = np.transpose(newkey).tolist()
        retkey.append(newkey)
    return retkey


def keyExpansion192(key, sbox, rcon):
    retkey = []

    # key: 6 x 4 array

    for i in key:
        retkey.append(list.copy(i))

    for i in range(0, 8):
        rconarr = [rcon[i], 0, 0, 0]
        index = len(retkey) - 6
        k6n_6 = list.copy(retkey[index])
        workingarr = list.copy(retkey[-1])
        workingarr = rotWord(workingarr)
        for q in range(0, 4):
            workingarr[q] = sbox[workingarr[q]]

        for j in range(0, len(workingarr)):
            workingarr[j] = workingarr[j] ^ k6n_6[j] ^ rconarr[j]
            
        retkey.append(list.copy(workingarr))
        index += 1
        for k in range(0, 5):
            for j in range(0, 4):
                workingarr[j] = workingarr[j] ^ retkey[index][j]
            retkey.append(list.copy(workingarr))
            index += 1

    expandedKey = []

    for i in range(0, 13):
        interkey = []
        for j in range(0, 4):
            interkey.append(list.copy(retkey.pop(0)))
        interkey = np.transpose(interkey)
        interkey = interkey.tolist()
        expandedKey.append(interkey)

    return expandedKey


def keyExpansion256(key, sbox, rcon):
    retkey = []

    # key: 8 x 4 array

    for i in key:
        retkey.append(list.copy(i))

    for i in range(0, 7):
        rconarr = [rcon[i], 0, 0, 0]
        index = len(retkey) - 8
        k8n_8 = list.copy(retkey[index])
        workingarr = list.copy(retkey[-1])
        workingarr = rotWord(workingarr)
        for q in range(0, 4):
            workingarr[q] = sbox[workingarr[q]]
        for j in range(0, len(workingarr)):
            workingarr[j] = workingarr[j] ^ k8n_8[j] ^ rconarr[j]
        retkey.append(list.copy(workingarr))
        index += 1
        for k in range(0, 3):
            for j in range(0, 4):
                workingarr[j] = workingarr[j] ^ retkey[index][j]
            retkey.append(list.copy(workingarr))
            index += 1

        for q in range(0, 4):
            workingarr[q] = sbox[workingarr[q]]

        for j in range(0, 4):
            workingarr[j] = workingarr[j] ^ retkey[index][j]
        retkey.append(list.copy(workingarr))
        index += 1

        for k in range(0, 3):
            for j in range(0, 4):

                workingarr[j] = workingarr[j] ^ retkey[index][j]
            retkey.append(list.copy(workingarr))
            index += 1

    expandedKey = []

    for i in range(0, 15):
        interkey = []
        for j in range(0, 4):
            interkey.append(list.copy(retkey.pop(0)))
        interkey = np.transpose(interkey)
        interkey = interkey.tolist()
        expandedKey.append(interkey)

    return expandedKey
