#!/usr/bin/env bash

cd "$(dirname "${BASH_SOURCE[0]}")"
SCRIPTPATH="`pwd`"

. $SCRIPTPATH/setenv.sh

FTP_ADDRESS=ftp://forge-idi.ign.fr/applications/micmacmgrv2/tests
DATASET=MICMACMGRV2_TNR1

#retrieving dataset
cd $DIRECTORY
if [ ! -e $DATASET ]; then
    wget -r -nv -nH --cut-dirs=3 --user="guest" --password="guest" $FTP_ADDRESS/$DATASET.zip
    unzip -o $DATASET.zip
    rm  $DATASET.zip
fi

#some ugly lines to adjust the current directory in GPAO_PARAMETERS_FILE
GPAO_PARAMETERS_FILE=$DIRECTORY/$DATASET/MICMACMGRV2_TNR1b.json
echo GPAO_PARAMETERS_FILE: $GPAO_PARAMETERS_FILE

GPAO_PARAMETERS_UPDATED_FILE=$DIRECTORY/$DATASET/MICMACMGRV2_parameters.json

if [ -e $GPAO_PARAMETERS_UPDATED_FILE ]; then
    rm $GPAO_PARAMETERS_UPDATED_FILE
fi

cat $GPAO_PARAMETERS_FILE | while  read line ; do
    
    #replaceing DIRECTORY by a single character
    string_to_find="/"$DATASET"/"
    line_update=${line//$string_to_find/"$"}
    line_update_first_part=`echo $line_update | cut -d '$' -f1 `
    line_update_second_part=`echo $line_update | cut -d '$' -f2 `
    if [ "$line_update" == "$line" ]; then
        #cleaning numbers (e.g.: 10. --> 10.0)
        string_to_find=".\""
        string_to_replace=".0\""
        line_update=${line_update//$string_to_find/$string_to_replace}
        echo $line_update >> $GPAO_PARAMETERS_UPDATED_FILE
    else
        #replaceing old directory for current one
        parameter_name=`echo $line_update_first_part | cut -d ':' -f1 `
        line_update=$parameter_name:\"$DIRECTORY/$DATASET/$line_update_second_part
        echo $line_update >> $GPAO_PARAMETERS_UPDATED_FILE
    fi
done

#launching electron

cd $SCRIPTPATH

electron $SCRIPTPATH/../../../main.js \
--ihm $SCRIPTPATH/../ihm_micmacmgr.json \
--parameters $GPAO_PARAMETERS_UPDATED_FILE
