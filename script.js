var http = require('http');
var formidable = require('formidable');
var fs = require('fs');
//import { exec } from 'child_process';
//
//async function sh(cmd) {
//  return new Promise(function (resolve, reject) {
//    exec(cmd, (err, stdout, stderr) => {
//      if (err) {
//        reject(err);
//      } else {
//        resolve({ stdout, stderr });
//      }
//    });
//  });
//}

http.createServer(function(req, res) {
    if(req.url == '/'){
      var content = fs.readFileSync('home.html');
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.end(content);   
    }
    else if(req.url == '/analyze'){
       var form = new formidable.IncomingForm();
       form.parse(req, function (err, fields, files) {
          var oldpath = files.filetoupload.path.trim();
          var newpath = './uploads/' + files.filetoupload.name;
          var mv = require("mv");
          mv(oldpath, newpath, function(err) {
             if (err) {
                console.log('> FileServer.jsx | route: "/files/upload" | err:', err);
                throw err;
            } 
          });
//        let { output } = await sh('python analyze_chat.py' + new_path);
          setTimeout(function(){
              console.log(fs.existsSync(newpath));
          }, 500);
          setTimeout(function(){
              var execSync = require('child_process').execSync;
              var date_frmt = fields.date_format;
              var msgnr = fields.messenger;
              var output = execSync('python analyze_chat.py "' + newpath + '" ' + date_frmt + ' ' + msgnr, { encoding: 'utf-8' });
              console.log(output)
              setTimeout(function(){
                  var content = fs.readFileSync(output.trim());
                  res.writeHead(200, {'Content-Type': 'text/html'  });
                  res.end(content); 
              }, 1500);
          }, 1000);
//          const { exec } = require("child_process");
//          exec("python analyze_chat.py " + newpath);
//          res.writeHead(200, {'Content-Type': 'text/html'});
//          var content = fs.readFileSync('button_page.html');
//          res.end(content);
       });
    }
}).listen(8080, function(){console.log("Server is running...");});