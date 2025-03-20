import numpy as np
import tkinter as tk
from tkinter import messagebox
import time
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

    start_time = time.time()
    encrypted_text = "".join(matToString(
        func[lenkey](stringToMat(i), cypherkey)) for i in res)
    encrypt_time = time.time() - start_time

    return encrypted_text, encrypt_time


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

    start_time = time.time()
    decrypted_text = "".join(matToString(
        func[lenkey](stringToMat(i), cypherkey)) for i in res)
    decrypt_time = time.time() - start_time

    return decrypted_text, decrypt_time


def on_encrypt():
    plain_text = entry_plain.get()
    key = entry_key.get()
    encrypted_text, encrypt_time = encrypt(plain_text, key)
    entry_encrypted.delete(0, tk.END)
    entry_encrypted.insert(0, encrypted_text)
    label_encrypt_time.config(text=f"Encrypt Time: {encrypt_time:.6f} sec")


def on_decrypt():
    encrypted_text = entry_encrypted.get()
    key = entry_key.get()
    decrypted_text, decrypt_time = decrypt(encrypted_text, key)
    entry_decrypted.delete(0, tk.END)
    entry_decrypted.insert(0, decrypted_text)
    label_decrypt_time.config(text=f"Decrypt Time: {decrypt_time:.6f} sec")


# UI Setup
root = tk.Tk()
root.title("AES Encryption & Decryption")
root.geometry("900x700")  # Increased window size
root.configure(bg="#2c3e50")

# Centering the form with padding
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

form_frame = tk.Frame(root, bg="#2c3e50", padx=40, pady=40)
form_frame.grid(row=1, column=1, sticky="nsew")

style = {
    # Increased font size
    "bg": "#34495e", "fg": "white", "font": ("Arial", 18), "padx": 10, "pady": 10
}

tk.Label(form_frame, text="Plain Text:", **
         style).grid(row=0, column=0, padx=20, pady=10)
entry_plain = tk.Entry(form_frame, width=60, font=("Arial", 18))
entry_plain.grid(row=0, column=1, padx=20, pady=10)

label_encrypt_time = tk.Label(form_frame, text="Encrypt Time: 0 sec", **style)
label_encrypt_time.grid(row=0, column=2, padx=20, pady=10)

tk.Label(form_frame, text="Cipher Key:", **
         style).grid(row=1, column=0, padx=20, pady=10)
entry_key = tk.Entry(form_frame, width=60, font=("Arial", 18), show="*")
entry_key.grid(row=1, column=1, padx=20, pady=10)

tk.Button(form_frame, text="Encrypt", command=on_encrypt, bg="#1abc9c",
          fg="white", font=("Arial", 18)).grid(row=2, column=0, columnspan=2, pady=20)

tk.Label(form_frame, text="Encrypted Text:", **
         style).grid(row=3, column=0, padx=20, pady=10)
entry_encrypted = tk.Entry(form_frame, width=60, font=("Arial", 18))
entry_encrypted.grid(row=3, column=1, padx=20, pady=10)

tk.Button(form_frame, text="Decrypt", command=on_decrypt, bg="#e74c3c",
          fg="white", font=("Arial", 18)).grid(row=4, column=0, columnspan=2, pady=20)

tk.Label(form_frame, text="Decrypted Text:", **
         style).grid(row=5, column=0, padx=20, pady=10)
entry_decrypted = tk.Entry(form_frame, width=60, font=("Arial", 18))
entry_decrypted.grid(row=5, column=1, padx=20, pady=10)

label_decrypt_time = tk.Label(form_frame, text="Decrypt Time: 0 sec", **style)
label_decrypt_time.grid(row=5, column=2, padx=20, pady=10)

root.mainloop()
