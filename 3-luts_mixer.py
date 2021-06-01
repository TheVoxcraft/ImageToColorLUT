import random
import lut_tools
import os
from tqdm import tqdm

folder_path = "./scaled_luts/"
output_path = "./mixed_luts/"

all_files = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".cube"):
            file_path = os.path.join(root, file)
            all_files.append( (file_path, file) )

print("files:",len(all_files))

MAKE_NEW_COUNT = 12100

mixes = []
for _ in range(MAKE_NEW_COUNT):
    c1 = random.choice(all_files)
    c2 = random.choice(all_files)
    if c1 != c2:
        mixes.append((c1, c2))

for mix in tqdm(mixes):
    tl1 = lut_tools.load_lut(mix[0][0])
    tl2 = lut_tools.load_lut(mix[1][0])
    lut1 = lut_tools.text_to_lut(tl1[0])
    lut2 = lut_tools.text_to_lut(tl2[0])
    if tl1[1] == tl2[1]: # check grid size
        mix_name = "mix-"+str(random.randint(0,99))+"-"+mix[0][1]+"-"+mix[1][1]
        mixed = lut_tools.rmix(lut1, lut2, 0.4, 0.25)
        if mixed != None:
            lut_tools.save_to_file(lut_tools.create_file(mixed, tl2[1]), output_path+mix_name)

    else:
        print("Errorrr!")