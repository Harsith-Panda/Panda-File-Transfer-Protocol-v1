from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.button import Button
from kivy.lang import Builder
import socket
import os

username_helper = """ 
MDTextField:
    hint_text: "Enter Username"
    hint_helper: "Or hit forgot username"
    helper_text_mode: "on_focus"
    pos_hint: {'center_x':0.5, 'center_y':0.5}
    size_hint_x:None
    width:500
 """

class main(MDApp):
    def build(self):
        screen = Screen()
        username = Builder.load_string(username_helper)
        screen.add_widget(username)
        return screen

main().run()