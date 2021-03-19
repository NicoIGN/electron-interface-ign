# ign-gpao-client
outil s'appuyant sur electronjs permettant d'interpreter une description d'interface en json pour en deduire un formulaire de parametres utilisateur puis de lancer des commandes 
Utilisable pour la creation de chantiers de gpao IGN.

Usage:
- installer electronjs
- installer l'application: bash install.sh
- electron main.js --ihm interface.json

Le fichier interface.json decrit 
- l'ensemble des champs a remplir par l'utilisateur
- les ressources qui doivent exister
- les variables d'environnement requises
- les commandes a lancer une fois le formulaire rempli

Example: 
- bash examples/micmacmgr/macosx-clang/launch.sh
