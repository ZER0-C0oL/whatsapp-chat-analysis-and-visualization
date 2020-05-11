var http = require('http');
var formidable = require('formidable');
var fs = require('fs');

http.createServer(function(req, res) {
    if(req.url == '/'){
      var content = fs.readFileSync('home.html');
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.end(content);   
    }
    else if(req.url == '/analyze'){
       var form = new formidable.IncomingForm();
       form.parse(req, function (err, fields, files) {
          var oldpath = files.filetoupload.path;
          var newpath = './uploads/' + files.filetoupload.name;
          const mv = require("mv");
          mv(oldpath, newpath, function(err) {
             if (err) {
                console.log('> FileServer.jsx | route: "/files/upload" | err:', err);
                throw err;
            } 
          });
          const { exec } = require("child_process");
          exec("python analyze_chat.py " + newpath);
//          res.writeHead(200, {'Content-Type': 'text/html'});
//          var content = fs.readFileSync('button_page.html');
//          res.end(content);
           setTimeout(function(){
               var content = fs.readFileSync('analysis.html');
               res.writeHead(200, {'Content-Type': 'text/html'});
               res.end(content); 
           }, 3000);
       });
    }
}).listen(8080);