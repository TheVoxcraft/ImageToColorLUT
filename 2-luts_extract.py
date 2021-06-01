import os
from shutil import copyfile
from tqdm import tqdm

folder_path = "./unextracted_luts/"

all_files = set()
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".cube"):
            file_path = os.path.join(root, file)
            all_files.add( (file_path, file) )

print("files:",len(all_files))

folder_output = "./luts/"

print("Copied to "+folder_output)
for file in tqdm(all_files):
    copyfile(file[0], folder_output+file[1])