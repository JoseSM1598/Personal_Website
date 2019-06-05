var express = require('express');
var router = express.Router();


let runPy = new Promise(function(success, nosuccess) {

    const { spawn } = require('child_process');
    const pyprog = spawn('python', ['public/pipeline/log_generator.py']);

    pyprog.stdout.on('data', function(data) {
        success(data);
    });
    pyprog.stderr.on('data', (data) => {
        nosuccess(data);

    });
});

/* GET users listing. */
router.get('/', function(req, res, next) {
    res.write('<h1>Hello, World!</h1>');

    runPy.then(function(fromRunpy) {
        console.log(fromRunpy.toString());
        res.end(fromRunpy);
    }).catch(function() {
            console.log("Promise Rejected");
    });
});

module.exports = router;
