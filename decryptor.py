import os
import base64
import string
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def fetch_key_from_github(raw_url: str) -> bytes:
    """Fetch the encryption key from a GitHub raw URL."""
    response = requests.get(raw_url)
    if response.status_code == 200:
        key = bytes.fromhex(response.text.strip())
        if len(key) != 32:
            raise ValueError("Invalid key length: Key must be 32 bytes for ChaCha20.")
        return key
    else:
        raise ConnectionError(f"Failed to fetch key from GitHub. Status code: {response.status_code}")
    
def get_available_drives():
    """Detect all available drives on the system."""
    drives = []
    for drive in string.ascii_uppercase:
        if os.path.exists(f"{drive}:\\"):
            drives.append(f"{drive}:\\")
    return drives


def simulate_decryption_on_drive(drive, key: bytes):
    """Simulate decryption by decoding Base64-encoded files with .rns extension."""
    for root, dirs, files in os.walk(drive):
        for file in files:
            # Process only files with the custom extension
            if not file.endswith(".rns"):
                continue

            file_path = os.path.join(root, file)
            try:
                # Read encoded file data
                with open(file_path, 'rb') as f:
                    nonce = f.read(16)  # Read the first 16 bytes as nonce
                    ciphertext = f.read()  # The rest is ciphertext

                cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
                decryptor = cipher.decryptor()
                plaintext = decryptor.update(ciphertext)    

                # Restore original file by removing .tst extension
                original_file_path = file_path[:-4]  # Remove ".rns"

                # Write decoded data to the original file
                with open(original_file_path, 'wb') as f:
                    f.write(plaintext)

                # Remove the encrypted file
                os.remove(file_path)

                print(f"Decrypted: {original_file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")



def main():
        try:
                # GitHub raw URL to the key file
            key_url = "https://raw.githubusercontent.com/repel11/ransomtest/refs/heads/main/key.txt"

            # Fetch the encryption key
            key = fetch_key_from_github(key_url)
            print(f"Fetched key: {key.hex()}")

            # Detect all drives
            drives = get_available_drives()
            print(f"Detected drives: {drives}")

            
            # Process each drive
            for drive in drives:
                print(f"Decrypting files on {drive}")
                simulate_decryption_on_drive(drive, key)

            print("Decryption simulation complete. The system should remain functional.")
        except Exception as e:
            print(f"Error while decryption: {e}")



if __name__ == "__main__":
    main()
