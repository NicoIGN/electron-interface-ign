import json
import sys
import os
import string

def readfile(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

def getIdFromName(pile, name):
    id = -1;
    count = -1
    for p in pile:
        count += 1
        if p['name'] == name:
            id = count
            break
    return id


def convertsimple(inputjsondata):
    my_projects = []
    my_chantier = inputjsondata['SolVeg']['chantier']
    
    # on scanne les blocs et on ne garde que les jobs appartenant a ces blocs
    for bloc in my_chantier['blocs']:
        my_jobs = []
        print 'scanning bloc', bloc['name']
        for job in my_chantier['jobs']:
            idlot = job['idlot']
            idbloc =  my_chantier['lots'][idlot]['idbloc']
            if bloc['name'] == my_chantier['blocs'][idbloc]['name']:
                # ce job est bien inclus dans le bloc courant, on l'ajoute.
                #print "job", job
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
                    print 'le job ', jobname, ' d identifiant (', depjob['idjob'], ', ', newid, ') depend du job ', jobnamedependant, 'd identifiant (', depjob['idjobdependant'], ', ', newiddependant, ')'

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

def convertwithmerge(inputjsondata):
    my_projects = []
    my_chantier = inputjsondata['SolVeg']['chantier']
    
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
        print 'scanning bloc', bloc['name']
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
                #print "job", job
                my_job = {}
                my_job['name'] = job['name']
                my_job['command'] = job['commande']
                print 'on ajoute le job ', job['name'], 'dans la pile des jobs du lot ', nomlot
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

            print 'add ', len(job), ' jobs of lot ', nomlot, ' in project ', bloc['name']
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
                
        print 'adding ', len(my_newjobs), ' jobs in project'

        my_project = {}
        my_project['name'] = bloc['name']
        my_project['jobs'] = my_newjobs
        my_project['deps'] = []

        print 'adding new project', my_project['name']
        my_projects.append(my_project)


    #on ajoute les pretraitements en dependances de tous les autres projets
    if len(my_project_pretraitements['jobs']) > 0:
        my_projects.append(my_project_pretraitements)
        id_pretraitements = len(my_projects) -1

        for project in my_projects:
            my_dep = {}
            my_dep['id'] = id_pretraitements
            project['deps'].append(my_dep)

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

    print 'conversion succeeded'
    outputjsonData = {}
    outputjsonData['projects'] = my_projects
    return outputjsonData


def convert(inputjsondata, strategy):
    if strategy == "simple":
        return convertsimple(inputjsondata)
    elif strategy == "mergejoblot":
        return convertwithmerge(inputjsondata)
    elif strategy == "script":
        return convertwithscript(inputjsondata)
    else:
        raise NameError("unhandled stategy")


input = ""
output = ""
strategy="simple" #mergejoblot # script
directory= ""
verbose = 0
count = 0

for eachArg in sys.argv:
    eachArg = eachArg.lower()
    if eachArg == "--input":
        input=sys.argv[count + 1]
    elif eachArg == "--output":
        output=sys.argv[count + 1]
    elif eachArg == "--strategy":
        strategy=sys.argv[count + 1]
    elif eachArg == "--directory":
        directory=sys.argv[count + 1]
    elif eachArg == "--verbose":
        verbose=sys.argv[count + 1]
    elif "--" in eachArg:
        print ("unrecognized option: ", eachArg)
        exit(1)
    count += 1

if strategy == "simple":
    print ("stategy: simple")
elif strategy == "mergejoblot":
    print ("stategy: mergejoblot")
elif strategy == "script":
    print ("stategy: script")
else:
    raise NameError("unhandled stategy. Possible values: simple/mergejoblot/script")

if not os.path.exists(input):
    print "file does not exist: ", input
    exit(1)

if output.endswith('.json') == False:
    print "invalid output path: ", output
    exit(1)

if input == output:
    print "input and output file names must differ"
    exit(1)

if strategy == "script":
    if not os.path.exists(os.path.dirname(directory)):
        print "directory does not exist: ", directory
        exit(1)

print "input: ", input
print "output: ", output
print "strategy: ", strategy
print "directory: ", directory
print "verbose: ", verbose

#lecture du json
inputjsondata = readfile(input)

#conversion dans le nouveau formalisme
outputjsondata = convert(inputjsondata, strategy)

#ecriture du fichier
with open(output, 'w') as outfile:
    json.dump(outputjsondata, outfile, indent=4)

