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
    encrypted_state = encrypt()
    print(encrypted_state)

    decrypt_state = decrypt(encrypted_state)
    print(decrypt_state)
    # # Example plaintext and key (16 bytes for AES-128)
    # plaintext = input("Input plaintext: ")
    # while len(plaintext) < 16:
    #     print("text length should be multiply of 16, current length: ", len(plaintext))
    #     plaintext = input("Input plaintext again: ")

    # key = "SecretAESKey1234"

    # # Convert plaintext and key to matrix form
    # state = stringToMat(plaintext)
    # cypherkey = stringToMat(key)

    # # Expand the key

    # # Encrypt the plaintext
    # encrypted_state = AES128(state, cypherkey)
    # encrypted_text = matToString(encrypted_state)

    # print("Encrypted Text:", ''.join(
    #     f'{byte:02x}' for byte in np.ravel(encrypted_state)))

    # # Decrypt the ciphertext
    # decrypted_state = AES128_decrypt(encrypted_state, cypherkey)
    # decrypted_text = matToString(decrypted_state)

    # print("Decrypted Text:", decrypted_text)


if __name__ == "__main__":
    main()
