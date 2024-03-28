import PySimpleGUI as sg
import os

SERVER_IP = "192.168.1.67"
SERVER_SHARE_FOLDER = "Main"
MOUNT_DIR = f"/mnt/{SERVER_SHARE_FOLDER}/"
USB_DIR = "/media/cookiejar/3D PRINTING"

os.system(f"echo 'flatcow1644' | sudo -S mkdir {MOUNT_DIR} | sudo -S mount -t cifs -w -o username=admin -o "
          f"password=flatcow1644 //{SERVER_IP}/{SERVER_SHARE_FOLDER} {MOUNT_DIR}")

folders = os.listdir(MOUNT_DIR)


def isUSBConnected():
    return os.path.exists(USB_DIR)


def rsync(source, destination):
    os.system(f"rsync -vru {source} {destination}")


layout = [[sg.Text(f"USB: {isUSBConnected()}")]]

for folder in folders:
    print(folder)
    layout.append([sg.Button(folder)])

layout.append([sg.Button("Refresh Drive")])

window = sg.Window('Hello', layout)

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    if event == "Refresh Drive":
        layout[0] = [sg.Text(f"USB: {isUSBConnected()}")]

    if event in folders:
        print(event)
        rsync(f"{MOUNT_DIR}{event}", f"{USB_DIR}")

window.close()
