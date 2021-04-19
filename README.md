# Electron GUI for command line tools

++++++++++++++++++++++++++++++++++++++
Sommaire
++++++++++++++++++++++++++++++++++++++

I- Présentation
II- Installation
III- Utilisation
IV- Exemples
V- Formalisme du json de description d'interface
VI- bogs connus et to-do list
VII- Liens utiles

++++++++++++++++++++++++++++++++++++++
I- Présentation
++++++++++++++++++++++++++++++++++++++

Electron GUI for command line tools est un petit outil permettant d'interpréter une description d'interface en json pour en déduire une interface utilisateur afin de remplir un formulaire de paramètres puis de lancer des commandes système (cf shema.png).
Il a  été initialement conçu (et est donc utilisable) pour la création de chantiers de gpao des chaînes de traitement image de l'IGN (MicMacMgr, Solveg, MosAR), mais il peut être utilisé pour tout pipeline en ligne de commandes.

Il s'appuie sur la technologie npmjs et le framework 'electron' qui permet de développer des applications multi-plateformes de bureau avec des technologies web. Il est basé sur Chromium, la partie open source de Google Chrome. Electron est un logiciel libre open source développé par GitHub sous licence MIT.

Il permet de:
- présenter une interface simple et organisée avec des menus déroulants, des sélecteurs de fichiers, des cases à cocher etc...
- clarifier les paramètres en leur donnant des intitulés clairs et des info-bulles pour renseigner l'utilisateur.
- ne faire apparaître que les paramètres nécessaires aux traitements souhaités.
- valider les champs en vérifiant que leur type (nombre entier, nombre flottant, etc...) est correct.
- s'assurer que des ressources nécessaires au lancement du pipeline (fichiers, dossiers, variables d'environnement) existent bien.

Electron GUI for command line tools s'appuie sur un formalisme de description d'IHM en json dont les spécifications sont décrites ci-dessous. Il n'a pas vocation à proposer une interface esthétique à façon, mais permet de disposer, avec un effort minimal de développement (à savoir l'écriture d'un fichier json), d'une interface simple afin de rendre plus user-friendly un pipeline en lignes de commande. 

Pour démarrer une nouvelle interface, il est recommandé de se reporter aux exemples fourni dans le projet.

++++++++++++++++++++++++++++++++++++++
II- Installation
++++++++++++++++++++++++++++++++++++++

La dépôt git se situe à l'adresse suivante:
https://github.com/NicoIGN/electron-interface-ign

- Assurez-vous que vous avez les droits suffisants pour l'installation.
- installer npm: https://www.npmjs.com/get-npm 
- alternativement sous Ubuntu, vous pouvez installer nodejs avec apt-get:
    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs
    (cf. https://github.com/nodesource/distributions/blob/master/README.md#installation-instructions)
[attention à vérifier vos versions, node v>=12.x et npm v>=6 sont recommandés pour que ce projet fonctionne. ]
- vérifiez votre proxy (cf ci-dessous).
- installer l'application: placez-vous à la racine du dépot git et lancez la commande "bash install.sh".


Notes sur les problèmes d'installation courants d'Electron:

- en cas de timeout ou de message du type:
     "npm ERR! If you are behind a proxy, please make sure that the 'proxy' config is set properly."
     Vérifiez que votre proxy est correctement paramétré. Au besoin (pour l'IGN), utilisez le script set-proxy-ign à la racine du projet.

- en cas d'échec de l'installation d'electron lors de la commande "bash install.sh"
    - vérifiez d'abord que vous avez correctement interprété le problème en lançant la commande 'electron -v' dans un terminal. Cela doit renvoyer une version supérieure ou égale à 12.x.
    - lancez également la commande 'electron' dans un terminal. L'application se lance-t-elle bien?
    
- si electron semble effectivement défectueux:
    - essayez d'abord de lancer la commande: sudo npm install electron -g --verbose --unsafe-perm=true
    
    - en cas de nouvel échec, il faut installer electron à la main, en le récupérant directement  à cette adresse:    https://github.com/electron/electron/releases/
        Cet outil a été développé et validé avec electron v12.0.2 sous MacOSX10.15 et Windows10 64b. Il est donc recommandé d'installer une version 12.x d'electron. [https://github.com/electron/electron/releases/tag/v12.0.2]
        - Téléchargez l'archive correspondant à votre OS, dézippez-la et placez-la dans votre répertoire d'applications (a priori: 'Program Files' sous windows et '/Applications' sous macosx)
        - Lancez l'application et vérifiez que vos préférences de sécurité permettent de la lancer correctement. Au besoin, ajoutez l'exception de sécurité.
        - Puis ajoutez-le chemin au début de votre PATH système:
            par exemple sous macosx: export PATH=/Applications/Electron.app/Contents/MacOS:$PATH
        - Vérifiez que la commande 'electron -v' se lance bien dans un terminal et renvoie la version v12.0.2
        - Vérifiez que cette fois-ci, la commande 'electron'dans un terminal lance bien l'application
        - En ce cas, remplacez la commande de lancement "npm start" "par electron ."
        
++++++++++++++++++++++++++++++++++++++
III- Utilisation
++++++++++++++++++++++++++++++++++++++

Pour créer sa propre interface utilisateur, il suffit d'écrire un fichier de description d'interface en json et de lancer Electron après avoir initialisé des variables d'environnement.

Les commandes de post-traitement à lancer une fois le formulaire rempli par l'utilisateur peuvent être écrites soit directement dans le fichier json (cf examples/minimal), soit en relisant le fichier de paramètres, par exemple dans un script python (cf examples/basic). Toute commande exécutable via une commande système (DOS bat, bash shell, scripts python etc...) est valide. Dans le cas d'une interface multi-OS, il faut cependant faire attention à ce que les commandes soient correctement interprétables sur les différents OS ciblés. Voir les exemples ci-dessous. 
    
Le fichier interface en json décrit :
- l'ensemble des champs à remplir par l'utilisateur
- les ressources qui doivent exister (fichiers, dossiers, exécutables, etc...)
- les variables d'environnement requises
- le dossier 'DIRECTORY' dans lequel écrire le formulaire utilisateur sous la forme d'un fichier 'parameters.json'
- les commandes à lancer une fois le formulaire rempli

La commande à lancer est: "electron ." [ ou son alias "npm start" ] à la racine du projet git, après avoir initialisé la variable d'environnement 'IHMFILE' avec le fichier json de description d'interface (voir les scripts launch.sh/.bat dans les exemples)

Il est possible d'initialiser les valeurs de l'interface avec un fichier de paramètres préexistant en initialisant la variable d'environnement 'PARAMETERS'.

Lorsque les champs sont remplis, l'utilisateur peut lancer la commande 'Exécuter'. Un fichier de nom fixé 'parameters.json' est généré dans le dossier 'DIRECTORY' défini dans le fichier '(moninterface).json'
Puis toutes les commandes 'execute' de post-traitements sont lancées séquentiellement.

Exemple du contenu d'un fichier parameters.json résultant (provenant de examples/basic, cf. ci-dessous):
{
    "param": {
        "kSomeSimpleLineEdit": "simple text",
        "kSomeIntegerNumberField": "10",
        "kSomeFloatingNumberField": "0.05",
        "kSomeFileSelector": "/some/file/on/the/disk.ext",
        "kSomeFolderSelector": "/some/folder/on/the/disk",
        "kSomeCheckBox1": false,
        "kSomeCheckBox2": true,
        "kSomeCheckBox3": true,
        "kSomeRadioButtonGroup": "kRadioButton2",
        "kSomeComboBox": " 1"
    }
}
La clef principale 'param' permet de ne pas le confondre avec des json d'autres natures.

++++++++++++++++++++++++++++++++++++++
IV- Exemples
++++++++++++++++++++++++++++++++++++++

   Exemple minimal:
        bash examples/minimal/launch.sh
 
   Exemple plus complet avec différents types et des dépendances:
       bash examples/basic/launch.sh
     
   MicMacMgr:
      - ajuster les PATH dans  examples/micmacmgr/macosx-clang/setenv.sh
      - bash examples/micmacmgr/macosx-clang/launch.sh 
     
  Solveg (interface uniquement):
      - bash examples/solveg/macosx-clang/launch.sh 
     
++++++++++++++++++++++++++++++++++++++
V- Formalisme du json de description d'interface
++++++++++++++++++++++++++++++++++++++

- L'objet racine est unique et sa clef doit être le mot clef 'ihm'. Ceci permet de ne pas le confondre avec des json d'autres natures.
- Il contient 3 entrées:
    - 'content' un vecteur d'objet d'ihm décrivant l'interface
    - 'dependencies': un vecteur d'objets décrivant les dépendances dynamiques entre objets afin d'activer ou désactiver des champs.
    - 'oncreate': les tâches à effectuer une fois que l'utilisateur a cliqué sur le bouton 'Executer'
    
    Patron de l'entrée 'ihm':
    {
        "ihm":{
                "content":[ ... ],
                "dependencies":[...],
                "oncreate":{... }
        }
     }

.   ================
     A- 'content'
     ================
'content' contient obligatoirement un vecteur de N objets de type 'Page', qui correspondront à des onglets dans l'interface. Pour des pipelines un peu complexes, on peut ainsi organiser les paramètres par grands ensembles: données en entrée, paramétrage et données en sortie, par exemple.

Patron de l'entrée 'content' de 'ihm':
"content":[   { "Name":"Page1",
                      "Type":"Page",
                      "content":[...]
                 }, { "Name":"Page2",
                      "Type":"Page",
                      "content":[...]
                 } ]
    
Chaque 'Page' contient ensuite N objets d'interface, dont les types, identifiés par la propriété "Type", sont les suivants:
    - Label
    - LineEdit
    - CheckBox
    - FileSelector
    - FolderSelector
    - ComboBox
    - Group
    - ButtonGroup
   
   Patron de l'entrée 'content' de 'Page':
    "content":[ { "Type":"Label", ...
                    },{ "Type":"LineEdit", ...
                    },{ "Type":"CheckBox", ...
                    },{ "Type":"FileSelector", ...
                    },{ "Type":"FolderSelector", ...
                    },{ "Type":"ComboBox", ...
                    },{ "Type":"Group", ...
                    },{ "Type":"ButtonGroup", ...
                    } ]
        
        
Les objets correspondant à un paramètre éditable par l'utilisateur sont les suivants:
- LineEdit: un champ texte typable en chaîne quelconque, entier ou nombre flottant
- CheckBox: une case à cocher qui renvoie donc 'true' ou 'false'
- FileSelector: un sélecteur de fichier
- FolderSelector: un sélecteur de dossier
- ComboBox: un menu déroulant avec sélection d'un item
- ButtonGroup / RadioButton: un ensemble d'options parmi lesquelles on ne peut choisir qu'une valeur


Exemple d'un champ LineEdit typé en nombre flottant (cf examples/basic)
{
    "Type":"LineEdit",
    "Key":"kSomeFloatingNumberField",
    "Name":"some floating number field ",
    "Value":"0.0",
    "ValueType":"Double",
    "DefaultValue":"0.0",
    "ToolTip":"info bubble to explain what to enter in this field to the end-user"
}

Ces objets éditables doivent comporter un champ 'Key' unique qui permettra d'identifier le champ dans le fichier 'parameters.json' résultant sous la forme d'une paire (key, user value).

Chaque objet possède en outre un intitulé que l'on peut paramétrer dans le champ 'Name' et qui peut être une chaîne vide.    

Pour chaque champ éditable, le champ 'Value' définit la valeur initiale du champ. [ Remarque: Un champ 'DefaultValue' a été prévu pour réinitialiser les paramètres mais il n'est pas opérationnel dans l'interface pour le moment ]

Le champ 'ValueType' définit la nature du champ 'Boolean', 'Double', 'Integer', 'String', 'Path', 'FilePath'. Le typage du champ permet de valider que l'utilisateur rentre une valeur correcte dans l'interface.

Le champ 'ToolTip', optionnel, permet de générer une info-bulle qui s'affiche quand on reste suffisamment longtemps sur le champ avec la souris afin de décrire plus précisement ce que l'utilisateur doit rentrer. Par défaut, il affiche simplement la clef du paramètre.


L'objet 'Group' permet de regrouper des paramètres sous un même intitulé et d'organiser les champs en les alignant soit verticalement soit horizontalement via la clef 'GroupType' ("GroupType":"VerticalGroup" / "HorizontalGroup"). Il contient ensuite une entrée 'content' qui est un vecteur d'objets d'interface, exactement comme l'objet 'Page'. Cette propriété est récursive, c'est-à-dire que le 'content' d'un objet 'Group' peut lui-même contenir un objet 'Group' etc...  Ceci permet d'organiser les pages en cadrans, en combinant les groupes horizontaux et verticaux.
Il peut (mais ce n'est pas requis) comporter une entrée 'Key' afin de pouvoir piloter l'activation ou l'inactivation de tout les objets de ce groupe par un objet 'Master' dans le vecteur des dependencies (cf. ci-dessous).

Patron d'un Group:
{
    "Type":"Group",
    "Name":"a vertical group to organize fields",
    "Key":"myGroupKey",                                                --> ce groupe possède une clef, ce qui permet de l'activer ou le désactiver en le référençant dans le champ 'Slave' d'une dépendance (cf. ci-dessous)
    "GroupType":"VerticalGroup",                                    --> les objets de ce groupe seront alignés verticalement
    "content":[     { "Type":"Label", ...
                        },{ "Type":"LineEdit", ...
                        },{ "Type":"CheckBox", ...
                        },{ "Type":"FileSelector", ...
                        },{ "Type":"FolderSelector", ...
                        },{ "Type":"ComboBox", ...
                        },{ "Type":"Group", ...                             --> les groupes peuvent comporter des sous-groupes, et ceci, récursivement 
                        },{ "Type":"ButtonGroup", ...
                        } ]
}


L'objet ButtonGroup a la même fonction mais ne fonctionne que pour les RadioButton. En outre il DOIT comporter l'entrée 'Key' car c'est cet objet qui porte la valeur de l'item selectionné par l'utilisateur. Il comporte une entrée 'content' qui est un vecteur de N objets de type 'RadioButton' exclusivement.

Patron d'un ButtonGroup:
{
    "Type":"ButtonGroup",
    "Key":"myGroupKey",  
    "GroupType":"VerticalGroup",     
    "content":[     { "Type":"RadioButton", "Key":"myKey1",  ...
                        },{ "Type":"RadioButton", "Key":"myKey2",  ...
                        } , ...]
}

Le résultat dans le fichier parameters.json si le bouton 2 est coché sera: "myGroupKey": "myKey2".

.   ================
  B- 'dependencies':
     ================

 cette entrée est optionnelle. Elle décrit les dépendances dynamiques entre objets afin d'activer ou désactiver des champs selon qu'on souhaite ou non que l'utilisateur y ait accès. Cela peut notamment servir à neutraliser des options incompatibles avec d'autres.
 Un champ inactif apparaît en grisé, n'est pas éditable par l'utilisateur et n'est pas exporté dans le fichier parameters.json même si une valeur y a été rentrée.
 
   Le vecteur des 'dependencies' contient N entrées 'dependency' qui ont chacune pour entrée un 'Master' qui correspond à la clef de l'objet maître et un 'Slave' qui correspond à la clef de l'objet dépendant. 
 
 L'objet maître doit répondre de manière booléenne, donc être de type CheckBox ou RadioButton.
  L'objet esclave est de nature quelconque du moment qu'il possède une entrée 'Key'. Lorsque l'utilisateur change l'état du Master, l'objet esclave est activé ou désactivé dynamiquement selon le champ 'Inverse'. 
 
 Patron d'un item 'dependency':
  {
     "Master":"kKeyMaster",
     "Slave":"kKeySlave",
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
   
  + 'prerequisite' contient 3 entrées:
     - 'environment': un vecteur de chaines de caractères correspondant aux variables d'environnement qui doivent être initialisées au moment de l'exécution
     - 'directory' (required): le dossier dans lequel on écrit le fichier 'parameters.json'
     - 'resources': un vecteur de path correspondant à des dossiers et fichiers devant exister sur le disque au moment de l'exécution. Il est possible d'utiliser les variables d'environnement pour valider l'existence de ces ressources, en embrassant les variables d'environnement par le caractère '$'
   
  + 'commands' contient un vecteur d'objets 'execute' qui sont les commandes à exécuter. Toute commande exécutable dans un terminal peut être utilisée. 
   Les paramètres de l'interface peuvent être interprétées dans la commande en embrassant la clef du paramètre par le caractère '$'.
   Les variables d'environnement sont également interprétées dans la commande de la même manière en les embrassant par le caractère '$'.

Exemple de oncreate (cf examples/minimal):
    "oncreate":{
        "prerequisite":{
            "environment":[ "SOME_DIRECTORY" ],
            "directory":"SOME_DIRECTORY"
        },
        "commands":[
            {
                "execute":"echo  l utilisateur a rentre la valeur $kSomeSimpleLineEdit$ dans le champ kSomeSimpleLineEdit. Le fichier de parametres est ecrit dans le dossier $SOME_DIRECTORY$"
            }
        ]
    }

++++++++++++++++++++++++++++++++++++++
VI-  bogs connus et to-do list
++++++++++++++++++++++++++++++++++++++

Bogs connus:
- les champs "FileSelector" et "FolderSelector" sont exportés même lorsqu'ils sont inactifs
- les info-bulles des "FileSelector", "FolderSelector" et "ComboBox"  ne s'affichent pas
- les chaînes vides sont considérées comme des Path et des FilePath valides

To-do list:
- vérification de l'unicité des clefs lors du chargement de l'interface
- validation des requirements au lancement de l'application et non lorsque l'utilisateur clique sur 'Executer'
- ajout d'un type 'Tableau'
- ajout d'un filtre sur les extensions de fichiers dans les objets "FileSelector"
- ajout d'un ValueType 'Date' voire d'un 'DateTime' pour les LineEdit
- utilisation de css (Framework Bootstrap) pour rendre l'interface plus modulaire
- pouvoir choisir la page affichée par défaut (actuellement, c'est la dernière de la liste)

++++++++++++++++++++++++++++++++++++++
VII- Liens utiles
++++++++++++++++++++++++++++++++++++++

Json validator. Ce site très pratique permet d'identifier les erreurs de syntaxe json. Très utile lorsque le json d'interface devient un peu conséquent.
- https://jsonformatter.curiousconcept.com

Documentation sur Electron
- https://www.electronjs.org
- https://fr.wikipedia.org/wiki/Electron_(framework)
