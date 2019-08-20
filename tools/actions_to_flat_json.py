import os
import json
import csv
import numpy as np
import sys

def flatten_json(nested_json):
    """
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out

def non_deflatten(json, element):
    if element in json:
        json[element] = str(json[element])

def load_and_flat_actions(action, input_name, output_name):
    print("-----------------------")
    print(input_name);
    with open(input_name) as json_data:
        lines = json_data.readlines()
        if lines:
            rejilla = np.empty([24,24])
            prekeys = []
            keys = []

            fout = open(output_name, "w")
            header = True
            for line in lines:
                # print("line:"+line)
                if (len(line) > 0 and line.startswith("[")):
                    d = json.loads(line)

                    non_deflatten(d[0]['action']['state'], 'Rejilla')
                    non_deflatten(d[0]['action']['nextstate'], 'Rejilla')

                    non_deflatten(d[0]['action']['state'], 'vector')
                    non_deflatten(d[0]['action']['nextstate'], 'vector')

                    non_deflatten(d[0]['action']['state'], 'valMovs')
                    non_deflatten(d[0]['action']['nextstate'], 'valMovs')

                    non_deflatten(d[0]['action']['state'], 'wallMovs')
                    non_deflatten(d[0]['action']['nextstate'], 'wallMovs')

                    non_deflatten(d[0]['action']['state'], 'persMovs')
                    non_deflatten(d[0]['action']['nextstate'], 'persMovs')

                    non_deflatten(d[0]['action']['state'], 'sonidos')
                    non_deflatten(d[0]['action']['nextstate'], 'sonidos')

                    jsonbuffer = flatten_json(d[0])
                    keys = jsonbuffer.keys()
                    if (len(keys) > len(prekeys)):
                        diff = list(set(keys) - set(prekeys))
                    else:
                        diff = list(set(prekeys) - set(keys))

                    print ("diff {} : {}".format(len(diff), diff))
                    prekeys = keys
                    
                    print("[{}]".format(jsonbuffer))
                    print("keys {}".format(len(jsonbuffer.keys())))

                    if (action == "to_json"):
                        # fout.write("")
                        fout.write(json.dumps(jsonbuffer) + "\n")
                        # fout.write("\n")

                    if (action == "to_csv"):
                        if header:
                            header = False
                            w = csv.DictWriter(fout, flatten_json(jsonbuffer))
                            w.writeheader()

                        w.writerow(jsonbuffer)
                        fout.write(json.dumps(jsonbuffer))
            fout.close()
                    # print("json{}".format(d))
                    # print("Rejilla: {}".format(d[0]['action']['nextstate']['Rejilla']))
                    # rejilla = np.append(rejilla, d[0]['action']['nextstate']['Rejilla'], axis=0)
                    #print(rejilla)
    print("-----------------------")


def all_files_curr_dir():
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
    # print(files)
    for file in files:
        if ".json.gz" in file:
            continue
        if  "abadia_actions" in file:
            load_actions(file)


if __name__ == '__main__':
    print("I will flat the {} json {} -> {} json".format(sys.argv[2], sys.argv[1], sys.argv[3]))
    load_and_flat_actions(sys.argv[1], sys.argv[2], sys.argv[3])

