#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
cd $BASEDIR

export GPAO_URL='http://localhost:8000'

export DIRECTORY='/Users/nbellaiche/DATA/TEMP/'
export APPLICATION_DIR='/Applications/MicMacMgrV2.app/Contents/MacOS'
export IGN_DATA='/Applications/MicMacMgrV2.app/Contents/Data'
export GDAL_DATA='/Applications/MicMacMgrV2.app/Contents/Data/geodesy/gdal'
export PROJ_LIB='/Applications/MicMacMgrV2.app/Contents/Data/geodesy/nad'
export GPAO_CLIENT_DIR='/Users/nbellaiche/DATA/TEMP/ign-gpao-client'
electron client.js  --ihm ./data/ihm_micmacmgr.json
