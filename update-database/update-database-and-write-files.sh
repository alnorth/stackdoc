#!/bin/bash

virtualenv --no-site-packages venv
venv/bin/pip install -r requirements.txt

# Get the latest question updates from Stack Overflow
venv/bin/python update-latest-from-so.py

# Write out the files from the database
venv/bin/python write-files.py

rm -rf venv
