# Nimble Proxy

This repo is to hide network details and provide a unified interface to miners.

# Development

### Virtual Env

```bash
# create env and activate
make env
source ./nbenv/bin/activate

# install dependencies
brew install python@3.9
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install -e ./

# format
make format

# clean after code dev
deactivate
make clean
```

## Running the Application
```bash
# start dev server
# available at `http://127.0.0.1:8000`
# any code change triggers a server restart in dev
uvicorn main:app --reload
```
