#!/usr/bin/env python3
import os
import yaml
import json

# create a new file called index.yaml
open("index.json", "w+")
basedir = "/Users/carafagi/workdir/kubero-dev/kubero/services/"

data = {
    "services": []
}
# find al directories in the current directory and iterate over them
for dirname in os.listdir(basedir):
    dir = os.path.join(basedir, dirname)
    filepath = os.path.join(dir, "service.yaml")
    # check if app.yaml exists in the directory
    if os.path.isfile(filepath):
        print (filepath)
        # if not, skip to the next directory
        with open(filepath, "r") as service_yaml:
            content = service_yaml.read()
            # convert yaml to json
            content = yaml.safe_load(content)
            # write the json to the index.yaml file
            data.get("services").append(content)

with open("index.json", "a+") as index_json:
    contentjson = json.dumps(data)
    index_json.write(contentjson)
exit(0)