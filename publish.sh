source .venv/bin/activate
source .env
git submodule update --init --recursive
./createindex.py
deta deploy
deactivate
