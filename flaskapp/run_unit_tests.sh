#!/bin/bash

. .venv/bin/activate

export PYTHONPATH=$PWD/../

pip3 install --require-virtualenv -q -r requirements.txt

docker compose up -d

python3 -m unittest tests/test_habit*.py -v

docker compose down