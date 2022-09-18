import os
from tqdm import tqdm

path = "logs_Mush2"
NB_FOLDERS = 2

with open(os.getcwd() + "/" + "clean_player_logs.csv", "w") as f:
    print("Ship|Character|Day.Cycle|Action|Log", file=f)

for i in tqdm(range(1, NB_FOLDERS + 1)):
    folder_name = path + "/" + str(i)
    #open the folder
    for filename in os.listdir(folder_name):
        #open txt files
        if filename.endswith(".txt") and not "Morts" in filename and not "NERON" in filename:
            #open the file
            with open(folder_name + "/" + filename, "r") as f:
                for line in f:
                    if "[ADM]" in line or not "[" in line or "NERON" in line:
                        continue
                    line +=  str(i) + "|" + filename.split(".")[0].split("-")[1] + "|"
                    print(line, file=open(os.getcwd() + "/" + "test.csv", "a"), end='', sep='\n')
    