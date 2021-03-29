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
export OPEN_METHOD=open

if [ ! -e $IHMFILE ]; then
    echo current directory must be where the ihm/json file is located
    exit 1
fi

#launching electron
cd $ROOT && npm start
