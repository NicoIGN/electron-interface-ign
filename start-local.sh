#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
cd $BASEDIR

export GPAO_URL='http://localhost:8000'

export DIRECTORY='/Users/nbellaiche/DATA/TEMP/'
export APPLICATION_DIR='/Applications/SolVeg.app/Contents/MacOS'
export IGN_DATA='/Applications/SolVeg.app/Contents/Data'
export PROJ_LIB='/Applications/SolVeg.app/Contents/Data/geodesy/nad'
export GPAO_CLIENT_DIR='/Users/nbellaiche/DATA/TEMP/ign-gpao-client'

#electron main.js  --ihm ./data/ihm_solveg.json
electron main.js  --ihm ./data/ihm_micmacmgr.json
