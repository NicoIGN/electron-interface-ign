

var view_folder = function() {
    const path = require('path')
    return path.join(__dirname, '/views');
}

var script_folder = function() {
    const path = require('path')
    return path.join(__dirname, '/js');
}


exports.view_folder = view_folder;
exports.script_folder = script_folder;



