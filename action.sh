#!/bin/bash

pip install -r requirements.txt
./templatemigration.py
./createindex.py

git config --global user.email "Template bot"
git config --global user.name "template.bot@kubero.dev"
cp index.json docs/src/components/Templates/index.json
cd docs
git add src/components/Templates/index.json
git commit -m "Update index.json"
git push
cd ..