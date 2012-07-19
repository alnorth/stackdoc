#!/bin/bash

BASEDIR=$(dirname $0)

virtualenv $BASEDIR/venv
$BASEDIR/venv/bin/pip install -r $BASEDIR/requirements.txt

$BASEDIR/venv/bin/python $BASEDIR/update-database.py $1

rm -rf $BASEDIR/venv
