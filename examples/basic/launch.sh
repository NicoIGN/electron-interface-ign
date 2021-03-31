#!/usr/bin/env bash

#finding the current dir
cd "$(dirname "${BASH_SOURCE[0]}")"
SCRIPTPATH="`pwd`"

cd ..
cd ..
ROOT=`pwd`

#defining requirements
export __SLASH__=/
export SOME_REQUIRED_ENVIRONMENT_VARIABLE=$SCRIPTPATH
export SOME_REQUIRED_ENVIRONMENT_VARIABLE2=$ROOT/scripts
export IHMFILE=$SCRIPTPATH/ihm_basic.json
export OPEN_METHOD=open
export PYTHON_EXECUTABLE=python3

#launching electron
cd $ROOT && npm start
