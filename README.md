# Image Steganography Application

This Image Steganography application allows users to hide and retrieve text and audio data within image files using encryption techniques. The graphical user interface (GUI) is built using Tkinter, while image processing is handled with OpenCV.

## Prerequisites

Make sure you have the following installed:
- Python 3.x
- Required libraries:
  ```bash
  pip install opencv-python tkinter
  ```

## How to Use

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Belard4l/Image-steganography.git
   ```

2. **Run the Application**

   ```bash
   python code.py
   ```

3. **Using the GUI**

   - **Select Image**: Click on the "Browse" button next to "Image Path" to select the image file to use for steganography.
   - **Enter Key**: Provide a key for encryption and decryption in the "Key" field.
   - **Text Operations**:
     - **Encrypt Text in Image**: Enter the text to hide in the image in the "Text" field and click the "Encrypt Text in Image" button.
     - **Decrypt Text from Image**: Click the "Decrypt Text from Image" button to retrieve hidden text from the image. The text will appear in the "Text" field.
   - **Audio Operations**:
     - **Select Audio**: Click on the "Browse" button next to "Audio Path" to select the audio file to hide in the image.
     - **Encrypt Audio in Image**: Click the "Encrypt Audio in Image" button to hide the selected audio in the image.
     - **Decrypt Audio from Image**: Click the "Decrypt Audio from Image" button to retrieve hidden audio from the image. You will be prompted to save the extracted audio file.

## Expected Results

- **Encrypt Text in Image**: The text will be encrypted and hidden in the selected image, and the encrypted image will be saved with a unique filename.
- **Decrypt Text from Image**: The hidden text will be decrypted and displayed in the "Text" field.
- **Encrypt Audio in Image**: The audio file will be encrypted and hidden in the selected image, and the encrypted image will be saved with a unique filename.
- **Decrypt Audio from Image**: The hidden audio will be decrypted and saved as an audio file at the specified location.

## Demo files
The image and audio can be used for demonstration of the image steganography

## Note

Ensure the key used for encryption and decryption is the same to successfully retrieve the hidden data.

---

This README provides a quick guide on how to use the image steganography application and what to expect from it. Happy coding!
