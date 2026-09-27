from cryptography.fernet import Fernet
from pathlib import Path 
from datetime import datetime 

class PycryptCore: 
    def __init__(self): 
        path = Path("outputs")
        if not path.exists(): 
            path.mkdir() 

        path = Path("user")
        if not path.exists(): 
            path.mkdir()

    def key_generation(self): 
        key = Fernet.generate_key()
        file = open("user/key.txt", "wb")
        file.write(key)
        file.close() 

    def encrypt(self, filepath, output_name=None, stream=False, chunksize=1000000): 
        key_path = Path("user/key.txt")
        file_path = Path(filepath)
        extension = filepath.split(".")[-1]

        if not stream: 
            chunksize = None 

        if key_path.exists(): 
            if file_path.exists(): 
                keyfile = open("user/key.txt", "rb")
                datafile = open(filepath, "rb")
                key = keyfile.read()
                data = datafile.read(chunksize) 
                f = Fernet(key)
                encrypted_data = f.encrypt(data)
                if stream: 
                    while data:
                        path, encrypted_file = self.stream_write(encrypted_data, extension=f".{extension}", pathname=filepath)
                        data = datafile.read(chunksize) 
                        encrypted_data = f.encrypt(data)
                    encrypted_file.close() 
                    return path 
                else: 
                    path = self.write(encrypted_data, extension=f".{extension}", pathname = filepath)
                    return path 
            else: 
                print("No such file.")
        else: 
            self.key_generation() 

    def decrypt(self, filepath): 
        path = Path(filepath) 
        extension = filepath.split(".")[-1]

        if not path.exists(): 
            print("No such file.")
            return 

        key_path = Path("user/key.txt")

        if not key_path.exists(): 
            print("Key has not been generated, impossible to decrypt.")
            return 

        key = open("user/key.txt", "rb").read()
        encrypted_data = open(filepath, "rb").read()
        f = Fernet(key)
        data = f.decrypt(encrypted_data) 
        self.write(data, extension=f".{extension}")

    # UTILITY FUNCTIONS 
    def get_unique_path(self, name): 
        i = 0 
        path = Path(name) 
        extension = name.split(".")[-1]
        name = name.split(".")[0]


        while path.exists(): 
            name = name + f" ({i})"
            path = Path(name + "." + extension)
            i += 1 

        return name + "." + extension

    def write(self, data, pathname=None, extension=""): 
        if pathname == None:
            current_time = datetime.now().strftime("%H %M %S")
            pathname = f"result generated at {current_time}{extension}"
        else: 
            pathname = pathname.split("/")[-1]

        writeback_path = f"outputs/{pathname}"
        writeback_path = self.get_unique_path(writeback_path)
        writeback_file = open(writeback_path, "wb")
        written = writeback_file.write(data)
        print(f"Wrote {written} to {writeback_path}")
        writeback_file.close()      
        return writeback_path

    def stream_write(self, data, pathname=None, extension=""): 
        if pathname == None:
            current_time = datetime.now().strftime("%H %M %S")
            pathname = f"result generated at {current_time}{extension}"
        else: 
            pathname = pathname.split("/")[-1]

        writeback_path = f"outputs/{pathname}"
        writeback_path = self.get_unique_path(writeback_path)
        writeback_file = open(writeback_path, "ab")
        written = writeback_file.write(data)
        print(f"Wrote {written} to {writeback_path}")      
        return writeback_path, writeback_file    