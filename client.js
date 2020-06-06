const electron = require('electron');

const { app } = electron;

const { BrowserWindow } = electron;

let mainWindow;
const url = process.env.GPAO_URL;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 1200,
    webPreferences: {
      nodeIntegration: true,
      webSecurity: false,
    },
  });

  const args = require('minimist')(process.argv);
  if ({}.hasOwnProperty.call(args, 'ihm')) {
    const fs = require('fs');
    const rawdata = fs.readFileSync(args.ihm);
    if (url === undefined) {
    // eslint-disable-next-line no-console
      console.log('env variable GPAO_URL undefined');
      process.exit(1);
    }
    mainWindow.loadURL(`${url}/creation`, {
      postData: [{
        type: 'rawData',
        bytes: Buffer.from(rawdata),
      }],
      extraHeaders: 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8',
    });
  } else {
    mainWindow.loadURL(url);
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// set the view engine to ejs
// app.set('views', path.join(__dirname, 'views'));
// app.set('view engine', 'ejs');

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  app.quit();
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});
