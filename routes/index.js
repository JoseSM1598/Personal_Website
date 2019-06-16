var express = require('express');
require('dotenv').config();
const nodemailer = require('nodemailer');
const bodyParser = require('body-parser');
var router = express.Router();


/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'José San Martin' });
});


router.post('/contact', function(req,res,next){
    let mailOpts, smtpTrans;
    smtpTrans = nodemailer.createTransport({
        host: 'smtp.gmail.com',
        port: 465,
        secure: true,
        auth: {
            user: process.env.GMAIL_USER,
            pass: process.env.GMAIL_PASS
        }
    });
    mailOpts = {
        from: req.body.name + ' &lt;' + req.body.email + '&gt;',
        to: process.env.GMAIL_USER,
        subject: 'New message from contact form',
        text: `${req.body.name} (${req.body.email}) says: ${req.body.message}`
    };
    smtpTrans.sendMail(mailOpts, function (error, response) {
        if (error) {
            res.render('contact-failure');
        }
        else {
            res.render('contact-success');
        }
    });
});

module.exports = router;
