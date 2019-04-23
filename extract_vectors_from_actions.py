import numpy as np
import os
import sys
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

print("--> Processing the action file {}".format(sys.argv[1]))

Filename = sys.argv[1].replace("gs://abadia-data/", "")
if ".gz" in Filename:
    localName = "/tmp/actions.gz"
else:
    localName = "/tmp/actions"

print("Download {}".format(Filename))
download_blob(Filename, localName)

print("Transforming some actions to vectors and saving it into a dir")
ngdqn.load_actions_from_a_file(localName)
vectorName = Filename.replace("actions", "vectors").replace(".gz", "").replace(".json", ".data")

print("Processing: {} -> {}".format(Filename, vectorName))
ngdqn.save_actions_as_vectors("/tmp/vectors.data")

print("uploading vectors files to google cloud")
upload_blob("/tmp/vectors.data", vectorName)

print("Transforming some actions to value vectors and saving it into a dir")
value.load_actions_from_a_file(localName)
vectorName = Filename.replace("actions", "values_vectors").replace(".gz", "").replace(".json", ".data")

print("Processing: {} -> {}".format(Filename, vectorName))
value.save_actions_as_vectors("/tmp/value_vector.data")

print("uploading vectors files to google cloud")
upload_blob("/tmp/value_vector.data", vectorName)




