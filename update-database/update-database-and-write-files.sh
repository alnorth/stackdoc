#!/bin/bash

virtualenv --no-site-packages venv
venv/bin/pip install -r requirements.txt


# Write out the files from the database
venv/bin/python write-files.py

rm -rf venv
