from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDRectangleFlatButton
from helpers import username_helper
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen,ScreenManager
import socket
import os
import tqdm
from cryptography.fernet import Fernet

class FileChoosePopup(Popup):
    load = ObjectProperty()

class main(MDApp):
    file_path = StringProperty("No file chosen")
    the_popup = ObjectProperty(None)

    def build(self):
        self.hoo = socket.gethostname() 
        screen = Screen()
        self.username = Builder.load_string(username_helper)
        button = MDRectangleFlatButton(text='send file', pos_hint={'center_x':0.5, 'center_y':0.4}, on_release=self.show_data)
        fbuttn = MDRectangleFlatButton(text='Select file to send', pos_hint={'center_x':0.5, 'center_y':0.3}, on_release=self.open_popup)
        rbuttn = MDRectangleFlatButton(text='recieve file', pos_hint={'center_x':0.5, 'center_y':0.2}, on_release=self.recieve_file)
        screen.add_widget(self.username)
        screen.add_widget(button)
        screen.add_widget(fbuttn)
        screen.add_widget(rbuttn)
        screen.add_widget(MDLabel(text=self.hoo))
        return screen

    def show_data(self, obj, *args):
        s = socket.socket()
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096 # send 4096 bytes each time step
        key = '4CIc7Qpyp1XilQcSQkRwD9d5Qsc9xHcM116jYZEI0xM='
        host = self.username.text
        port = 5001
        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
        print("[+] Connected.")
        filename = self.file_path
        filesize = os.path.getsize(filename)
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
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

    def open_popup(self,obj, *args):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()

    def load(self, selection):
        self.file_path = str(selection[0])
        self.the_popup.dismiss()
        print(self.file_path)

    def recieve_file(self,obj, *args):
        key = '4CIc7Qpyp1XilQcSQkRwD9d5Qsc9xHcM116jYZEI0xM='
        # device's IP address
        SERVER_PORT = 5001
        # receive 4096 bytes each time
        BUFFER_SIZE = 4096
        SEPARATOR = "<SEPARATOR>"

        # create the server socket
        # TCP socket
        s = socket.socket()

        # bind the socket to our local address
        s.bind((self.hoo, SERVER_PORT))

        # the system will allow before refusing new connections
        s.listen(5)
        print(f"[*] Listening as {self.hoo}:{SERVER_PORT}")

        # accept connection if there is any
        client_socket, address = s.accept() 
        # if below code is executed, that means the sender is connected
        print(f"[+] {address} is connected.")

        # receive the file infos
        # receive using client socket, not server socket
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer
        filesize = int(filesize)

        # start receiving the file from the socket
        # and writing to the file stream
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

        with open(filename, 'wb') as f:
            for _ in progress:
                # read 1024 bytes from the socket (receive)

                bytes_read = client_socket.recv(BUFFER_SIZE)

                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    break
                    # write to the file the bytes we just received
                f.write(bytes_read)

                # update the progress bar
                progress.update(len(filename))

        # close the client socket
        client_socket.close()
        # close the server socket
        s.close()

        def Dec (filename, key):
            file = open(filename, 'rb')
            data = file.read()

            fernet = Fernet(key)
            decrypted = fernet.decrypt(data)

            file = open(filename,'wb')
            file.write(decrypted)
            file.close()

        Dec(filename, key)
    
if __name__ == "__main__":
    main().run()