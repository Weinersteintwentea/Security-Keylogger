# Security-Keylogger
This is a keylogger which would send all the details of user's system which includes system information, screenshot of current window, open ports, clipboard information, keys that user press, audio file (10 seconds you can change it according to your convenience)  

you can also change the number of time keylogger would execute simply by changing the value of "number_of_iterations_end" variable from keylogger.py file(by-default its set to 1 time) and make sure that the mail which you are using as a sender should have less secure app access enabled.



Usage:-
Step 1:-
Install all the packages which are imported in python files.

Step 2 (generates key for encryption and decryption of files):-
Run GenerateKey.py file.

Step 3:-
Run keylogger.py file.


Step 4(for decryption of files copy and paste all the encrypted file in Cryptography Folder):-
Run DecryptFile.py file.




