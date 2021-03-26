#!/usr/bin/env bash

#finding the current dir
cd "$(dirname "${BASH_SOURCE[0]}")"
SCRIPTPATH="`pwd`"

cd ..
cd ..
ROOT=`pwd`

#defining requirements
export SCRIPT_ROOT=$ROOT/scripts
export MEMO_ROOT=/Users/nbellaiche/dev/platinum_code
export PATH=$MEMO_ROOT:$PATH
export TEMP=/Users/nbellaiche/DONNEES/DATA/AI4GEO/donnees/robotcar/out

#launching electron
cd $SCRIPTPATH
electron $ROOT/index.js --ihm $SCRIPTPATH/ihm_memo.json
