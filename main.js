const { BrowserWindow, app, dialog } = require('electron');
// eslint-disable-next-line  import/no-unresolved
const ignGpao = require('ejs-ign');

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
    // eslint-disable-next-line  no-console
    console.log('parsing ihm json file', args.ihm);

    ihmData = JSON.parse(rawdata);

    ihmData.js_folder = '../../js';
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

  if ({}.hasOwnProperty.call(args, 'parameters')) {
    // eslint-disable-next-line  no-console
    console.log('parameters file: ', args.parameters);
    process.env.PARAMETERS = args.parameters;
  }

  // eslint-disable-next-line  no-unused-vars
  mainWindow.on('close', (event) => {
    mainWindow = null;
    process.exit(0);
  });

  mainWindow.webContents.on('did-finish-load', () => {
    if (process.env.PARAMETERS) {
      mainWindow.webContents.send('setparameters', process.env.PARAMETERS);
    }
    /* let code = `var promise = Promise.resolve(document.getElementById('name').innerHTML);
        promise.then(data => data)`;

        mainWindow.webContents.executeJavaScript(code, true)
        .then((result) => {
            console.log(result) // will be your innherhtml
        }) */
  });
}

app.on('ready', main);
