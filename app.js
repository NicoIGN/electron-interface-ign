var path = require('path')
var express = require("express");
const ign_gpao =  require('ejs-electron-ign-gpao')

var app = express();

// set the view engine to ejs
app.set('view engine', 'ejs');

// set the resources folders
console.log('ign_gpao.script_folder():', ign_gpao.script_folder())
app.set('views', ign_gpao.view_folder());
app.use(express.static(ign_gpao.script_folder()))
