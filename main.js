const { BrowserWindow, app, dialog } = require('electron');
const ignGpao = require('ejs-electron-ign-gpao');

require('./app.js');
const ejse = require('ejs-electron');

let mainWindow = null;
let ihmData = {};

function main() {
  // Create the new window
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 1200,
    webPreferences: {
      nodeIntegration: true,
    },
  });


  const args = require('minimist')(process.argv);

  if ({}.hasOwnProperty.call(args, 'ihm')) {
    const fs = require('fs');
    const rawdata = fs.readFileSync(args.ihm);
    ihmData = JSON.parse(rawdata);

    ihmData.jsFolder = '../../js';
    ihmData.page = `${ignGpao.viewFolder()}/pages/creation`;

    if ({}.hasOwnProperty.call(ihmData, 'ihm')) {
      const result = ignGpao.validate(ihmData);
      if (!result.valid) {
        const messagelist = [];
        Array.prototype.forEach.call(result.errors, (error) => {
          const submessagelist = ignGpao.analyzeError(error, ihmData);
          Array.prototype.forEach.call(submessagelist, (submessage) => {
            messagelist.push(submessage);
          });
          if (submessagelist.length < 1) messagelist.push(`${error.message} on ${error.property}`);
        });
        if (messagelist) dialog.showErrorBox('Error', messagelist[0]);
        process.exit(1);
      } else {
        ejse.data('no_header', 'on');
        ejse.data('js_folder', '../../js');
        ejse.data('ihm_data', ihmData.ihm);
        mainWindow.loadURL(`file://${ignGpao.viewFolder()}/pages/creation.ejs`);
      }
    } else {
      // eslint-disable-next-line  no-console
      console.log(dialog.showErrorBox('Error', 'invalid json: ihm key not found'));
      process.exit(1);
    }
  } else {
    // eslint-disable-next-line  no-console
    console.log('no ihm json in arguments. Use: electron main.js --ihm ihmfile.json');
    process.exit(1);
  }

  // eslint-disable-next-line  no-unused-vars
  mainWindow.on('close', (event) => {
    mainWindow = null;
    process.exit(0);
  });
}

app.on('ready', main);
