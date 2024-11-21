#!/bin/bash

pip install -r requirements.txt
./templatemigration.py
./createindex.py

git add index.json
git commit -m "Update index.json"
git push