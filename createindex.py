#!/usr/bin/env python3
import os
import yaml
import json
import requests

# create a new file called index.yaml
basedir = "/Users/carafagi/workdir/kubero-dev/kubero-service-base/services/"

data = {
    "services": []
}
# find all directories in the current directory and iterate over them
for dirname in os.listdir(basedir):
    dir = os.path.join(basedir, dirname)
    filepath = os.path.join(dir, "service.yaml")
    apppath = os.path.join(dir, "app.yaml")
    # check if app.yaml exists in the directory
    if os.path.isfile(filepath) and os.path.isfile(apppath):
        print (filepath)
        # if not, skip to the next directory
        with open(filepath, "r") as service_yaml:
            content = service_yaml.read()
            # convert yaml to json
            content = yaml.safe_load(content)
            # write the json to the index.yaml file

            # check if source contains github string
            if content.get("source").find("github.com") != -1:
                # replace url with api url
                apiURL = content["source"].replace("github.com", "api.github.com/repos")
                # call the api and get the stars
                apiData = requests.get(apiURL).json()

                if apiData.get("message"):
                    print(apiData.get("message"))
                    print(apiData)
                    exit(1)
                content["stars"] = apiData.get("stargazers_count")
                content["forks"] = apiData.get("forks_count")
                content["watchers"] = apiData.get("watchers_count")
                content["issues"] = apiData.get("open_issues_count")
                content["last_updated"] = apiData.get("updated_at")
                content["last_pushed"] = apiData.get("pushed_at")
                content["created_at"] = apiData.get("created_at")
                content["size"] = apiData.get("size")
                content["language"] = apiData.get("language")
                content["license"] = apiData.get("license").get("name")
                content["spdx_id"] = apiData.get("license").get("spdx_id")
                content["dirname"] = dirname


            data.get("services").append(content)

open("index.json", "w+")
with open("index.json", "a+") as index_json:
    contentjson = json.dumps(data)
    index_json.write(contentjson)
exit(0)