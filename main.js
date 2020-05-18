const { BrowserWindow, app } = require('electron')

require('./app.js')
const ejse = require('ejs-electron')

const ign_gpao =  require('ejs-electron-ign-gpao')

let mainWindow = null

function main() {
    
    //Create the new window
    mainWindow = new BrowserWindow({
                                   "width": 1200,
                                   "height": 1200,
                                   "webPreferences": {
                                   nodeIntegration: true
                                   }
                                   });

    var jsonfile = './data/ihm.json';
    ihm_data = require(jsonfile)['ihm'];
    ejse.data('electron', 'on');
    ejse.data('ihm_data', ihm_data);

    console.log('file://' + ign_gpao.view_folder() + '/pages/creation.ejs')
    mainWindow.loadURL('file://' + ign_gpao.view_folder() + '/pages/creation.ejs');
    mainWindow.on('close', event => {
                  mainWindow = null
                  })
}

app.on('ready', main)
