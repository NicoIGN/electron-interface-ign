{
    let  asyncBtn  = document.querySelector('#'+document.currentScript.getAttribute('name'));
    let myForm = undefined;
    
    for (var i = 0; i < document.getElementsByTagName("form").length; i++) {
        let elem = document.getElementsByTagName("form")[i];
        if (elem.hasAttribute('class')){
            if (elem.getAttribute('class') == document.currentScript.getAttribute('params')) {
                myForm = elem;
            }
        }
    }
    if (myForm == undefined)
    {
        dialog.showErrorBox('Oops! Something went wrong!', 'Help us improve your experience by sending an error report')
    }
    
    function updateValue (object, value)
    {
        verbose = false;
        if (verbose) console.log('object:', object);
        if (verbose) console.log('tagName:', object.tagName);
        if (object.tagName.toLowerCase() == 'input')
        {
           if (object.hasAttribute('type'))
           {
               var type = object['type'].toLowerCase();
               if (type == 'checkbox')
               {
                   object.checked = (value == true);
               } else  if (type == 'text')
               {
                    object.value = value;
               } else  if (type == 'radio')
               {
                    let  radioBtn  = document.getElementById(value);
                   radioBtn.checked = true;
               } else
               {
                    object.value = value;
               }
           }
        }
        else if (object.tagName.toLowerCase() == 'select')
        {
            object.value = value;
        }
        object.value = value;
    }
    
    function append(array1, array2)
    {
        count = array1.length;
        for (var i in array2)
        {
            array1[count]=array2[i];
            count = count +1;
        }
    }
    
    let onButtonClick = function() {
        const { dialog, currentWindow } = require('electron').remote;

        let dialogOptions = {
          title: "charger les parametres",
          buttonLabel : "charger",
          properties: ['openFile'],
          filters :[  {name: 'Json file', extensions: ['json']}  ]
        };
        
        dialog.showOpenDialog( currentWindow, dialogOptions).then(result => {
           if(result.canceled == false) {
              let jsonData={};
              console.log('filepath: ',result.filePaths[0]);
                                                                  
              var fs = require('fs');
              var data = fs.readFileSync(result.filePaths[0]);

              const obj = JSON.parse(data);
              if (!obj.hasOwnProperty('parameters')) {
                   dialog.showErrorBox('error', 'not a parameters file');
               }
               jsonData = obj['parameters'];

                  
              var inputs = myForm.querySelectorAll('input');
              append(inputs, myForm.querySelectorAll('select'));
              console.log('number of inputs:', inputs.length);
              for (var i = 0; i < inputs.length; i++)
              {
                  if (inputs[i].hasAttribute("name"))
                  {
                      if (jsonData.hasOwnProperty(inputs[i]["name"]))  {
                         updateValue(inputs[i], jsonData[inputs[i]["name"]]);
                      }
                  }
              }
            }
        }).catch(err => {
          console.log(err)
        })
    }

                        
  asyncBtn.addEventListener("click", onButtonClick);
}
