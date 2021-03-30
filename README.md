# Electron GUI for command line tools

++++++++++++++++++++++++++++++++++++++
Présentation
++++++++++++++++++++++++++++++++++++++

electron GUI for command line tools est un petit outil permettant d'interpréter une description d'interface en json pour en déduire une interface utilisateur afin de remplir un formulaire de paramètres puis de lancer des commandes système (cf shema.png).
Il a  été initialement conçu (et est donc utilisable) pour la création de chantiers de gpao des chaînes de traitement image de l'IGN (MicMacMgr, Solveg, MosAR), mais il peut être utilisé pour tout pipeline en ligne de commandes.

Il s'appuie sur la technologie npmjs et le framework 'electron' qui permet de développer des applications multi-plateformes de bureau avec des technologies web. Il est basé sur Chromium, la partie open source de Google Chrome. Electron est un logiciel libre open source développé par GitHub sous licence MIT.

Electron GUI for command line tools s'appuie sur un formalisme de description d'IHM en json dont les spécifications sont décrites ci-dessous. Il n'a pas vocation à proposer une interface esthétique à façon, mais permet de disposer d'une interface basique afin de rendre plus user-friendly (clarté du paramétrage, validation de champs, documentation par info-bulle etc...) un pipeline en lignes de commande avec un effort minimal de développement. 

Pour démarrer une nouvelle interface, il est recommandé de se reporter aux exemples ci-dessous.

++++++++++++++++++++++++++++++++++++++
Installation
++++++++++++++++++++++++++++++++++++++

La dépôt git se situe à l'adresse suivante:
https://github.com/NicoIGN/electron-interface-ign

- Assurez-vous que vous avez les droits suffisants pour l'installation.
- installer npm: https://www.npmjs.com/get-npm
- installer l'application: placez-vous à la racine du dépot git et lancez la commande bash install.sh

Notes sur les problèmes potentiels:
 - en cas de timeout, verifiez que votre proxy est correctement paramétré. Au besoin (pour l'IGN), utilisez le script set-proxy-ign à la racine du projet.

 - sous windows, en cas d'erreur du type "Error: Cannot find module '...\npm\node_modules\electron\cli.js' il est possible que npm n'ait pas réussi à installer correctement electron. En ce cas il faut l'installer à la main en le récupérant directement  à cette adresse:   https://github.com/electron/electron/releases/
    Cet outil a été développé et validé avec electron v8.3 sous MacOSX101.5 et v8.5 sous Windows10 64b. Il est donc recommandé d'installer une version 8.x d'electron.
    Placez le dossier dans votre répertoire d'applications et ajoutez le chemin à votre PATH système. 
    
++++++++++++++++++++++++++++++++++++++
Utilisation
++++++++++++++++++++++++++++++++++++++

Pour créer sa propre interface utilisateur, il suffit d'écrire un fichier de description d'interface en json et d'écrire les scripts de relecture du fichier 'parameters.json' résultant afin d'en déduire les commandes à lancer une fois le formulaire rempli par l'utilisateur. Ces scripts peuvent être écrits dans tout langage exécutable via une commande système (DOS bat, bash shell, javascript, python). Dans le cas d'une interface multiOS, il faut cependant faire attention à ce que les commandes soient correctement interprétables sur les différents OS ciblés. Voir les exemples ci-dessous. 
    
Le fichier interface en json décrit :
- l'ensemble des champs à remplir par l'utilisateur
- les ressources qui doivent exister (fichiers, dossiers, exécutables, etc...)
- les variables d'environnement requises
- le dossier 'DIRECTORY' dans lequel écrire le formulaire utilisateur sous la forme d'un fichier 'parameters.json'
- les commandes à lancer une fois le formulaire rempli

La commande à lancer est: "electron ." ou "npm start" après avoir initialisé la variable d'environnement 'IHMFILE' avec le fichier json de description d'interface (voir les scripts launch.sh/.bat dans les exemples)

Il est possible d'initialiser l'interface avec un fichier de paramètres préexistant en initialisant la variable d'environnement 'PARAMETERS'.

Lorsque les champs sont remplis, l'utilisateur peut lancer la commande 'Exécuter'. Un fichier de nom fixé 'parameters.json' est généré dans le dossier 'DIRECTORY' défini dans le fichier '(moninterface).json'
Puis toutes les commandes 'execute' de post-traitements sont lancées séquentiellement.

Exemple du contenu d'un fichier parameters.json résultant (provenant de examples/basic, cf. ci dessous):
{
    "param": {
        "kSomeSimpleLineEdit": "simple text",
        "kSomeIntegerNumberField": "10",
        "kSomeFloatingNumberField": "0.05",
        "kSomeFileSelector": "/some/file/on/the/disk.ext",
        "kSomeFolderSelector": "/some/folder/on/the/disk",
        "kSomeCheckBox1": false,
        "kSomeCheckBox2": false,
        "kSomeCheckBox3": true,
        "kSomeComboBox": " 1"
    }
}
La clef principale 'param' permet de ne pas le confondre avec des json d'autres natures.


++++++++++++++++++++++++++++++++++++++
Exemples: 
++++++++++++++++++++++++++++++++++++++
    Exemple minimal:
        bash examples/minimal/launch.sh
 
   Exemple plus complet avec differents types et des dependances:
       bash examples/basic/launch.sh
     
   MicMacMgr:
      - ajuster les PATH dans  examples/micmacmgr/macosx-clang/setenv.sh
      - bash examples/micmacmgr/macosx-clang/launch.sh 
     
  Solveg (interface uniquement):
      - bash examples/solveg/macosx-clang/launch.sh 
     

++++++++++++++++++++++++++++++++++++++
Formalisme du json de description d'interface:
++++++++++++++++++++++++++++++++++++++

- L'objet racine est unique et sa clef doit être le mot clef 'ihm'. Ceci permet de ne pas le confondre avec des json d'autres natures
- Il contient 3 entrées:
    - 'content' un vecteur d'objet d'ihm décrivant l'interface
    - 'dependencies': un vecteur d'objets décrivant les dépendances dynamiques entre un objet 'Master' booléen (checkbox/radiobutton) et et un objet 'Slave' qui active ou désactive un champ selon qu'on souhaite ou non que l'utilisateur ait accès à ce champ. Un champ inactif n'est pas exporté dans le fichier 'parameters.json'
    - 'oncreate': les tâches à effectuer une fois que l'utilisateur a cliqué sur le bouton 'Executer'
    
    Patron d'un fichier 'ihm':
    { "ihm":{
            "content":[ ... ],
            "dependencies":[...],
            "oncreate":{... }
            }
    }

.   ================
     A- 'content':  
     ================
'content' contient obligatoirement un vecteur de N objets de type 'Page', qui correspondront à des onglets dans l'interface. Pour des pipelines un peu complexes, on peut ainsi organiser les paramètres par grands ensembles: données en entrée, paramétrage et données en sortie, par exemple.
    
Chaque 'Page' contient ensuite N objets d'interface, dont les types sont les suivants:
    - Label
    - LineEdit
    - CheckBox
    - FileSelector
    - FolderSelector
    - ComboBox
    - RadioButton
    - Group
    - ButtonGroup
    
Chaque champ possède un intitulé que l'on peut paramétrer dans le champ 'Name' et qui peut être une chaîne vide.    
    
Les objets correspondant à un paramètre éditable par l'utilisateur sont les suivants:
- LineEdit: un champ texte typable en chaîne quelconque, entier ou nombre flottant
- CheckBox: une case à cocher qui renvoie donc 'true' ou 'false'
- FileSelector: un sélecteur de fichier
- FolderSelector: un sélecteur de dossier
- ComboBox: un menu déroulant avec sélection d'un item
- ButtonGroup / RadioButton: un ensemble d'options parmi lesquelles on ne peut choisir qu'une valeur.

Ces objets doivent comporter un champ 'Key' unique qui permettra d'identifier le champ dans le fichier 'parameters.json' résultant sous la forme d'une paire (key, user value).

L'objet 'Group' permet de regrouper des paramètres sous un même intitulé et d'organiser les champs en les alignant soit verticalement soit horizontalement via la clef 'GroupType' ("GroupType":"VerticalGroup" / "HorizontalGroup"). Il contient ensuite une entrée 'content' qui est un vecteur d'objets d'interface, exactement comme l'objet 'Page'. Cette propriété est récursive, c'est-à-dire que le 'content' d'un objet 'Group' peut lui-même contenir un objet 'Group' etc...  Il peut (mais ce n'est pas requis) comporter une entrée 'Key' afin de pouvoir piloter l'activation ou l'inactivation de tout les objets d'un groupe par un objet 'Master' dans le vecteur des dependencies (cf. ci-dessous).

L'objet ButtonGroup a la même fonction mais ne fonctionne que pour les RadioButton. En outre il DOIT comporter l'entrée 'Key' car c'est cet objet qui identifie l'item selectionné par l'utilisateur. Il comporte une entrée 'content' qui est un vecteur de N objets de type 'RadioButton'.

Pour chaque champ éditable, le champ 'Value' définit la valeur initiale du champ. (remarque: Un champ DefaultValue a été prévu pour réinitialiser les paramètres mais il n'est pas opérationnel dans l'interface pour le moment.)

Le champ 'ValueType' definit la nature du champ 'Boolean', 'Double', 'Integer', 'String', 'Path', 'FilePath'. Le typage du champ permet de valider que l'utilisateur rentre une valeur correcte dans l'interface.

Le champ 'ToolTip', optionnel, permet de générer une info-bulle qui s'affiche quand on reste suffisamment longtemps sur le champ afin de décrire plus précisement ce que l'utilisateur doit rentrer. Par défaut, il affiche simplement la clef du paramètre.


.   ================
  B- 'dependencies':
     ================
  Le vecteur des 'dependencies' est optionnel. Il contient N entrées de 'Type' Dependency' avec un 'Master' qui contient la clef de l'objet maître et un 'Slave' qui contient la clef de l'objet dépendant. L'objet maître doit répondre de manière booléenne, donc être de type CheckBox ou RadioButton. L'objet esclave est de nature quelconque du moment qu'il possède une clef 'Key'. Lorsque l'utilisateur change l'état du Master, l'objet esclave est activé ou désactivé dynamiquement selon le champ 'Inverse'. Un champ inactif n'est pas exporté dans le fichier parameters.json même si une valeur y a été rentrée.
 
 Patron d'un item 'dependency':
  {
     "Master":"kKeyMaster",
     "Slave":"kKeySlave",
     "Type":"Dependency",
     "Inverse":false
  }

   ================
 C- 'oncreate':
    ================
     
L'entrée 'oncreate' décrit les opérations à effectuer une fois que l'utilisateur a cliqué sur le bouton 'Executer'.
Il comporte 2 entrées:
    - 'prerequisite' contient les informations préalables à valider avant d'exécuter les commandes
    - 'commands' contient un vecteur de commandes effectuées séquentiellement après l'export du fichier de paramètres utilisateur.
    
 Patron de l'entrée 'oncreate':
    "oncreate":{
            "prerequisite":{
                 "environment":[...],
                 "directory":"SOME_DIRECTORY",
                 "resources":[...]
            },
            "commands":[...]
    }
   
   'prerequisite' contient 3 entrées:
   - 'environment': un vecteur de chaines de caractères correspondant aux variables d'environnement qui doivent être initialisées au moment de l'exécution`.
   - 'directory' (required): le dossier dans lequel on écrit le fichier 'parameters.json'`;
    - 'resources': un vecteur de path correspondant à des dossiers et fichiers devant exister sur le disque au moment de l'exécution. Il est possible d'utiliser les variables d'environnement pour valider l'existence de ces ressources, en embrassant les variables d'environnement par le caractère '$'.
   
   'commands' contient un vecteur d'objets 'execute' qui sont les commandes à exécuter. Toute commande exécutable dans un terminal peut être utilisée. Les variables d'environnement sont également interprétées dans la commande en les embrassant par le caractère '$'.



