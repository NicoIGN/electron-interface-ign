#!/usr/bin/python
import json
import requests
import os
import sys
import socket

HN=socket.gethostname()

input = ""
verbose = 0
url = ""
count = 0

def readfile(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

for eachArg in sys.argv:
    eachArg = eachArg.lower()
    if eachArg == "--input":
        input=sys.argv[count + 1]
    elif eachArg == "--verbose":
        verbose=sys.argv[count + 1]
    elif eachArg == "--url":
        url=sys.argv[count + 1]
    elif eachArg == "--help":
        print ("usage: python insert_project.py\n --input inputfile\n [--url my_url]\n [--verbose verbosity_level]\n");
        exit(1)
    elif "--" in eachArg:
        print ("unrecognized option: ", eachArg);
        exit(1)
    count += 1


if not os.path.exists(input):
    print ("file does not exist: ", input)
    exit(1)

if __name__ == "__main__":

    print("Demarrage du client GPAO")
    print("Hostname : ", HN)

   # url_api = os.getenv('URL_API', 'localhost')
    url_api = url + '/api/project'
    headers = {'Content-Type': "application/json", 'Accept': "application/json"}

    print ('url_api:', url_api)

    res = requests.put(url_api, json=readfile(input), headers=headers)

    print(res.status_code)
    print(res.raise_for_status())
    exit (0)
