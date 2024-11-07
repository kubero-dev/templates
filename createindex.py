#!/usr/bin/env python3
import os
import yaml
import json
import requests
from datetime import datetime

# create a new file called index.yaml
basedir = "kubero/services"
baseURL = "https://raw.githubusercontent.com/kubero-dev/kubero/main/templates/"

data = {
    "services": []
}

GH_Token = os.environ.get("GH_TOKEN")

totalTemplates = 0

# find all directories in the current directory and iterate over them
for dirname in os.listdir(basedir):
    dir = os.path.join(basedir, dirname)
    filepath = os.path.join(dir, "service.yaml")
    apppath = os.path.join(dir, "app.yaml")
    # check if app.yaml exists in the directory
    if os.path.isfile(filepath) and os.path.isfile(apppath):
        print (filepath)
        totalTemplates += 1

        with open(apppath, "r") as app_yaml:
            app = app_yaml.read()
            # convert yaml to json
            app = yaml.safe_load(app)
            # write the json to the index.yaml file

            gitops = False
            if app.get('spec').get('deploymentstrategy') == 'git':
                gitops = True
                
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
                headers = {'Authorization': 'token ' + GH_Token}

                # call the api and get the stars
                apiData = requests.get(apiURL, headers=headers).json()

                if apiData.get("message"):
                    print(apiData.get("message"))
                    print(apiData)
                    exit(1) # make sure index.json is not overwritten
                try: 
                    content["stars"] = apiData.get("stargazers_count")
                    content["forks"] = apiData.get("forks_count")
                    content["watchers"] = apiData.get("watchers_count")
                    content["issues"] = apiData.get("open_issues_count")
                    content["last_updated"] = apiData.get("updated_at")
                    content["last_pushed"] = apiData.get("pushed_at")
                    content["created_at"] = apiData.get("created_at")
                    content["size"] = apiData.get("size")
                    content["language"] = apiData.get("language")
                    content["gitops"] = gitops
                    content["url"] = baseURL + dirname + ".yaml"

                    # calculate date since last update
                    days = (datetime.now() - datetime.strptime(content["last_updated"], "%Y-%m-%dT%H:%M:%SZ")).days

                    content["status"] = "active"
                    if days > 182:
                        content["status"] = "inactive"
                    if days > 365:
                        content["status"] = "abandoned"
                    if days > 730:
                        content["status"] = "archived"

                    license = apiData.get("license")
                    # some repos don't have a license (laravel)
                    if license:
                        content["license"] = license.get("name")
                        content["spdx_id"] = license.get("spdx_id")
                    else:
                        content["license"] = "Unknown"
                        content["spdx_id"] = "-"

                    content["dirname"] = dirname
                except Exception as e:
                    print("Error: ", e)
                    continue

            data.get("services").append(content)
    #print(data)
    #exit(1)

    if totalTemplates % 10 == 0:
        print("more than ", totalTemplates, " templates")
        #break

print("Total Templates: ", totalTemplates)

# sort data by last_pushed
data["services"] = sorted(data["services"], key=lambda k: k['last_pushed'], reverse=True)

open("index.json", "w+")
with open("index.json", "a+") as index_json:
    contentjson = json.dumps(data, indent=2)
    index_json.write(contentjson)
exit(0)