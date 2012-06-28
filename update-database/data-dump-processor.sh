#!/bin/bash

virtualenv --no-site-packages data-dump-processor-venv
data-dump-processor-venv/bin/pip install -r data-dump-processor-requirements.txt
data-dump-processor-venv/bin/python data-dump-processor-venv.py $1
rm -rf data-dump-processor-venv
