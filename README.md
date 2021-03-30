
electron GUI for command line tools est un petit outil permettant d'interpréter une description d'interface en json pour en déduire une interface utilisateur afin de remplir un formulaire de paramètres puis de lancer des commandes système (cf shema.png).
Il a  été initialement conçu (et est donc utilisable) pour la création de chantiers de gpao des chaînes de traitement image de l'IGN (MicMacMgr, Solveg, MosAR), mais il peut être utilisé pour tout pipeline en ligne de commandes.

Il s'appuie sur la technologie npmjs et le framework 'electron' qui permet de développer des applications multi-plateformes de bureau avec des technologies web. Il est basé sur Chromium, la partie open source de Google Chrome. Electron est un logiciel libre open source développé par GitHub sous licence MIT.

Electron GUI for command line tools s'appuie sur un formalisme de description d'IHM en json dont les spécifications sont décrites ci-dessous. Il n'a pas vocation à proposer une interface esthétique à façon, mais permet de disposer d'une interface basique afin de rendre plus user-friendly (clarté du paramétrage, validation de champs, documentation par info-bulle etc...) un pipeline en lignes de commande avec un effort minimal de développement. 
