import os
from tqdm import tqdm

path = "logs_Mush2"
NB_FOLDERS = 1710

with open(os.getcwd() + "/" + "NERON_announcements.txt", "w") as f:
    print("Day.Cycle|Annoucement\n", file=f, end='', sep='\n')

for i in tqdm(range(1, NB_FOLDERS + 1)):
    folder_name = path + "/" + str(i)
    for filename in os.listdir(folder_name):
        if filename.endswith(".txt") and "NERON" in filename:
            with open(folder_name + "/" + filename, "r") as f:
                for line in f:
                    print(line.strip(), file=open(os.getcwd() + "/" + "NERON_announcements.txt", "a"))