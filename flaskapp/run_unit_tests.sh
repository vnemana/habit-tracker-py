#!/bin/bash

. .venv/bin/activate

pip3 install --require-virtualenv -q -r requirements.txt

docker compose up -d

export PYTHONPATH=$PWD/../

python3 -m unittest discover -s tests

docker compose down