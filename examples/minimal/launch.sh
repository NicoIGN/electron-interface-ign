#!/usr/bin/env bash

#finding the current dir
cd "$(dirname "${BASH_SOURCE[0]}")"
SCRIPTPATH="`pwd`"

cd ..
cd ..
ROOT=`pwd`

#defining requirements
export SOME_REQUIRED_ENVIRONMENT_VARIABLE=$SCRIPTPATH
export IHMFILE=$SCRIPTPATH/ihm_minimal.json
set OPEN_METHOD=open

#launching electron
cd $ROOT && npm start
