# python-ransomware-foreducationalpurposeonly
Python ransomware for educational purpose only.

***How it works***

1. Run RSA_private_public_keys.py to get the asymmetric keys for encryption and decryption
2. Replace with the new public key in the run_ransomware.py (Line 72). This is the file that will encrypt the victim's PC
3. Run run_ransomware.py on the victim's PC (Please don't run it on your personal PC, run it on a virtual machine)
4. The Program will create a key on the victim's PC, he will need to send it back to the attacker.
5. The attacker can decrypt the key with the private key file by running the Decrypt_fernet_key.py file (You need to have the key in the same directory)
6. Replace run_decrypt_system_with_key.py (Line 77) with the new decrypted key.
7. The attacker sends the run_decrypt_system_with_key.py file to the victim (with the decrypted key in the code)_
8. Victim runs run_decrypt_system_with_key.py to decrypt his PC.

*** PARAMETERS ***
You can edit run_decrypt_system_with_key.py (LINE 53) to change the path of the directories/files you want to encrypt. 
You can also change the type of files you want to encrypt (LINE 11).




This is an improved version of a project made by someone else.

Here is the github of the original project: https://github.com/ncorbuk/Python-Ransomware




Disclaimer:
This tool is only for testing and academic purposes and can only be used where strict consent has been given. Do not use it for illegal purposes! It is the end user’s responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this tool and software in general.
