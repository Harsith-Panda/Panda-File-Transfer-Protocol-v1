#importing modules
import socket
import tqdm
import os
from cryptography.fernet import Fernet
import tkinter.filedialog

#defining variables
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step
key = '4CIc7Qpyp1XilQcSQkRwD9d5Qsc9xHcM116jYZEI0xM='


# the ip address or hostname of the server, the receiver
host = input(str("Enter host name: "))
# the port number
port = 5001

# create the client socket
s = socket.socket()

#connection authentication messages
print(f"[+] Connecting to {host}:{port}")
def connect():
    connect((host,port))
    print("[+] Connected.")

root = tkinter.Tk()
root.withdraw()   

def send():
    # the name of file we want to send, make sure it exists
    filename = tkinter.filedialog.askopenfilename()
    # get the file size
    filesize = os.path.getsize(filename)

    # send the filename and filesize
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    #Definig tqdm prgress bar structure
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    #Start sending the file
    with open(filename, "rb") as f:
         for _ in progress:
             # read the bytes from the file
             bytes_read = f.read()

             fernet = Fernet(key)
             encrypted = fernet.encrypt(bytes_read)

             if not filename:
                 # file transmitting is done
                 break
             # sendall to assure transimission in busy networks
             s.sendall(encrypted)
             # update the progress bar
             progress.update(len(filename))
    # close the socket
    s.close()

send()