#this is used to quickly and effiecently rename any files in a folder
import os

cd = input('what is the folder location: ')
name = input('what would you like the file names to be: ')
file_type = input('file type: ')

path = '/Users/Mohammad/Documents/GitHub/Python-Vision-Processing/src/' + cd
files = os.listdir(path)


for index, file in enumerate(files):
    os.rename(os.path.join(path, file), os.path.join(path, ''.join([name + '_' + str(index), file_type.lower()])))