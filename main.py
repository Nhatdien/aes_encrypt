# main.py
import numpy as np
from galois_multiplication import *
from key_expansion import keyExpansion128
from aes_encrypt_decrypt import *
from utils import stringToMat, matToString, xorMatrix
from sbox_and_rcon import *


def encrypt(state=None, key=None):
    ret = ""
    while (state == None):
        print("Please insert your plaintext?")
        state = input()

    while (key == None or not (len(key) == 16 or len(key) == 32 or len(key) == 24)):
        print("Please insert your cipher key? Your key must be of length 16, 24 or 32")
        key = input()

    lenkey = len(key)

    func = {
        16: AES128,
        24: AES192,
        32: AES256
    }

    res = [state[y - 16:y] for y in range(16, len(state) + 16, 16)]

    lim = 16 - len(res[-1])

    for i in range(0, lim):
        res[-1] += chr(0x00)

    key = stringToMat(key)
    if (lenkey != 16):
        cypherkey = np.transpose(key)
        cypherkey = cypherkey.tolist()
    else:
        cypherkey = key

    print(f"Using AES{lenkey*8} to encrypt")
    for i in res:
        sub = stringToMat(i)
        sub = func[lenkey](sub, cypherkey)
        sub = matToString(sub)
        ret += sub

    return ret


def decrypt(state=None, key=None):

    ret = ""

    while (state == None):
        print("Please insert your plaintext?")
        state = input()

    while (key == None or not (len(key) == 16 or len(key) == 32 or len(key) ==
                               24)):
        print("Please insert your cipher key? Your key must be of length 16, 24 or 32")
        key = input()

    lenkey = len(key)

    func = {
        16: AES128_decrypt,
        24: AES192_decrypt,
        32: AES256_decrypt
    }

    res = [state[y - 16:y] for y in range(16, len(state) + 16, 16)]

    lim = 16 - len(res[-1])

    for i in range(0, lim):
        res[-1] += chr(0x00)

    key = stringToMat(key)
    if (lenkey != 16):
        cypherkey = np.transpose(key)
        cypherkey = cypherkey.tolist()
    else:
        cypherkey = key

    for i in res:
        sub = stringToMat(i)
        sub = func[lenkey](sub, cypherkey)
        sub = matToString(sub)
        ret += sub

    return ret


def main():
    plain_text = input("Input you plain text: ")
    key = input(
        "Please insert your cipher key? Your key must be of length 16, 24 or 32: ")
    encrypted_state = encrypt(plain_text, key)

    decrypt_state = decrypt(encrypted_state, key=key)

    print(
        f"Your plain text: {plain_text} ecrypted to {encrypted_state} and will be decrypted back to {decrypt_state} with key: {key}")


if __name__ == "__main__":
    main()
