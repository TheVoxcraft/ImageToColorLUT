import os
import random
from tqdm import tqdm
from shutil import copyfile
import pycubelut

images_path = "./images/"
luts_path = "./mixed_luts/"
output_path = "./dataset/"

def load_files_from_folder(folderpath, filetype=".cube"):
    all_files = []
    for root, dirs, files in os.walk(folderpath):
        for file in files:
            if file.endswith(filetype):
                file_path = os.path.join(root, file)
                all_files.append( (file_path, file) )
    return all_files


all_images = load_files_from_folder(images_path, ".jpg")
all_luts = load_files_from_folder(luts_path, ".cube")
all_luts.extend(load_files_from_folder("./final_luts", ".cube"))

print("Images:",len(all_images))
print("LUTs:",len(all_luts))


for imgpath in tqdm(all_images):
    using_lut_path = random.choice(all_luts)[0]
    try:
        using_lut = pycubelut.read_lut(using_lut_path, True)
        pycubelut.process_image(imgpath[0], output_path, (240, 160), using_lut, False, imgpath[1], desat=False)
        copyfile(using_lut_path, output_path+"lut-"+imgpath[1].split('.')[0]+'.cube')
    except:
        pass
        #print("ups")


'''
for imgpath in all_images: #tqdm(
    using_lut_path = random.choice(all_luts)[0]
    img = lut3d.convert_with_lut(imgpath[0], using_lut_path)
    copyfile(using_lut_path, output_path+imgpath[1])
    img.save(output_path+imgpath[1])
'''