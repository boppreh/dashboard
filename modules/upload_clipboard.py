import os
import shutil
import random
import string
import zipfile
import modules.clipboard as clipboard

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
    if clipboard.get_text():
        path = 'files/' + random_name() + '.txt'
        with open(path, 'wb') as f:
            f.write(clipboard.get_text())
        new_value = upload(path)
        os.remove(path)

    elif clipboard.get_files():
        values_list = []
        for path in clipboard.get_files():
            local_file = 'files/' + os.path.basename(path)

            if os.path.isdir(path):
                local_file += '.zip'
                zip_folder(path, local_file)
            else:
                shutil.copy(path, local_file)

            values_list.append(upload(local_file))
            os.remove(local_file)
        new_value = '\n'.join(values_list)

    elif clipboard.get_bmp():
        path = 'files/' + random_name() + '.png'
        clipboard.get_bmp().save(path, 'PNG')
        new_value = upload(path)
        os.remove(path)

    clipboard.set_text(new_value)
