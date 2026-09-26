# pycrypt

A simple tool to encrypt and decrypt files before you upload to cloud storage (e.g. google drive). 
Aims to support most files by just thinking of them as bytes. 
Recovering file type may require additional consideration, but I will try. 

Initial idea of how it will work: 

pycrypt "file-name" "output file name" 
-> a file with the output file name which is encrypted 
pycrypt -decrypt "file-name" 
-> A decrypted file 
