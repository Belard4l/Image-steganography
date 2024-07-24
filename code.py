import cv2
import os
import uuid
from tkinter import Tk, Label, Button, Entry, Text, filedialog, messagebox

# Initialize dictionaries for character-to-ASCII and ASCII-to-character mapping
d = {}
c = {}
for i in range(255):
    d[chr(i)] = i
    c[i] = chr(i)

# Function to convert audio to binary
def audio_to_binary(audio_path):
    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()
    binary_data = ''.join(format(byte, '08b') for byte in audio_data)
    delimiter = '11111111' * 10  # A long sequence to mark the end
    binary_data += delimiter
    return binary_data

# Function to encrypt binary data using XOR with a key
def encrypt_binary_data(binary_data, key):
    key_binary = ''.join(format(ord(char), '08b') for char in key)
    encrypted_data = ""
    key_index = 0
    for bit in binary_data:
        encrypted_bit = int(bit) ^ int(key_binary[key_index % len(key_binary)])
        encrypted_data += str(encrypted_bit)
        key_index += 1
    return encrypted_data

# Function to embed binary data into an image
def hide_binary_in_image(image_path, binary_data):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Could not open or find the image.")
    
    data_len = len(binary_data)
    max_capacity = img.shape[0] * img.shape[1] * 3

    if data_len > max_capacity:
        raise ValueError("The selected image is not large enough to hold the data.")
    
    for i in range(data_len):
        pixel_index = i // 3
        row = pixel_index // img.shape[1]
        col = pixel_index % img.shape[1]
        channel = i % 3
        img[row, col, channel] = img[row, col, channel] & 254 | int(binary_data[i])

    encrypted_image_path = f"encrypted_img_{uuid.uuid4().hex}.png"
    cv2.imwrite(encrypted_image_path, img)
    return encrypted_image_path

# Function to extract binary data from an image
def extract_binary_from_image(image_path, key):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Could not open or find the image.")
    
    binary_data = ""
    key_binary = ''.join(format(ord(char), '08b') for char in key)
    key_index = 0
    delimiter = '11111111' * 10
    
    for i in range(img.shape[0] * img.shape[1] * 3):
        pixel_index = i // 3
        row = pixel_index // img.shape[1]
        col = pixel_index % img.shape[1]
        channel = i % 3
        binary_data += str(img[row, col, channel] & 1)
    
    decrypted_data = ""
    for i in range(len(binary_data)):
        decrypted_bit = int(binary_data[i]) ^ int(key_binary[key_index % len(key_binary)])
        decrypted_data += str(decrypted_bit)
        key_index += 1
    
    end_index = decrypted_data.find(delimiter)
    if end_index != -1:
        decrypted_data = decrypted_data[:end_index]
    else:
        raise ValueError("Delimiter not found. Data extraction might be corrupted.")
    
    return decrypted_data

# Function to convert binary data back to audio
def binary_to_audio(binary_data, output_path):
    audio_data = bytearray(int(binary_data[i:i + 8], 2) for i in range(0, len(binary_data), 8))
    with open(output_path, "wb") as audio_file:
        audio_file.write(audio_data)

# Function to hide audio in image
def hide_audio_in_image(image_path, key, audio_path):
    binary_data = audio_to_binary(audio_path)
    encrypted_data = encrypt_binary_data(binary_data, key)
    encrypted_image_path = hide_binary_in_image(image_path, encrypted_data)
    messagebox.showinfo("Success", f"Data hiding done. Encrypted image saved as {encrypted_image_path}")

# Function to extract audio from image
def extract_audio_from_image(image_path, key, output_path):
    binary_data = extract_binary_from_image(image_path, key)
    binary_to_audio(binary_data, output_path)
    messagebox.showinfo("Success", f"Data extraction done. Audio saved as {output_path}")

# Function to hide text in image
def hide_text_in_image(image_path, key, text):
    text += "\0"  # Append a null character as the delimiter
    x = cv2.imread(image_path)
    if x is None:
        messagebox.showerror("Error", "Could not open or find the image.")
        return
    
    i = x.shape[0]
    j = x.shape[1]
    
    kl = 0
    z = 0
    n = 0
    m = 0
    l = len(text)

    for i in range(l):
        x[n, m, z] = d[text[i]] ^ d[key[kl]]
        n += 1
        m = (m + 1) % 3
        kl = (kl + 1) % len(key)

    # Save the encrypted image with a unique filename
    encrypted_image_path = f"encrypted_img_{uuid.uuid4().hex}.png"
    cv2.imwrite(encrypted_image_path, x)
    messagebox.showinfo("Success", f"Data hiding done. Encrypted image saved as {encrypted_image_path}")

# Function to extract text from the encrypted image
def extract_text_from_image(key, image_path):
    x = cv2.imread(image_path)
    if x is None:
        messagebox.showerror("Error", "Could not open or find the image.")
        return

    kl = 0
    z = 0
    n = 0
    m = 0
    decrypt = ""

    try:
        while True:
            char = c[x[n, m, z] ^ d[key[kl]]]
            if char == "\0":  # Stop if the delimiter is found
                break
            decrypt += char
            n += 1
            m = (m + 1) % 3
            kl = (kl + 1) % len(key)
    except KeyError:
        return None
    
    return decrypt

# GUI setup
def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
    if file_path:
        image_path_entry.delete(0, 'end')
        image_path_entry.insert(0, file_path)

def select_audio():
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.mp3")])
    if file_path:
        audio_path_entry.delete(0, 'end')
        audio_path_entry.insert(0, file_path)

def encrypt_image_text():
    image_path = image_path_entry.get()
    key = key_entry.get()
    text = text_entry.get("1.0", 'end-1c')
    if not image_path or not key or not text:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    hide_text_in_image(image_path, key, text)

def decrypt_image_text():
    image_path = image_path_entry.get()
    key = key_entry.get()
    if not image_path or not key:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    try:
        decrypted_text = extract_text_from_image(key, image_path)
    except IndexError:
        messagebox.showerror("Error", "Wrong Key, Please try again")
    else:
        if decrypted_text is None:
            messagebox.showerror("Error", "Wrong Key, Please try again")
        else:
            text_entry.delete("1.0", 'end')
            text_entry.insert("1.0", decrypted_text)

def encrypt_image_audio():
    image_path = image_path_entry.get()
    key = key_entry.get()
    audio_path = audio_path_entry.get()
    if not image_path or not key or not audio_path:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    hide_audio_in_image(image_path, key, audio_path)

def decrypt_image_audio():
    image_path = image_path_entry.get()
    key = key_entry.get()
    output_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("Audio files", "*.wav")])
    if not image_path or not key or not output_path:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    try:
        extract_audio_from_image(image_path, key, output_path)
    except (IndexError, ValueError):
        messagebox.showerror("Error", "Data extraction failed. Possibly wrong key or corrupted image.")

# Main application window
root = Tk()
root.title("Steganography")

Label(root, text="Image Path:").grid(row=0, column=0, padx=10, pady=10)
image_path_entry = Entry(root, width=50)
image_path_entry.grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Browse", command=select_image).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="Key:").grid(row=1, column=0, padx=10, pady=10)
key_entry = Entry(root, width=50)
key_entry.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Text:").grid(row=2, column=0, padx=10, pady=10)
text_entry = Text(root, width=50, height=10)
text_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

Label(root, text="Audio Path:").grid(row=3, column=0, padx=10, pady=10)
audio_path_entry = Entry(root, width=50)
audio_path_entry.grid(row=3, column=1, padx=10, pady=10)
Button(root, text="Browse", command=select_audio).grid(row=3, column=2, padx=10, pady=10)

Button(root, text="Encrypt Text in Image", command=encrypt_image_text).grid(row=4, column=1, padx=10, pady=10)
Button(root, text="Decrypt Text from Image", command=decrypt_image_text).grid(row=4, column=2, padx=10, pady=10)

Button(root, text="Encrypt Audio in Image", command=encrypt_image_audio).grid(row=5, column=1, padx=10, pady=10)
Button(root, text="Decrypt Audio from Image", command=decrypt_image_audio).grid(row=5, column=2, padx=10, pady=10)

root.mainloop()
 # type: ignore