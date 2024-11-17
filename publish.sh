source .venv/bin/activate
source .env
cd kubero 
git co main && git pull
cd ..
./templatemigration.py
./createindex.py
deactivate

git add index.json
git commit -m "Update index.json"
git push