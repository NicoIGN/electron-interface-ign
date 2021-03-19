#!/usr/bin/env bash

cd "$(dirname "${BASH_SOURCE[0]}")"
SCRIPTPATH="`pwd`"

. $SCRIPTPATH/setenv.sh

electron $SCRIPTPATH/../../../main.js \
--ihm $SCRIPTPATH/../ihm_micmacmgr.json
