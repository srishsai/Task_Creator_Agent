import os
import shutil

# Specify the root directory to search for .venv folders
root_dir = '/Users/srish/Downloads/Task_Creator_Agent'

for dirpath, dirnames, filenames in os.walk(root_dir):
    for dirname in dirnames:
        if dirname == '.venv':
            venv_path = os.path.join(dirpath, dirname)
            print(f'Deleting: {venv_path}')
            shutil.rmtree(venv_path)