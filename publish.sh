source .venv/bin/activate
source .env
cd kubero 
git co main && git pull
cd ..
./createindex.py
deta deploy
deactivate
