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
         
    

Formalisme du json de description d'interface
- L'objet racine est unique et sa clef doit etre le mot clef 'ihm'. Ceci permet de ne pas le confondre avec des jsond 'autres natures
- Il contient 3 entrees
    - 'content' un vecteur d'objet d'ihm décrivant 'interface
    - 'dependencies': un vecteur d'objets decrivant les dépendances dynamiques entre un objet 'Master' booleen (checkbox/radiobutton) et et un objet Slave qui active oud désactive un champ selon qu'on souhaite ou non que l'utilisateur est accès à ce champ. Un champ inactif n'est pas exporté dans le fichier parameters.json
    - 'oncreate': les taches a effectuer une fois que l'utilisateur a clique sur le bouton 'Executer'
    
    
    'content' contient obligatoirement un vecteur de N objets 'Page', qui correspondront à des onglets dans l'interface
    Chaque Page contient ensuite N objets d'interface, dont les types sont les suivants:
        - Label
        - LineEdit
        - CheckBox
        - FileSelector
        - FolderSelector
        - ComboBox
        - RadioButton
        - Group
        - ButtonGroup
        
    Chaque champ a un intitulé que l'on peut parametrer dans le champ 'Name'
        
    Les objets correspondant à un parametre utilisateur: LineEdit, CheckBox, FileSelector, FolderSelector, ComboBox, RadioButton doivent comporter un champ 'Key' qui permettra d'identifier le champ dans le fichier parameters.json sous la forme d'une paire (Key, Value)
    
    L'objet 'Group' permet de regrouper des parametres sous un même intitulé et d'organiser les champs en les alignant soit verticalement soit horizontalement via la clef 'GroupType' ("GroupType":"VerticalGroup" / "GroupType":"HorizontalGroup"). Il contient ensuite une entree 'content' qui est un vecteur d'objets d'interface, exactement comme l'objet 'Page'. Cette propriété est recursice, c'est à dire qu'on objet 'Group' peut lui-même contenir un objet Group etc...  Il peut comporter une entree 'Key' afin de pouvoir piloter l'activation ou l'inactivation de tout un groupe par un objet 'Master' dans le vecteur des dependencies
    
    L'objet ButtonGroup a la même fonction mais ne fonctionne que pour les RadioButton. En outre il DOIT comporter l'entree 'Key' car c'est cet objet qui identifie l'item selectionné par l'utilisateur. Il comporte une entree content qui est un vecteur de N objets 'RadioButton'
    
    Pour chaque champ editable, le champ 'Value' definit la valeur initiale du champ. 
    
    Le champ 'ValueType' definit la nature du champ 'Boolean', 'Double', 'Integer', 'String', 'Path', 'FilePath'. Le typage du champ permet de valider que l'utilisateur rentre une valeur correcte dans l'interface
    
   Le champ 'ToolTip', optionnel, permet de generer une info-bulle qui s'affiche quand on reste suffisamment longtemps sur le champs afin de decrire plus précisement ce que l'utilisateur doit rentrer 
   
  
  Le vecteur des dependencies est optionnel. Il contient N entrees de 'Type' Dependency' avec un 'Master' qui contient la clef de l'objet maître et un 'Slave' qui contient la clef de l'objet dependant. L'objet maître doit répondre de manière booleenne, donc être de type CheckBox ou RadioButton. L'objet esclave est de nature quelconque du moment qu'il possede une clef. Lorsque l'utilisateur change l'état du Master, l'objet esclave est activé ou désactivé selon le champ 'Inverse'.

L'entree 'oncreate' décrit les operations à effectuer une fois que l'utilisateur a cliqué sur le bouton 'Executer'.
Il comporte 2 entrees:
    - prerequisite contient les informations necessaires à executer les commandes
    - commands contient un vecteur de commandes effectuees sequentiellement après l'export du fichier de parametres utilisateur
    
    'prerequisite' contient 3 entrees:
    - environment: un vecteur de chaines de chaines de caractères correspondant aux variables d'environnement qui doivent être initialisées au moment de l'execution
    - directory: le dossier dans lequel on ecrit le fichier 'parameters.json'
    - resources: un vecteur de path correspondant a des dossiers et fichiers devant exister sur le disque au moment de l'execution. Il est possible d'utiliser les variables d'environnement pour valider l'existence de ces ressources en embrassant les variables d'environnement apr des $.
    
    'commands' contient un vecteur d'objets 'execute' qui sont les commandes a executer. Toute commande executable dans un terminal peut être utilisée. Les variables d'environnement sont egalement interprétées dans la commande
    
    
    
