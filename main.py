import numpy as np
import tkinter as tk
from tkinter import messagebox
from galois_multiplication import *
from key_expansion import keyExpansion128
from aes_encrypt_decrypt import *
from utils import stringToMat, matToString, xorMatrix
from sbox_and_rcon import *


def encrypt(state, key):
    if not (len(key) == 16 or len(key) == 32 or len(key) == 24):
        messagebox.showerror(
            "Error", "Cipher key must be of length 16, 24, or 32")
        return ""

    lenkey = len(key)
    func = {16: AES128, 24: AES192, 32: AES256}
    res = [state[y - 16:y] for y in range(16, len(state) + 16, 16)]
    lim = 16 - len(res[-1])
    res[-1] += chr(0x00) * lim

    key = stringToMat(key)
    cypherkey = np.transpose(key).tolist() if lenkey != 16 else key

    encrypted_text = "".join(matToString(
        func[lenkey](stringToMat(i), cypherkey)) for i in res)
    return encrypted_text


def decrypt(state, key):
    if not (len(key) == 16 or len(key) == 32 or len(key) == 24):
        messagebox.showerror(
            "Error", "Cipher key must be of length 16, 24, or 32")
        return ""

    lenkey = len(key)
    func = {16: AES128_decrypt, 24: AES192_decrypt, 32: AES256_decrypt}
    res = [state[y - 16:y] for y in range(16, len(state) + 16, 16)]
    lim = 16 - len(res[-1])
    res[-1] += chr(0x00) * lim

    key = stringToMat(key)
    cypherkey = np.transpose(key).tolist() if lenkey != 16 else key

    decrypted_text = "".join(matToString(
        func[lenkey](stringToMat(i), cypherkey)) for i in res)
    return decrypted_text


def on_encrypt():
    plain_text = entry_plain.get()
    key = entry_key.get()
    encrypted_text = encrypt(plain_text, key)
    entry_encrypted.delete(0, tk.END)
    entry_encrypted.insert(0, encrypted_text)


def on_decrypt():
    encrypted_text = entry_encrypted.get()
    key = entry_key.get()
    decrypted_text = decrypt(encrypted_text, key)
    entry_decrypted.delete(0, tk.END)
    entry_decrypted.insert(0, decrypted_text)


# UI Setup
root = tk.Tk()
root.title("AES Encryption & Decryption")
root.geometry("500x300")

tk.Label(root, text="Plain Text:").grid(row=0, column=0, padx=10, pady=5)
entry_plain = tk.Entry(root, width=50)
entry_plain.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Cipher Key:").grid(row=1, column=0, padx=10, pady=5)
entry_key = tk.Entry(root, width=50, show="*")
entry_key.grid(row=1, column=1, padx=10, pady=5)

tk.Button(root, text="Encrypt", command=on_encrypt).grid(
    row=2, column=0, columnspan=2, pady=10)

tk.Label(root, text="Encrypted Text:").grid(row=3, column=0, padx=10, pady=5)
entry_encrypted = tk.Entry(root, width=50)
entry_encrypted.grid(row=3, column=1, padx=10, pady=5)

tk.Button(root, text="Decrypt", command=on_decrypt).grid(
    row=4, column=0, columnspan=2, pady=10)

tk.Label(root, text="Decrypted Text:").grid(row=5, column=0, padx=10, pady=5)
entry_decrypted = tk.Entry(root, width=50)
entry_decrypted.grid(row=5, column=1, padx=10, pady=5)

root.mainloop()
