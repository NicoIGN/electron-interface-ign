const express = require('express');
const ignGpao = require('ejs-electron-ign-gpao');

const app = express();

// set the view engine to ejs
app.set('view engine', 'ejs');

// set the resources folders
app.set('views', ignGpao.view_folder());
app.use(express.static(ignGpao.script_folder()));
