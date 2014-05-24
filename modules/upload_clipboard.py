import win32clipboard, win32con
import os
import shutil
import random
import string
import zipfile

def random_name(n=8):
    return ''.join(random.choice(string.ascii_letters + string.digits)
                   for i in range(n))

def upload(path):
    scp_fmt = 'scp -i %USERPROFILE%/.ssh/id_rsa "{}" lucasboppre@marte.inf.ufsc.br:public_html'
    os.system(scp_fmt.format(path))
    return 'https://inf.ufsc.br/~lucasboppre/' + os.path.basename(path)

def zip_folder(folder_path, zip_path):
    zip = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(folder_path) + 1
    for base, dirs, files in os.walk(folder_path):
       for f in files:
          fn = os.path.join(base, f)
          zip.write(fn, fn[rootlen:])

def upload_clipboard():
    win32clipboard.OpenClipboard()

    try:
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT):
            path = 'files/' + random_name() + '.txt'
            with open(path, 'wb') as f:
                f.write(win32clipboard.GetClipboardData(win32con.CF_TEXT))
            new_value = upload(path)
            os.remove(path)

        elif win32clipboard.IsClipboardFormatAvailable(win32con.CF_HDROP):
            values_list = []
            for path in win32clipboard.GetClipboardData(win32con.CF_HDROP):
                local_file = 'files/' + os.path.basename(path)

                if os.path.isdir(path):
                    local_file += '.zip'
                    zip_folder(path, local_file)
                else:
                    shutil.copy(path, local_file)

                values_list.append(upload(local_file))
                os.remove(local_file)
            new_value = '\n'.join(values_list)

    finally:
        win32clipboard.CloseClipboard()
    
    if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
        path = 'files/' + random_name() + '.png'
        from PIL import ImageGrab
        image = ImageGrab.grabclipboard()
        image.save(path,'PNG')
        new_value = upload(path)
        os.remove(path)

    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, new_value)
    finally:
        win32clipboard.CloseClipboard()
