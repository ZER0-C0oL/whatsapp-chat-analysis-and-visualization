var http = require('http');
var formidable = require('formidable');
var fs = require('fs');
var express = require('express');
// var routes = require('./routes');
// var user = require('./routes/user');
var path = require('path');


var app = express();

// all environments
app.set('port', process.env.PORT || 8080);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');
// app.use(express.favicon());
// app.use(express.logger('dev'));
// app.use(express.json());
// app.use(express.urlencoded());
// app.use(express.methodOverride());
// app.use(app.router);
app.use(express.static(__dirname + 'public'));

function execShellCommand(cmd) {
    const exec = require('child_process').exec;
    return new Promise((resolve, reject) => {
     exec(cmd, (error, stdout, stderr) => {
      if (error) {
       console.warn(error);
      }
      resolve(stdout? stdout : stderr);
     });
    });
   }

app.get('/', function(req, res) {
    fs.readFile('./home.html', function(error, content) {
        if (error) {
            res.writeHead(500);
            res.end();
        }
        else {
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(content, 'utf-8');
        }
    });
});

app.post('/analyze', function(req, res) {
    var form = new formidable.IncomingForm();
    form.parse(req, async function (err, fields, files) {
       var oldpath = files.filetoupload.path.trim();
       var newpath = './uploads/' + files.filetoupload.name;
       var mv = require("mv");
       mv(oldpath, newpath, function(err) {
          if (err) {
             console.log('> FileServer.jsx | route: "/files/upload" | err:', err);
             throw err;
         } 
       });
       var date_frmt = fields.date_format;
       var msgnr = fields.messenger;
       var output = await execShellCommand('python ./analyze_chat.py "' + newpath + '" ' + date_frmt + ' ' + msgnr);
       console.log(output);
       fs.readFile(output.trim(), 'utf-8',  function(err, html) {
           if (err) {
               throw err;
           }
           res.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'});
           res.write(html); 
           res.end();
       })
    });
});

app.listen(8080);