var path = require('path')
var express = require("express");
const ign_gpao =  require('ejs-electron-ign-gpao')

var app = express();

app.set('views', path.join(__dirname, '/views'));
app.use(express.static(ign_gpao.script_folder()))
