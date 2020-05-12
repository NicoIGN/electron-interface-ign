#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
cd $BASEDIR

GPAO_URL=http://localhost:8000

electron client.js  --ihm ./data/ihm.json
