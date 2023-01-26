import os
import shutil

root_dir = r'venv'

#Destroy the virtual environment by destroying the venv directory recursively
for root, dirs, files in os.walk(root_dir):

    for name in files:
            print(os.path.join(root, name)) 
            os.remove(os.path.join(root, name))
    for name in dirs:
            print(os.path.join(root, name))
            shutil.rmtree(os.path.join(root, name))
    os.rmdir(root_dir)
