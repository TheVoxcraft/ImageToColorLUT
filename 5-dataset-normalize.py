from PIL import Image
from tqdm import tqdm
from shutil import copyfile
import os

input_folder = "./dataset/"
output_folder = "./dataset-scaled/"

def load_files_from_folder(folderpath, filetype):
    all_files = []
    for root, dirs, files in os.walk(folderpath):
        for file in files:
            if file.endswith(filetype):
                file_path = os.path.join(root, file)
                all_files.append( (file_path, file) )
    return all_files


all_images = load_files_from_folder(input_folder, ".jpg")
all_luts = load_files_from_folder(input_folder, ".cube")

NEW_SIZE = (240, 160)
for img in tqdm(all_images):
    path, filename = img
    try:
        im = Image.open(path)
        im1 = im.resize(NEW_SIZE)
        new_name = filename.split('.')[0]+".jpg"
        lut_pathI = input_folder + "lut-"+filename.split('.')[0]+".cube"
        lut_pathO = output_folder + "lut-"+filename.split('.')[0]+".cube"
        im1.save(output_folder + new_name, quality=95)
        copyfile(lut_pathI, lut_pathO)
    except Exception as e:
        print(e)