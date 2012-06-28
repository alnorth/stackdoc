#!/bin/bash

virtualenv --no-site-packages update-from-so-venv
update-from-so-venv/bin/pip install -r update-from-so-requirements.txt

# Get the latest question updates from Stack Overflow
update-from-so-venv/bin/python update-from-so.py

rm -rf venv
