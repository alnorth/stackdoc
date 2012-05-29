#!/bin/bash

virtualenv --no-site-packages venv
venv/bin/pip install -r requirements.txt
venv/bin/python parser.py $1
rm -rf venv
