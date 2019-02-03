import os
import json
import numpy as np


def load_actions(name):
    print("-----------------------")
    print(name);
    with open(name) as json_data:
        lines = json_data.readlines()
        if lines:
            rejilla = np.empty([24,24])
            for line in lines:
                # print("line:"+line)
                if (len(line) > 0 and line.startswith("[")):
                    d = json.loads(line)
                    # print("json{}".format(d))
                    print("Rejilla: {}".format(d[0]['action']['nextstate']['Rejilla']))
                    rejilla = np.append(rejilla, d[0]['action']['nextstate']['Rejilla'], axis=0)
                    print(rejilla)
    print("-----------------------")

folders = []
files = []
current_path = ""

for entry in os.scandir('games'):
    if entry.is_dir():
        folders.append(entry.path)
        current_path = entry.path
        for fi in os.scandir(entry.path):
            if fi.is_file():
                files.append(fi.path)
    elif entry.is_file():
        files.append(entry.path)

print('Files:')
print(files)
for file in files:
    if  "abadia_actions" in file and "20190202" in file:
        load_actions(file)


