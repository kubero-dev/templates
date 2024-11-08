source .venv/bin/activate
source .env
cd kubero 
git co main && git pull
cd ..
./templatemigration.py
./createindex.py
deactivate
