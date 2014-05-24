import modules.clipboard as clipboard
import os
import time
import shutil

REMOVABLE_DRIVE_LETTER = r'D:\\'

def transfer_clipboard():
    paths = clipboard.get_files()

    while not os.path.exists(REMOVABLE_DRIVE_LETTER):
        time.sleep(0.1)

    for path in paths:
        shutil.copy(path, REMOVABLE_DRIVE_LETTER + os.path.basename(path))

    os.system('saferemove.exe ' + REMOVABLE_DRIVE_LETTER[0])
