#!/usr/bin/env python3
import os
import yaml
import json

# create a new file called index.yaml
basedir = "kubero/services"

def toJson(obj):
    return json.dumps(obj, indent=0).replace("\n", "")

for dirname in os.listdir(basedir):

    dir = os.path.join(basedir, dirname)
    filepath = os.path.join(dir, "service.yaml")
    apppath = os.path.join(dir, "app.yaml")

    if os.path.isfile(filepath) and os.path.isfile(apppath):
        print (filepath)

        with open(apppath, "r") as app_yaml:
            app = app_yaml.read()
            # convert yaml to json
            template = yaml.safe_load(app)

        with open(filepath, "r") as service_yaml:
            service = service_yaml.read()
            # convert yaml to json
            service = yaml.safe_load(service)

        if template.get("metadata") is None:
            template["metadata"] = {}
        if template["metadata"].get("annotations") is None:
            template["metadata"]["annotations"] = {}
            

        #template["metadata"]["annotations"] = service
        template["metadata"]["annotations"]['kubero.dev/template.source'] = service["source"]
        template["metadata"]["annotations"]['kubero.dev/template.title'] = service["name"]
        template["metadata"]["annotations"]['kubero.dev/template.description'] = service["description"]
        template["metadata"]["annotations"]['kubero.dev/template.icon'] = service["icon"]
        template["metadata"]["annotations"]['kubero.dev/template.website'] = service["website"]
        template["metadata"]["annotations"]['kubero.dev/template.installation'] = service.get("installation", "")

        template["metadata"]["annotations"]['kubero.dev/template.architecture'] = toJson(service.get("architecture", []))
        template["metadata"]["annotations"]['kubero.dev/template.tags'] = toJson(service.get("tags", []))
        template["metadata"]["annotations"]['kubero.dev/template.screenshots'] = toJson(service.get("screenshots", []))
        template["metadata"]["annotations"]['kubero.dev/template.links'] = toJson(service.get("documentation", []))

        open("kubero/templates/"+dirname+".yaml", "w+")
        with open("kubero/templates/"+dirname+".yaml", "a+") as templateFile:
            templateYaml = yaml.dump(template, default_style=None, default_flow_style=False)
            templateFile.write(templateYaml.replace("\n\n", "\n"))

        os.remove(apppath)
        os.symlink("kubero/templates/"+dirname+".yaml", apppath)

exit(0)