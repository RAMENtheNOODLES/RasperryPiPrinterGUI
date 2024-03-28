import PySimpleGUI as sg
import os

SERVER_IP = "192.168.1.67"
SERVER_SHARE_FOLDER = "Main"
MOUNT_DIR = f"/mnt/{SERVER_SHARE_FOLDER}/"
USB_DIR = "'/media/cookiejar/3D PRINTING'"

if not os.path.exists(MOUNT_DIR):
    os.system(f"echo 'flatcow1644' | sudo -S mkdir {MOUNT_DIR} | sudo -S mount -t cifs -w -o username=admin -o "
              f"password=flatcow1644 //{SERVER_IP}/{SERVER_SHARE_FOLDER} {MOUNT_DIR}")

folders = os.listdir(MOUNT_DIR)
sub_dir = []


def isUSBConnected():
    return os.path.exists(USB_DIR)


def rsync(source, destination):
    os.system(f"rsync -vru {source} {destination}")


def get_subdirs():
    global sub_dir

    print(f"Subdir: {sub_dir}")

    subdirs = ""
    for directory in sub_dir:
        print(f"Processing {directory}")
        subdirs += directory + "/"

    return subdirs


layout = []


def update_layout():
    global layout
    layout = [[sg.Text(f"USB: {isUSBConnected()}")]]

    global folders

    subdirs = get_subdirs()
    print(f"Subdirs: {subdirs}")

    folders = os.listdir(MOUNT_DIR + subdirs)

    columns = []

    print(f"Folders: {folders}")
    for folder in folders:
        print(folder)
        columns.append([sg.Button(folder)])

    columns.append([sg.Button("Refresh Drive")])
    if sub_dir:
        columns.append([sg.Button("Transfer This Folder")])
        columns.append([sg.Button("< back")])

    layout.append([sg.Column(columns, scrollable=True, vertical_scroll_only=True)])


update_layout()

window = sg.Window('Hello', layout, size=(380, 420))

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    if event == "Refresh Drive":
        print("Refresh Drive")
        print(f"USB: {isUSBConnected()}")
        update_layout()
        window.close()
        window = sg.Window(f'{MOUNT_DIR}{get_subdirs()}', layout, size=(380, 420))
        # layout[0] = [sg.Text(f"USB: {isUSBConnected()}")]

    if event in folders:
        print("folder found")
        sub_dir.append(event)
        print(*sub_dir)
        update_layout()
        window.close()
        window = sg.Window(f'{MOUNT_DIR}{get_subdirs()}', layout, size=(380, 420))
        print(event)

    if event == "Transfer This Folder":
        rsync(f"{MOUNT_DIR}{get_subdirs()}", f"{USB_DIR}")

    if event == "< back":
        sub_dir.pop()
        update_layout()
        window.close()
        window = sg.Window(f'{MOUNT_DIR}{get_subdirs()}', layout, size=(380, 420))

window.close()
