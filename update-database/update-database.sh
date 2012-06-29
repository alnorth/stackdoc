#!/bin/bash

virtualenv --no-site-packages venv
venv/bin/pip install -r requirements.txt

venv/bin/python update-database.py

rm -rf venv
