

var view_folder = function() {
    const path = require('path')
    return path.join(__dirname, '/views');
}

var script_folder = function() {
    const path = require('path')
    return path.join(__dirname, '/js');
}

const { validationResult } = require('express-validator/check')

var validate = function (req, res, next) {
    result = validationResult(req);
    
    if (!result.isEmpty()) {
        return res.status(400).json({
            'status': result.array({ onlyFirstError: true })[0].msg,
            'errors': result.array({ onlyFirstError: true })
        })
    }
    next()
}


exports.view_folder = view_folder;
exports.script_folder = script_folder;
exports.validate = validate;


