# AES Encryption and Decryption

## Introduction
This project implements AES (Advanced Encryption Standard) encryption and decryption using Python. It provides a GUI for users to encrypt and decrypt messages using 128-bit, 192-bit, or 256-bit keys. The project includes core AES functions, key expansion algorithms, and a graphical user interface (GUI) built with Tkinter.

## Overview of AES Encryption
AES is a symmetric-key encryption standard that operates on fixed-size blocks of 16 bytes (128 bits). It is widely used in securing sensitive data. The encryption process involves multiple rounds of transformations that include substitution, permutation, mixing, and key addition.

### AES Encryption Steps:
1. **Key Expansion:** The original cipher key is expanded into multiple round keys using a key schedule algorithm.
2. **Initial Round:**
   - AddRoundKey: XOR the plaintext with the first round key.
3. **Main Rounds (Repeated 9, 11, or 13 times for 128, 192, or 256-bit keys, respectively):**
   - SubBytes: Substitute each byte using a substitution box (S-Box).
   - ShiftRows: Rotate the rows of the state matrix.
   - MixColumns: Apply linear transformation on columns for diffusion.
   - AddRoundKey: XOR with the round key.
4. **Final Round:**
   - SubBytes, ShiftRows, AddRoundKey (without MixColumns).

### AES Decryption Steps:
The decryption process reverses encryption by applying inverse transformations:
1. AddRoundKey
2. Inverse ShiftRows
3. Inverse SubBytes
4. AddRoundKey
5. Inverse MixColumns (except for the final round)
6. Repeat until original plaintext is restored.

## Project Structure
```
├── main.py                  # Main file with GUI implementation
├── aes_encrypt_decrypt.py   # AES encryption & decryption logic
├── key_expansion.py         # Key expansion functions
├── galois_multiplication.py # Galois Field operations
├── sbox_and_rcon.py         # S-Box and Rcon values
├── utils.py                 # Helper functions for matrix transformations
```

## Explanation of Core Functions

### 1. **AddRoundKey**
```python
 def addRoundKey(state, key):
    return [[state[i][j] ^ key[i][j] for j in range(4)] for i in range(4)]
```
- This function performs an XOR operation between the state matrix and the round key.
- XOR is used because it provides a simple but effective way to combine key material with data.

### 2. **SubBytes**
```python
def subBytes(state, sbox):
    return [[sbox[byte] for byte in row] for row in state]
```
- Each byte in the state matrix is replaced using the S-Box, which provides non-linearity.
- The S-Box is precomputed and derived from the multiplicative inverse in GF(2^8).

### 3. **ShiftRows**
```python
def shiftRows(state):
    state[1] = state[1][1:] + state[1][:1]
    state[2] = state[2][2:] + state[2][:2]
    state[3] = state[3][3:] + state[3][:3]
    return state
```
- Rows are cyclically shifted to the left.
- This increases diffusion by spreading bytes across multiple columns.

### 4. **MixColumns**
```python
def gMixColumn(r):
    a = [0, 0, 0, 0]
    b = [0, 0, 0, 0]
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
```
- Uses matrix multiplication in GF(2^8) to transform the columns.
- Provides diffusion, ensuring that changing one byte affects the entire ciphertext.

### 5. **Key Expansion**
```python
def keyExpansion128(key, sbox, rcon):
    retkey = [list.copy(key)]
    for i in range(10):
        newkey = []
        interkey = np.transpose(retkey[-1]).tolist()
        rconarr = [rcon[i], 0, 0, 0]
        workingarr = rotWord(list.copy(interkey[-1]))
        for q in range(4):
            workingarr[q] = sbox[workingarr[q]]
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
```
- Expands a 128-bit key into 11 round keys (10 rounds + initial key).
- Uses the Rcon array for round constants to prevent symmetry attacks.
- The `rotWord` function cyclically rotates bytes before S-Box substitution.

## How to Use

### Prerequisites
- Python 3.x
- Required dependencies: `numpy`, `tkinter`

### Run the Program
```sh
python main.py
```

### Features
- **Encryption**: Enter plaintext and key, then click "Encrypt" to get the encrypted text.
- **Decryption**: Enter encrypted text and key, then click "Decrypt" to retrieve the original message.
- **Time Calculation**: Displays encryption and decryption time.
- **User-Friendly Interface**: Uses Tkinter for an interactive UI.

## Future Enhancements
- Implement AES-GCM mode for authenticated encryption.
- Add support for file encryption and decryption.
- Improve performance by optimizing matrix operations.

## Author
Nhat Tran

## License
MIT License

