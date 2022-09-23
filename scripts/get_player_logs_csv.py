import os
from tqdm import tqdm

import pandas as pd

path = "data/logs"
NB_FOLDERS = 4

with open("data" + "/" + "new_player_logs.csv", "w") as f:
    print("Ship|Character|Day.Cycle|Event|Log", file=f)

for i in tqdm(range(1711, NB_FOLDERS + 1711)):
    folder_name = path + "/" + str(i)
    #open the folder
    for filename in os.listdir(folder_name):
            #open the file
            with open(folder_name + "/" + filename, "r") as f:
                for line in f:
                    if "[ADM]" in line or not "[" in line or "NERON" in line:
                        continue
                    line +=  str(i) + "|" + filename.split(".txt")[0] + "|"
                    print(line, file=open("data" + "/" + "new_player_logs.csv", "a"), end='')
    
new_logs = pd.read_csv("data/new_player_logs.csv", sep="|")
new_logs = new_logs.drop([0, len(new_logs) - 1])
new_logs["Event"] = new_logs["Event"].apply(lambda x: x.split("EV:")[-1].split("]")[0])
new_logs.to_csv("data/new_player_logs.csv", index=False)