#this is used to quickly and effiecently rename any files in a folder

import os

path = '/Users/Mohammad/Documents/GitHub/Python-Vision-Processing/src/mask/a'
files = os.listdir(path)


for index, file in enumerate(files):
    os.rename(os.path.join(path, file), os.path.join(path, ''.join([str(index), '.jpg'])))