import os

from glob import glob
from tqdm import tqdm

import pandas as pd

LOGS_FOLDER_PATH = "logs_Mush2"
DESTINATION_PATH = "data/NERON_announcements.csv"
NB_FOLDERS = 1710

with open(DESTINATION_PATH, "w") as f:
    print("Ship|Day.Cycle|Annoucement\n", file=f, end='', sep='\n')

neron_files = glob(LOGS_FOLDER_PATH + "/**/*NERON.txt", recursive=True)

for i, file_name in enumerate(tqdm(neron_files, total=len(neron_files))):
    with open(file_name, "r") as file:
        for line in file:
            line += str(i) + "|" # add ship number
            line = line.replace("||", "") # remove double pipes
            print(line.strip(), file=open(DESTINATION_PATH, "a"), end='')

# remove last line of file
os.system("sed -i '$ d' " + DESTINATION_PATH)