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

OutputFileTxt = param['kMeshListOut'] + '/' + 'meshlist_out.txt'
OutputFilePly = param['kMeshListOut'] + '/' + 'meshlist_out.ply'

os.system('MeshChange' + ' ' + 'mode1' + ' ' + param['kParameterFile'] + ' ' + OutputFileTxt)
os.system('MeshMosaic' + ' ' + 'mode1' + OutputFileTxt + ' ' + OutputFilePly)


