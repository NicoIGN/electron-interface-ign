function regex(pattern, value)
{
    regexp=new RegExp(pattern)
    return regexp.test(value);
}

function validateValue (object)
{
    if (object.required && object.value == '') {
        return false;
    }
    if (object.hasAttribute('pattern')) {
        return regex(object['pattern'], object.value);
    }
    return true;
}

function readValue (object)
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
               return object.checked;
           } else  if (type == 'text')
           {
               return object.value;
           } else  if (type == 'number')
           {
               return object.value;
           } else  if (type == 'date')
           {
               return object.value;
           }
           else  if (type == 'radio')
           {
               return object.value;
           } else
           {
                return object.value;
           }
       }
    }
    else if (object.tagName.toLowerCase() == 'select')
    {
        return object.value;
    }
    return object.value;
}

function append(array1, array2)
{
    count = array1.length;
    for (var i in array2) {
        array1[count]=array2[i];
        count = count +1;
    }
}

exports.retrieve_parameters = function (myForm) {

    var inputs = myForm.querySelectorAll('input');
    append(inputs, myForm.querySelectorAll('select'));
    var jsonData = {};
    console.log('number of inputs:', inputs.length);
    for (var i = 0; i < inputs.length; i++)
    {
        if (!inputs[i].disabled) {
            if (inputs[i].hasAttribute("name"))
            {
                if (!validateValue(inputs[i])) {
                    dialog.showErrorBox('Error', 'valeur invalide pour le champ ' + inputs[i]["name"])
                    throw ('invalid value for field ' + inputs[i]["name"]);
                }
                jsonData[inputs[i]["name"]] = readValue(inputs[i]);
            }
        }
    }
    return jsonData;
}

exports.save_parameters=function(parameters, filename) {
    jsonParams={};
    jsonParams['param'] = parameters;
    console.log('save ', parameters, 'in ', filename)
    try {
        var fs = require('fs');
        fs.writeFileSync(filename, JSON.stringify(jsonParams, null, '\t'), 'utf-8');
    }
    catch(e) {
        console.log('cannot save file ', filename, e);
    }
}
        

