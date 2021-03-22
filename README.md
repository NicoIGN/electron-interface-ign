# ign-gpao-client
outil s'appuyant sur electronjs permettant d'interpréter une description d'interface en json pour en déduire une interface utilisateur afin de remplir un formulaire de parametres utilisateur puis de lancer des commandes.
Initialement conçu et donc utilisable pour la création de chantiers de gpao IGN.

Usage:
- installer npm: https://www.npmjs.com/get-npm
- installer l'application: bash install.sh

Le fichier interface en json décrit 
- l'ensemble des champs à remplir par l'utilisateur
- les ressources qui doivent exister
- le dossier 'DIRECTORY' dans lequel écrire le formulaire utilisateur sous la forme d'un fichier 'parameters.json'
- les variables d'environnement requises
- les commandes à lancer une fois le formulaire rempli

La commande à lancer est: electron main.js --ihm interface.json 

Lorsque les champs sont remplis, l'utilisateur peut lancer la commande 'Executer'. Un fichier de nom fixé 'parameters.json' est ecrit dans le dossier 'DIRECTORY' défini dans le fichier .json
Puis toutes les commandes 'execute' de post-traitements sont lancées séquentiellement

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
         
    

Formalisme du json de description d'interface
- L'objet racine est unique et sa clef doit être le mot clef 'ihm'. Ceci permet de ne pas le confondre avec des json d'autres natures
- Il contient 3 entrées
    - 'content' un vecteur d'objet d'ihm décrivant 'interface
    - 'dependencies': un vecteur d'objets decrivant les dépendances dynamiques entre un objet 'Master' booleen (checkbox/radiobutton) et et un objet Slave qui active ou désactive un champ selon qu'on souhaite ou non que l'utilisateur ait accès à ce champ. Un champ inactif n'est pas exporté dans le fichier parameters.json
    - 'oncreate': les taches a effectuer une fois que l'utilisateur a cliqué sur le bouton 'Executer'
    
    
    'content' contient obligatoirement un vecteur de N objets de type 'Page', qui correspondront à des onglets dans l'interface
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
        
    Chaque champ a un intitulé que l'on peut paramétrer dans le champ 'Name'
        
    Les objets correspondant à un paramètre utilisateur: LineEdit, CheckBox, FileSelector, FolderSelector, ComboBox, RadioButton doivent comporter un champ 'Key' unique qui permettra d'identifier le champ dans le fichier parameters.json résultant sous la forme d'une paire (Key, Value)
    
    L'objet 'Group' permet de regrouper des paramètres sous un même intitulé et d'organiser les champs en les alignant soit verticalement soit horizontalement via la clef 'GroupType' ("GroupType":"VerticalGroup" / "GroupType":"HorizontalGroup"). Il contient ensuite une entrée 'content' qui est un vecteur d'objets d'interface, exactement comme l'objet 'Page'. Cette propriété est recursice, c'est à dire qu'on objet 'Group' peut lui-même contenir un objet Group etc...  Il peut comporter une entrée 'Key' afin de pouvoir piloter l'activation ou l'inactivation de tout un groupe par un objet 'Master' dans le vecteur des dependencies
    
    L'objet ButtonGroup a la même fonction mais ne fonctionne que pour les RadioButton. En outre il DOIT comporter l'entrée 'Key' car c'est cet objet qui identifie l'item selectionné par l'utilisateur. Il comporte une entrée 'content' qui est un vecteur de N objets de type 'RadioButton'
    
    Pour chaque champ éditable, le champ 'Value' définit la valeur initiale du champ. 
    
    Le champ 'ValueType' definit la nature du champ 'Boolean', 'Double', 'Integer', 'String', 'Path', 'FilePath'. Le typage du champ permet de valider que l'utilisateur rentre une valeur correcte dans l'interface.
    
   Le champ 'ToolTip', optionnel, permet de générer une info-bulle qui s'affiche quand on reste suffisamment longtemps sur le champs afin de décrire plus précisement ce que l'utilisateur doit rentrer 
   
  
  Le vecteur des 'dependencies' est optionnel. Il contient N entrées de 'Type' Dependency' avec un 'Master' qui contient la clef de l'objet maître et un 'Slave' qui contient la clef de l'objet dependant. L'objet maître doit répondre de manière booleenne, donc être de type CheckBox ou RadioButton. L'objet esclave est de nature quelconque du moment qu'il possede une clef 'Key'. Lorsque l'utilisateur change l'état du Master, l'objet esclave est activé ou désactivé dynamiquement selon le champ 'Inverse'.


L'entrée 'oncreate' décrit les operations à effectuer une fois que l'utilisateur a cliqué sur le bouton 'Executer'.
Il comporte 2 entrées:
    - prerequisite contient les informations necessaires à exécuter les commandes
    - commands contient un vecteur de commandes effectuées séquentiellement après l'export du fichier de parametres utilisateur
    
    'prerequisite' contient 3 entrées:
    - environment: un vecteur de chaines de caractères correspondant aux variables d'environnement qui doivent être initialisées au moment de l'exécution
    - directory: le dossier dans lequel on écrit le fichier 'parameters.json'
    - resources: un vecteur de path correspondant à des dossiers et fichiers devant exister sur le disque au moment de l'exécution. Il est possible d'utiliser les variables d'environnement pour valider l'existence de ces ressources, en embrassant les variables d'environnement par le caractère '$'.

    'commands' contient un vecteur d'objets 'execute' qui sont les commandes à exécuter. Toute commande exécutable dans un terminal peut être utilisée. Les variables d'environnement sont également interprétées dans la commande en les embrassant apr le caractère '$'.



