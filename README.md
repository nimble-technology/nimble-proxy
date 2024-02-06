```markdown
# Nimble Cosmos API

## Introduction

This project is a simple RESTful API built using [FastAPI](https://fastapi.tiangolo.com/).

## Running the Application

Make sure you have installed all required dependencies within your virtual environment (`venv`). If not, activate your virtual environment and install FastAPI and Uvicorn:

```bash
pip install pylint

python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt

pip install fastapi uvicorn
```

To start the development server, navigate to the project directory in your terminal and run:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Any changes to the source code will trigger a server restart during development.
