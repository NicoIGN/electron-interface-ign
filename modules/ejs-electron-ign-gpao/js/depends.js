verbose = false;

function activate_dependencies (master)
{
    if (verbose) console.log("in depends.js", master);

    // recherche dans la table des dependances
    var depends = document.querySelectorAll('depends');
    for (var i = 0; i < depends.length; i++)
    {
        if (depends[i].getAttribute('master') == master['id'])
        {
            if (verbose) {
                console.log("depends[i]['master'] ", depends[i].getAttribute('master') );
                console.log("depends[i]['slave'] ", depends[i].getAttribute('slave') );
                console.log("master.checked ", master.checked );
            }
            
            let  asyncElement  = document.querySelector('#'+depends[i].getAttribute('slave') );
            if (asyncElement == undefined)
            {
                console.log("cannot find slave", depends[i].getAttribute('slave'));
            }
            else
            {
                var enabling=true;
                if (master.checked == true) {
                    if (depends[i].getAttribute('inverse') == 'true') {
                        enabling = false;
                    }
                }
                else {
                    if (depends[i].getAttribute('inverse') == 'false') {
                        enabling = false;
                    }
                }
                 if (verbose) console.log("asyncElement must be at state", enabling);
                enable(asyncElement, enabling);
            }
        }
    }
}

function enable (object, enabling)
{
    
    if (verbose) console.log("enable(", object, enabling,")");

    object.disabled = (!enabling);
    for (i in object.children)
    {
        var child=object.children[i];
        enable(child, enabling);
    }
}

function initialize_dependencies ()
{
    console.log("initialize_dependencies");
    var depends = document.querySelectorAll('depends');
    for (var i = 0; i < depends.length; i++)
    {
        let  asyncElement  = document.querySelector('#'+depends[i].getAttribute('master') );
        if (asyncElement == undefined || asyncElement == null)  {
            console.log("cannot find master", depends[i].getAttribute('master'));
        }
        else {
            activate_dependencies(asyncElement);
        }
    }
}
