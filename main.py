import numpy as np
import tkinter as tk
from tkinter import messagebox
import time
from galois_multiplication import *
from key_expansion import keyExpansion128
from aes_encrypt_decrypt import *
from utils import stringToMat, matToString
from sbox_and_rcon import *


def update_key_length(*args):
    key_length = len(entry_key.get())
    label_key_length.config(text=f"Key Length: {key_length} bytes")


def encrypt(state, key):
    if len(key) not in [16, 24, 32]:
        messagebox.showerror(
            "Error", "Cipher key must be 16, 24, or 32 bytes.")
        return "", 0

    func = {16: AES128, 24: AES192, 32: AES256}
    res = [state[i:i + 16] for i in range(0, len(state), 16)]
    res[-1] += chr(0x00) * (16 - len(res[-1]))  # Padding

    key_matrix = stringToMat(key)
    cypherkey = np.transpose(key_matrix).tolist() if len(
        key) != 16 else key_matrix

    start_time = time.time()
    encrypted_text = "".join(matToString(
        func[len(key)](stringToMat(i), cypherkey)) for i in res)
    return encrypted_text, time.time() - start_time


def decrypt(state, key):
    if len(key) not in [16, 24, 32]:
        messagebox.showerror(
            "Error", "Cipher key must be 16, 24, or 32 bytes.")
        return "", 0

    func = {16: AES128_decrypt, 24: AES192_decrypt, 32: AES256_decrypt}
    res = [state[i:i + 16] for i in range(0, len(state), 16)]
    res[-1] += chr(0x00) * (16 - len(res[-1]))  # Padding

    key_matrix = stringToMat(key)
    cypherkey = np.transpose(key_matrix).tolist() if len(
        key) != 16 else key_matrix

    start_time = time.time()
    decrypted_text = "".join(matToString(
        func[len(key)](stringToMat(i), cypherkey)) for i in res)
    return decrypted_text, time.time() - start_time


def on_encrypt():
    encrypted_text, encrypt_time = encrypt(entry_plain.get(), entry_key.get())
    entry_encrypted.delete(0, tk.END)
    entry_encrypted.insert(0, encrypted_text)
    label_encrypt_time.config(text=f"Encrypt Time: {encrypt_time:.6f} sec")


def on_decrypt():
    decrypted_text, decrypt_time = decrypt(
        entry_encrypted.get(), entry_key.get())
    entry_decrypted.delete(0, tk.END)
    entry_decrypted.insert(0, decrypted_text)
    label_decrypt_time.config(text=f"Decrypt Time: {decrypt_time:.6f} sec")


# UI Setup
root = tk.Tk()
root.title("AES Encryption & Decryption")
root.geometry("900x700")  # Default size
root.configure(bg="#2c3e50")

# Centering content
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

form_frame = tk.Frame(root, bg="#2c3e50", padx=40, pady=40)
form_frame.grid(row=1, column=1)

style = {"bg": "#34495e", "fg": "white", "font": (
    "Arial", 18), "padx": 10, "pady": 10}

# UI Elements
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
entry_key.bind("<KeyRelease>", update_key_length)

label_key_length = tk.Label(form_frame, text="Key Length: 0 bytes", **style)
label_key_length.grid(row=1, column=2, padx=20, pady=10)

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
