#!/usr/bin/env bash

python setup.py install
python setup.py build

cp ./.env.example ./.env
