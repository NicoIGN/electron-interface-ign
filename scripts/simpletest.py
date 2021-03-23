import sys
import os
import string
from sys import platform
import json

###
###
###
#lecture du json
def readfile(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

###
###
###

inputjsondata = readfile(sys.argv[1])
param = inputjsondata['param']

#ecriture du fichier
with open(sys.argv[2], 'w') as f:
    f.write("this is a simple test:\n")
    for p in param.keys():
         f.write('value of ('+p +') is: ' + json.dumps(param[p])+'\n')
    
    f.close()


