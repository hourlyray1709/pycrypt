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

    def encrypt(self, filepath, output_name=None): 
        key_path = Path("user/key.txt")
        file_path = Path(filepath)
        extension = filepath.split(".")[-1]

        if key_path.exists(): 
            if file_path.exists(): 
                key = open("user/key.txt", "rb").read()
                data = open(filepath, "rb").read()
                f = Fernet(key)
                encrypted_data = f.encrypt(data)

                path = self.write(encrypted_data, extension=f".{extension}")
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

        writeback_path = f"outputs/{pathname}"
        writeback_path = self.get_unique_path(writeback_path)
        writeback_file = open(writeback_path, "wb")
        written = writeback_file.write(data)
        print(f"Wrote {written} to {writeback_path}")
        writeback_file.close()      
        return writeback_path