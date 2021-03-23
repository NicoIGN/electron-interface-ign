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

InputParamJson = param['kParameterFile']
InputFileTxt = param['kMeshListIn']
OutputFileTxt = param['kMeshListOut'] + '/' + 'meshlist_out.txt'
OutputFilePly = param['kMeshListOut'] + '/' + 'meshlist_out.ply'

cmd = 'MeshChange' + ' ' + 'mode1' + ' ' + InputParamJson + ' ' + InputFileTxt + ' ' + OutputFileTxt
print ('cmd:', cmd)
os.system(cmd)

cmd = 'MeshMosaic' + ' ' + 'mode1' + ' ' + InputParamJson + ' ' + InputFileTxt + ' ' + OutputFileTxt
print ('cmd:', cmd)
os.system(cmd)


