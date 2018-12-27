import os, errno
from PIL import Image

cwd = os.getcwd()
x = 640
y = 640
q = 80
res_dir = 'resized'

try:
    os.makedirs(res_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

for file in os.listdir(cwd):
    if file.lower().endswith(('.jpg', '.png', '.jpeg')):
        with Image.open(file) as image:
            image = image.resize((x, y), Image.ANTIALIAS)
            os.chdir(res_dir)
            image.save(file, 'JPEG', quality=q)
            os.chdir(cwd)
