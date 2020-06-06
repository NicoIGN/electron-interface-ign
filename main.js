const { BrowserWindow, app } = require('electron');

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

  const jsonfile = './data/ihm.json';
  // eslint-disable-next-line import/no-dynamic-require
  const ihmData = require(jsonfile).ihm;
  ejse.data('no_header', 'on');
  ejse.data('js_folder', '../../js');
  ejse.data('ihm_data', ihmData);
  mainWindow.loadURL('file:///Temp/express-useragent/test/client_test.html');

  // mainWindow.loadURL('file://' + ignGpao.view_folder() + '/pages/creation.ejs');
  // eslint-disable-next-line  no-unused-vars
  mainWindow.on('close', (event) => {
    mainWindow = null;
  });
}

app.on('ready', main);
