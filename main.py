import PySimpleGUI as sg
import os

SERVER_IP = "192.168.1.67"
SERVER_SHARE_FOLDER = "Main"
MOUNT_DIR = f"/mnt/{SERVER_SHARE_FOLDER}/"


os.system(f"echo 'flatcow1644' | sudo -S mkdir {MOUNT_DIR} | sudo -S mount -t cifs -w -o username=admin -o "
          f"password=flatcow1644 //{SERVER_IP}/{SERVER_SHARE_FOLDER} {MOUNT_DIR}")

folders = os.listdir(MOUNT_DIR)

for folder in folders:
    print(folder)

layout = [
    [sg.Text("What's your name?")],
    [sg.InputText()],
    [sg.Button('ok'), sg.Button('Cancel')]
]

window = sg.Window('Hello', layout)

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    print('Hello', values[0], '!')

window.close()