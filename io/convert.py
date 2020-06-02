import json
import sys
import os
import string
from sys import platform


###
###
###

def readfile(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

###
###
###

def resolve(my_chantier):
    tmpdir = os.getcwd()
    for param in my_chantier['params']:
        if param['cle'] == 'TEMP':
            tmpdir = param['valeur']
        
    for job in my_chantier['jobs']:
        for param in my_chantier['params']:
            job['commande'] = job['commande'].replace('$'+param['cle']+'$', param['valeur'])
            key ='$RELPATH('+param['cle']+')$'
            #relative_path = os.path.relpath(param['valeur'], tmpdir)
            relative_path = os.path.relpath(tmpdir, param['valeur'])
            cmd = job['commande'].replace(key, relative_path)
            if cmd != job['commande']:
                if int(verbose) > 0: print('replacing ', key, 'with ',relative_path, 'value is ', param['valeur'])
                job['commande'] = cmd
                
    return my_chantier
###
###
###

def getIdFromName(pile, name):
    id = -1;
    count = -1
    for p in pile:
        count += 1
        if p['name'] == name:
            id = count
            break
    return id

###
###
###

def convertsimple(my_chantier):
    my_projects = []
        
    # on scanne les blocs et on ne garde que les jobs appartenant a ces blocs
    for bloc in my_chantier['blocs']:
        my_jobs = []
        print( 'scanning bloc', bloc['name'])
        for job in my_chantier['jobs']:
            idlot = job['idlot']
            idbloc =  my_chantier['lots'][idlot]['idbloc']
            if bloc['name'] == my_chantier['blocs'][idbloc]['name']:
                # ce job est bien inclus dans le bloc courant, on l'ajoute.
                my_job = {}
                my_job['name'] = job['name']
                my_job['command'] = job['commande']
                my_job['deps'] = []
                my_jobs.append(my_job)
 
        my_project = {}
        my_project['name'] = bloc['name']
        my_project['jobs'] = my_jobs
        my_project['deps'] = []
        
        # maintenant qu'on a une pile de jobs ordonnee, on peut reconstruire les dependances de jobs
        # avec les identifiants de la nouvelle pile
        for depjob in my_chantier['dependancejobs']:
            jobname = my_chantier['jobs'][depjob['idjob']]['name']
            newid =  getIdFromName(my_project['jobs'], jobname)
            if newid >= 0:
                jobnamedependant = my_chantier['jobs'][depjob['idjobdependant']]['name']
                newiddependant =  getIdFromName(my_project['jobs'], jobnamedependant)
                if newiddependant >= 0:
                    my_dep = {}
                    my_dep['id'] = newiddependant
                    my_project['jobs'][newid]['deps'].append(my_dep)
                    print( 'le job ', jobname, ' d identifiant (', depjob['idjob'], ', ', newid, ') depend du job ', jobnamedependant, 'd identifiant (', depjob['idjobdependant'], ', ', newiddependant, ')')

        print('adding new project', my_project['name'])
        my_projects.append(my_project)
    
    
    # maintenant qu'on a une pile de projects ordonnee, on peut reconstruire les dependances de projects
    # avec les identifiants de la nouvelle pile
    print('building project dependencies')
    for depbloc in my_chantier['dependanceblocs']:
        idbloc = depbloc['idbloc']
        idblocdependant = depbloc['idblocdependant']
        blocname = my_chantier['blocs'][idbloc]['name']
        newid = getIdFromName(my_projects, blocname)
        if newid >= 0:
            blocnamedependant = my_chantier['blocs'][idblocdependant]['name']
            newiddependant =  getIdFromName(my_projects, blocnamedependant)
            if newiddependant >= 0:
                my_dep = {}
                my_dep['id'] = newiddependant
                my_projects[newid]['deps'].append(my_dep)

    print('conversion succeeded')
    outputjsonData = {}
    outputjsonData['projects'] = my_projects

    return outputjsonData

###
###
###

def convertwithmerge(my_chantier):
    my_projects = []
    
    # on cree un project pour les pretraitements
    my_project_pretraitements = {}
    my_project_pretraitements['name'] = "pretraitements"
    my_project_pretraitements['jobs'] = []
    my_project_pretraitements['deps'] = []

    # on scanne les blocs et on ne garde que les jobs appartenant a ces blocs
    for bloc in my_chantier['blocs']:
        my_jobs = {}
        my_newjobs = []
        with_pretraitements = False
        if int(verbose) > 0: print( 'scanning bloc', bloc['name'])
        for job in my_chantier['jobs']:
            idlot = job['idlot']
            if idlot >= 0:
                nomlot = my_chantier['lots'][idlot]['name']
            else:
                my_job = {}
                my_job['name'] = job['name']
                my_job['command'] = job['commande']
                my_project_pretraitements['jobs'].append(my_job)
                continue
            


            idbloc =  my_chantier['lots'][idlot]['idbloc']
            if bloc['name'] == my_chantier['blocs'][idbloc]['name']:
                # ce job est bien inclus dans le bloc courant, on l'ajoute.
                my_job = {}
                my_job['name'] = job['name']
                my_job['command'] = job['commande']
                if int(verbose) > 2: print ('add job ', job['name'], 'in the stack of jobset ', nomlot)
                if not (nomlot in my_jobs):
                    my_jobs[nomlot] = []
                my_jobs[nomlot].append(my_job)
                    
        # on parcourt le tableau des jobs et on cree un job par lot en concatenant les commandes
        # - on suppose qu'il n'y a pas de dependances croisees entre lots
        # - on suppose que les jobs sont ecrits dans l'ordre croissant de dependances
        deps = []
        for nomlot, job in my_jobs.items():
            if len(job) == 0:
                raise NameError("no jobs in ", nomlot)

            if int(verbose) > 0: print ('add ', len(job), ' jobs of lot ', nomlot, ' in project ', bloc['name'])
            my_job = {}
            my_job['name'] = nomlot
            my_job['deps'] = []
            my_job['command'] = ""

            for subjob in job:
                if my_job['command'] == "":
                    my_job['command'] = subjob['command']
                else :
                     my_job['command'] = my_job['command'] + " && " + subjob['command']
           
            my_newjobs.append(my_job)
                
        if int(verbose) > 1: print ('adding ', len(my_newjobs), ' jobs in project')

        my_project = {}
        my_project['name'] = bloc['name']
        my_project['jobs'] = my_newjobs
        my_project['deps'] = []

        if int(verbose) > 0: print ('adding new project', my_project['name'])
        my_projects.append(my_project)


    #on ajoute les pretraitements en dependances de tous les autres projets
    if len(my_project_pretraitements['jobs']) > 0:
        print("ajout du bloc de pretraitements")
        my_projects.insert(0, my_project_pretraitements)
        id_pretraitements = 0

        for project in my_projects:
            if project['name'] != "pretraitements":
                my_dep = {}
                my_dep['id'] = id_pretraitements
                project['deps'].append(my_dep)

    # maintenant qu'on a une pile de projects ordonnee, on peut reconstruire les dependances de projects
    # avec les identifiants de la nouvelle pile
    if int(verbose) > 0: print('building project dependencies')
    
    for depbloc in my_chantier['dependanceblocs']:
        
        idbloc = depbloc['idbloc']
        idblocdependant = depbloc['idblocdependant']
        blocname = my_chantier['blocs'][idbloc]['name']
        newid = getIdFromName(my_projects, blocname)
        if newid >= 0:
            blocnamedependant = my_chantier['blocs'][idblocdependant]['name']
            newiddependant =  getIdFromName(my_projects, blocnamedependant)
            if newiddependant >= 0:
                my_dep = {}
                my_dep['id'] = newiddependant
                my_projects[newid]['deps'].append(my_dep)

    print ('conversion succeeded')
    outputjsonData = {}
    outputjsonData['projects'] = my_projects
    return outputjsonData



###
###
###

def convertwithscript(my_chantier, directory):

    my_projects = []
    
    # on cree un project pour les pretraitements
    my_project_pretraitements = {}
    my_project_pretraitements['name'] = "pretraitements"
    my_project_pretraitements['jobs'] = []
    my_project_pretraitements['deps'] = []

    # on scanne les blocs et on ne garde que les jobs appartenant a ces blocs
    for bloc in my_chantier['blocs']:
        my_jobs = {}
        my_newjobs = []
        with_pretraitements = False
        if int(verbose) > 0: print ('scanning bloc', bloc['name'])
        for job in my_chantier['jobs']:
            idlot = job['idlot']
            if idlot >= 0:
                nomlot = my_chantier['lots'][idlot]['name']
            else:
                my_job = {}
                my_job['name'] = job['name']
                my_job['command'] = job['commande']
                my_project_pretraitements['jobs'].append(my_job)
                continue
            


            idbloc =  my_chantier['lots'][idlot]['idbloc']
            if bloc['name'] == my_chantier['blocs'][idbloc]['name']:
                # ce job est bien inclus dans le bloc courant, on l'ajoute.
                my_job = {}
                my_job['name'] = job['name']
                my_job['command'] = job['commande']
                if int(verbose) > 2: print ('add job ', job['name'], 'in the stack of jobset ', nomlot)
                if not (nomlot in my_jobs):
                    my_jobs[nomlot] = []
                my_jobs[nomlot].append(my_job)
                    
        # on parcourt le tableau des jobs et on cree un job par lot en concatenant les commandes
        # - on suppose qu'il n'y a pas de dependances croisees entre lots
        # - on suppose que les jobs sont ecrits dans l'ordre croissant de dependances
        deps = []
        for nomlot, job in my_jobs.items():
            if len(job) == 0:
                raise NameError("no jobs in ", nomlot)

            if int(verbose) > 0: print ('add ', len(job), ' jobs of lot ', nomlot, ' in project ', bloc['name'])
            my_job = {}
            my_job['name'] = nomlot
            my_job['deps'] = []
            
            script_filename = directory + "/" + nomlot + ".sh"
            my_job['command'] = "sh " + script_filename
            my_newjobs.append(my_job)
            
            script_file = open(script_filename,"w")
            newcommand = ""

            for key in environment:
                if newcommand != "":  newcommand += " && "
                
                if platform == "linux" or platform == "linux2" or platform == "darwin":
                    # linux & macos
                    newcommand += "export " + key + "=" + environment[key]
                elif platform == "win32":
                    # Windows...
                    newcommand += "set " + key + "=" + environment[key]
                
            for subjob in job:
                if newcommand == "":
                    newcommand = subjob['command']
                else :
                     newcommand = newcommand + " && " + subjob['command']
           
            script_file.write(newcommand)
                
        if int(verbose) > 1: print ('adding ', len(my_newjobs), ' jobs in project')

        my_project = {}
        my_project['name'] = bloc['name']
        my_project['jobs'] = my_newjobs
        my_project['deps'] = []

        if int(verbose) > 0: print ('adding new project', my_project['name'])
        my_projects.append(my_project)


    #on ajoute les pretraitements en dependances de tous les autres projets
    if len(my_project_pretraitements['jobs']) > 0:
        print("ajout du bloc de pretraitements")
        my_projects.insert(0, my_project_pretraitements)
        id_pretraitements = 0

        for project in my_projects:
            if project['name'] != "pretraitements":
                my_dep = {}
                my_dep['id'] = id_pretraitements
                project['deps'].append(my_dep)


    # maintenant qu'on a une pile de projects ordonnee, on peut reconstruire les dependances de projects
    # avec les identifiants de la nouvelle pile
    if int(verbose) > 0: print('building project dependencies')
    
    for depbloc in my_chantier['dependanceblocs']:
        idbloc = depbloc['idbloc']
        idblocdependant = depbloc['idblocdependant']
        blocname = my_chantier['blocs'][idbloc]['name']
        newid = getIdFromName(my_projects, blocname)
        if newid >= 0:
            blocnamedependant = my_chantier['blocs'][idblocdependant]['name']
            newiddependant =  getIdFromName(my_projects, blocnamedependant)
            if newiddependant >= 0:
                my_dep = {}
                my_dep['id'] = newiddependant
                my_projects[newid]['deps'].append(my_dep)

    print ('conversion succeeded')
    outputjsonData = {}
    outputjsonData['projects'] = my_projects
    return outputjsonData



def convert(chantier, strategy):
    if strategy == "simple":
        return convertsimple(chantier)
    elif strategy == "mergejoblot":
        return convertwithmerge(chantier)
    elif strategy == "script":
        return convertwithscript(chantier, directory)
    else:
        raise NameError("unhandled stategy")


input = ""
output = ""
strategy="simple" #mergejoblot # script
directory= ""
verbose = 0
count = 0
exedir = ""
gpaoname = ""
resolvekeys = False
environment = {}

for eachArg in sys.argv:
    eachArg = eachArg.lower()
    if eachArg == "--input":
        input=sys.argv[count + 1]
    elif eachArg == "--output":
        output=sys.argv[count + 1]
    elif eachArg == "--gpaoname":
        gpaoname=sys.argv[count + 1]
    elif eachArg == "--strategy":
        strategy=sys.argv[count + 1]
    elif eachArg == "--directory":
        directory=sys.argv[count + 1]
    elif eachArg == "--verbose":
        verbose=sys.argv[count + 1]
    elif eachArg == "--exedir":
        exedir=sys.argv[count + 1]
    elif eachArg == "--env":
        key=sys.argv[count + 1]
        value=sys.argv[count + 2]
        environment[key] = value
    elif eachArg == "--resolvekeys":
        resolvekeys=True
    elif eachArg == "--help":
        print ("usage: python convert.py\n --input inputfile\n --output outputfilename\n  --gpaoname name\n [--strategy simple|mergejoblot|script]\n [--directory script_dir]\n [--resolvekeys]\n [--verbose verbosity_level]\n [--exedir exedir]\n [--env key value]")
        exit(1)
    elif "--" in eachArg:
        print ("unrecognized option: ", eachArg)
        exit(1)
    count += 1

if strategy == "simple":
    if int(verbose) > 1: print ("stategy: simple")
elif strategy == "mergejoblot":
     if int(verbose) > 1: print ("stategy: mergejoblot")
elif strategy == "script":
     if int(verbose) > 1: print ("stategy: script")
else:
    raise NameError("unhandled stategy. Possible values: simple/mergejoblot/script")

if not os.path.exists(input):
    print ("file does not exist: ", input)
    exit(1)

if output.endswith('.json') == False:
    print ("invalid output path: ", output)
    exit(1)
    
if gpaoname == "":
    print ("gpaoname not valid")
    exit(1)

if input == output:
    print ("input and output file names must differ")
    exit(1)

if strategy == "script":
    if not os.path.exists(os.path.dirname(directory)):
        print ("directory does not exist: ", directory)
        exit(1)

if int(verbose) > 0:
    print ("input: ", input)
    print ("output: ", output)
    print ("strategy: ", strategy)
    print ("directory: ", directory)
    print ("resolvekeys: ", resolvekeys)
    print ("gpaoname: ", gpaoname)
    print ("exedir: ", exedir)
    print ("verbose: ", verbose)

#lecture du json
inputjsondata = readfile(input)

if not (gpaoname in inputjsondata):
    print ("invalid main key: ", gpaoname);
    print ("inputjsondata: ", inputjsondata);
    exit(1);
    
chantier = inputjsondata[gpaoname]['chantier']

if exedir != "":
    param = {}
    param['type'] = "String"
    param['cle'] = "EXE_DIR"
    param['valeur'] = exedir
    chantier['params'].append(param)

#resolution des clefs generiques
if resolvekeys == True:
    chantier = resolve(chantier)
    
#conversion dans le nouveau formalisme
outputjsondata = convert(chantier, strategy)

#ecriture du fichier
with open(output, 'w') as outfile:
    json.dump(outputjsondata, outfile, indent=4)


