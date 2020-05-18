const path = require("path");

function getIdFromName(pile, name)
{
    id = -1;
    for (let j in pile) {
        if (pile[j]['name'] == name) {
            id = j
            break
        }
    }
    return id
}

function convert(my_chantier)
{
    my_projects = []
    
    for (let i in my_chantier['blocs']) {
        my_jobs = []
        console.log('scanning bloc', my_chantier['blocs'][i]['name'])
        for (let j in my_chantier['jobs']) {
            idlot = my_chantier['jobs'][j]['idlot']
            idbloc =  my_chantier['lots'][idlot]['idbloc']
            blocname = my_chantier['blocs'][i]['name']
            if (blocname = my_chantier['blocs'][i]) {
                // ce job est bien inclus dans le bloc courant, on l'ajoute.
                my_job = {}
                my_job['name'] = my_chantier['jobs'][j]['name']
                my_job['command'] = my_chantier['jobs'][j]['command']
                my_job['deps'] = []
                my_jobs.push(my_job)
            }
        }
        my_project = {}
        my_project['name'] = my_chantier['blocs'][i]['name']
        my_project['jobs'] = my_jobs
        my_project['deps'] = []
        
        // maintenant qu'on a une pile de jobs ordonnee, on peut reconstruire les dependances de jobs
        // avec les identifiants de la nouvelle pile
        for (let j in my_chantier['dependancejobs']) {
            jobname = my_chantier['jobs'][my_chantier['dependancejobs'][j]['idjob']]['name']
            newid =  getIdFromName(my_project['jobs'], jobname)
            if (newid >= 0) {
                jobnamedependant = my_chantier['jobs'][my_chantier['dependancejobs'][j]['idjobdependant']]['name']
                newiddependant =  getIdFromName(my_project['jobs'], jobnamedependant)
                if (newiddependant >= 0) {
                    my_dep = {}
                    my_dep['id'] = newiddependant
                    my_project['jobs'][newid]['deps'].push(my_dep)
                }
            }
        }
        console.log('adding new project', my_project['name'])
        my_projects.push(my_project)
    }
    
    // maintenant qu'on a une pile de projects ordonnee, on peut reconstruire les dependances de projects
    // avec les identifiants de la nouvelle pile
    console.log('building project dependencies')
    for (let j in my_chantier['dependanceblocs']) {
        idbloc = my_chantier['dependanceblocs'][j]['idbloc']
        idblocdependant = my_chantier['dependanceblocs'][j]['idblocdependant']
        blocname = my_chantier['blocs'][idbloc]['name']
        newid =  getIdFromName(my_projects, blocname)
        if (newid >= 0) {
            blocnamedependant = my_chantier['blocs'][idblocdependant]['name']
            newiddependant =  getIdFromName(my_projects, blocnamedependant)
            if (newiddependant >= 0) {
                my_dep = {}
                my_dep['id'] = newiddependant
                my_projects[newid]['deps'].push(my_dep)
            }
        }
    }
    console.log('conversion succeeded')
    return my_projects
}

///
///
///

inputfile = ''
outputfile = ''
var args = require('minimist')(process.argv)
if (args.hasOwnProperty('input')) {
    inputfile = args['input']
}

if (args.hasOwnProperty('output')) {
    outputfile = args['output']
}

if (inputfile == '' || outputfile == '')
{
    console.log('input or output file not defined')
    return process.exit(-1);
}

console.log('inputfile:', inputfile)
console.log('outputfile:', outputfile)


const fs = require('fs')
let rawdata = fs.readFileSync(inputfile)
jsondata = JSON.parse(rawdata)
my_projects = convert(jsondata['SolVeg']['project'])
outputjsonData = {}
outputjsonData['projects'] = my_projects
try {
    fs.writeFileSync(outputfile, JSON.stringify(outputjsonData, null, '\t'), 'utf-8');
}
catch(e) {
    console.log('cannot save file ', outputfile, e);
}

process.exit(0)
