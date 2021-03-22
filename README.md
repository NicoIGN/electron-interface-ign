# ign-gpao-client
outil s'appuyant sur electronjs permettant d'interpreter une description d'interface en json pour en deduire un formulaire de parametres utilisateur puis de lancer des commandes 
Utilisable pour la creation de chantiers de gpao IGN.

Usage:
- installer npm: https://www.npmjs.com/get-npm
- installer l'application: bash install.sh

Le fichier interface.json decrit 
- l'ensemble des champs a remplir par l'utilisateur
- les ressources qui doivent exister
- le dossier 'DIRECTORY' dans lequel ecrire le formulaire utilisateur
- les variables d'environnement requises
- les commandes a lancer une fois le formulaire rempli

La commande a lancer est: electron main.js --ihm interface.json 

Lorsque les champs sont remplis, l'utilisateur peut lnancer la commande 'Executer'. Un fichier de nom fixé 'parameters.json' est ecrit dans le dossier 'DIRECTORY' défini dans le fichier .json
Puis toutes les commandes 'execute' de post-traitement sont lancees sequentiellement

La syntaxe pour les variables d'environnement dans les lignes de commande est: $VAR$


Exemples: 

    Exemple minimal:
        bash examples/minimal/launch.sh
     
    Exemple plus complet avec differents types et des dependances:
         bash examples/basic/launch.sh
         
    MicMacMgr:
      - ajuster les PATH dans  examples/micmacmgr/macosx-clang/setenv.sh
      - bash examples/micmacmgr/macosx-clang/launch.sh 
         
    Solveg (interface uniquement):
      - bash examples/solveg/macosx-clang/launch.sh 
         
    

