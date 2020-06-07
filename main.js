const { BrowserWindow, app } = require('electron');
const ignGpao = require('ejs-electron-ign-gpao');

require('./app.js');
const ejse = require('ejs-electron');

let mainWindow = null;

function main() {
  // Create the new window
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 1200,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  const jsonfile = './data/ihm_micmacmgr.json';
  // eslint-disable-next-line import/no-dynamic-require
  const ihmData = require(jsonfile).ihm;
  ejse.data('no_header', 'on');
  ejse.data('js_folder', '../../js');
  ejse.data('ihm_data', ihmData);

  mainWindow.loadURL('file://' + ignGpao.viewFolder() + '/pages/creation.ejs');
 
    // eslint-disable-next-line  no-unused-vars
  mainWindow.on('close', (event) => {
    mainWindow = null;
  });
}

app.on('ready', main);
