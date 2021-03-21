# ign-gpao-client
outil s'appuyant sur electronjs permettant d'interpreter une description d'interface en json pour en deduire un formulaire de parametres utilisateur puis de lancer des commandes 
Utilisable pour la creation de chantiers de gpao IGN.

Usage:
- installer npm: https://www.npmjs.com/get-npm
- installer l'application: bash install.sh
- electron main.js --ihm interface.json 

Le fichier interface.json decrit 
- l'ensemble des champs a remplir par l'utilisateur
- les ressources qui doivent exister
- le dossier 'DIRECTORY' dans lequel ecrire le formulaire utilisateur
- les variables d'environnement requises
- les commandes a lancer une fois le formulaire rempli

Un fichier de nom fixé 'parameters.json' est ecrit dans le dossier 'DIRECTORY'
Puis toutes les commandes 'execute' sont lancees

La syntaxe pour les variables d'environnement dans les lignes de commande est: $VAR$


Example: 
- ajuster les PATH dans  examples/micmacmgr/macosx-clang/setenv.sh
- lancer dans un terminal bash examples/micmacmgr/macosx-clang/launch.sh 
