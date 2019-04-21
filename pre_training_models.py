import numpy as np
import os
import argparse
import json
from google.cloud import storage

import AbadIA.NGDQN
import AbadIA.VDQN

storage_client = storage.Client(project='abadia-1')
google_storage_bucket = storage_client.get_bucket('abadia-data')

def download_blob(source_blob_name, destination_file_name):
    blob = google_storage_bucket.blob(source_blob_name)
    directory = os.path.dirname(destination_file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        blob.download_to_filename(destination_file_name)
        print('Blob {} downloaded to {}.'.format(source_blob_name, destination_file_name))
    except:
        print("Error downloading {}".format(source_blob_name,))

def upload_blob(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    blob = google_storage_bucket.blob(destination_blob_name)
    try:
        blob.upload_from_filename(source_file_name)
        print('File {} uploaded to {}.'.format(source_file_name, destination_blob_name))
    except:
        print("Error uploading {}".format(source_file_name))

print("Creating the models classes")

ngdqn = AbadIA.NGDQN.NGDQN(env=None, initModelName=None, modelName=None)
value = AbadIA.VDQN.VDQN(env=None, initModelName=None, modelName=None)

print("--> Download the 1000 last actions list")
download_blob("last_1000_abadia_actions_list.txt", "/tmp/lista")
print("Done")

print("--> Processing the actions files")
days = {}
with open("/tmp/lista") as fp:
   line = fp.readline()
   cnt = 1
   while line:
       print("file {}: {}".format(cnt, line.strip()))
       Filename = line.strip().replace("https://storage.googleapis.com/abadia-data/", "")

       day = Filename.split("/")[1]
       print("Download {} --> {} day {}".format(Filename, Filename, day))
       download_blob(Filename, Filename)
       days[day] = day
       line = fp.readline()
       cnt += 1

for day in days:
    print("Generating values for the day {}".format(day))

    print("Transforming some actions to vectors and saving it into a dir")
    vectors_files = ngdqn.load_actions_from_a_dir_and_save_to_vectors("./games/{}".format(day))

    print("uploading vectors files to google cloud")
    for file in vectors_files:
        print("Uploading --> {} ".format(file))
        upload_blob(file, file)

    print("Transforming some actions to vectors and saving it into a dir")
    value_vectors_files = value.load_actions_from_a_dir_and_save_to_vectors("./games/{}".format(day))

    print("uploading value vectors files to google cloud")
    for file in value_vectors_files:
        print("Uploading --> {} ".format(file))
        upload_blob(file, file)




