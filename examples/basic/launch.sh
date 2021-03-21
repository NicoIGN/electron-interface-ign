#!/usr/bin/env bash

#finding the current dir
cd "$(dirname "${BASH_SOURCE[0]}")"
SCRIPTPATH="`pwd`"

cd ..
cd ..
ROOT=`pwd`

#defining requirements
export SOME_REQUIRED_ENVIRONMENT_VARIABLE=$SCRIPTPATH
export SOME_REQUIRED_ENVIRONMENT_VARIABLE2=$ROOT/io

#launching electron
cd $SCRIPTPATH

electron $ROOT/main.js \
--ihm $SCRIPTPATH/ihm_basic.json
