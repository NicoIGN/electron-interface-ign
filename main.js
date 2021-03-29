// Modules to control application life and create native browser window

// eslint-disable-next-line  import/no-unresolved
import { app, BrowserWindow, dialog } from 'electron';

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow = null;

// eslint-disable-next-line  import/no-unresolved
const ignGpao = require('ejs-ign');

const ejse = require('ejs-electron');

let ihmData = {};

function createWindow() {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  const args = require('minimist')(process.argv);

  if ({}.hasOwnProperty.call(args, 'ihm')) {
    // eslint-disable-next-line  no-console
    console.log('ihm file: ', args.ihm);
    process.env.IHMFILE = args.ihm;
  }

  if ({}.hasOwnProperty.call(args, 'parameters')) {
    // eslint-disable-next-line  no-console
    console.log('parameters file: ', args.parameters);
    process.env.PARAMETERS = args.parameters;
  }

  if (process.env.IHMFILE) {
    const fs = require('fs');
    const rawdata = fs.readFileSync(process.env.IHMFILE);
    // eslint-disable-next-line  no-console
    console.log('parsing ihm json file', process.env.IHMFILE);

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
    console.log('no json file desccribing ihm found. Set up environment variable IHMFILE');
    process.exit(1);
  }

  // Open the DevTools.
  // mainWindow.webContents.openDevTools();

  // Emitted when the window is closed.
  mainWindow.on('closed', () => {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null;
  });
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) createWindow();
});
