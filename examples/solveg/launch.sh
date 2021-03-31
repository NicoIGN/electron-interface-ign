#!/usr/bin/env bash

cd "$(dirname "${BASH_SOURCE[0]}")"
SCRIPTPATH="`pwd`"

. $SCRIPTPATH/setenv.sh


#parameters
export IHMFILE=$SCRIPTPATH/ihm_solveg.json

#launching electron
cd $SCRIPTPATH/../.. && electron .
