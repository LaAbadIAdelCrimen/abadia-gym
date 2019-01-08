import os
import json

def load_game(name):

    print(name);
    with open(name) as json_data:
        line = json_data.readline()
        print("Data:" + line)
        if (len(line) > 0 and line.startswith("[")):
            d = json.loads(line)
            print(d)


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
    if file.endswith("point") == False:
        load_game(file)

"pp.json".endswith("json")

