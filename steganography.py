import cv2
import os

def encode_message(img, msg):
    """
    Function to encode a secret message in the image pixels.
    """
    # Prepare the message to be encoded (we'll use the ASCII values of characters)
    msg_len = len(msg)
    if msg_len > img.size:
        print("Message is too long to encode in this image!")
        return img # Return the unmodified image

    msg_bin = ''.join(format(ord(i), '08b') for i in msg) # Convert each character to binary

    data_index = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3): # For RGB channels
                if data_index < len(msg_bin):
                    img[i, j, k] = (img[i, j, k] & ~1) | int(msg_bin[data_index]) # Modify the LSB
                    data_index += 1
                if data_index >= len(msg_bin):
                    return img # Message fully encoded

    return img

def decode_message(img):
    """
    Function to decode the secret message from the image pixels.
    """
    msg_bin = ""
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3): # For RGB channels
                msg_bin += str(img[i, j, k] & 1) # Get the LSB
    # Now split the binary string into 8-bit chunks and convert to characters
    message = ""
    for i in range(0, len(msg_bin), 8):
        byte = msg_bin[i:i + 8]
        if len(byte) == 8:
            message += chr(int(byte, 2)) # Convert binary to char

    return message

# Main program
img = cv2.imread("photo.jpg") # Replace with the correct image path
if img is None:
    print("Error: Image not found.")
    exit()

msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# Encrypt the message into the image
encrypted_img = encode_message(img.copy(), msg)

cv2.imwrite("encryptedImage.jpg", encrypted_img)
os.system("start encryptedImage.jpg") # Use 'start' to open the image on Windows

# Ask for the passcode and decrypt the message if the passcode matches
pas = input("Enter passcode for Decryption: ")
if password == pas:
    decrypted_msg = decode_message(encrypted_img)
    print("Decrypted message:", decrypted_msg)
else:
    print("YOU ARE NOT AUTHORIZED.")
