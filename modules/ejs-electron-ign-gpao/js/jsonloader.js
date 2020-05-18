    function loadJson (jsonfile)
    {
        const { BrowserWindow } = require('electron').remote
        var jsonfile = '../data/'+jsonfile;
        ihm_data = require(jsonfile)['ihm'];
        BrowserWindow.loadURL('file://' + __dirname + '/../views/pages/creation.ejs', {electron:'on', json:ihm_data})
    }
