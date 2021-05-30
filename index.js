const express = require("express");
const multer = require("multer");
const uuid = require('uuid').v4;
const {spawn} = require('child_process');
const bodyParser = require("body-parser");
const path = require('path');
const fs = require('fs');
const app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');


app.use(express.static('public'));

const dirUploads = path.join(__dirname, 'uploads');
if (!fs.existsSync(dirUploads)){
    fs.mkdirSync(dirUploads);
}
const dirImages = path.join(__dirname, 'public/images');
if (!fs.existsSync(dirImages)){
    fs.mkdirSync(dirImages);
}


const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads');
    },
    filename: (req, file, cb) => {
        
        const fullName = uuid() + file.originalname.substring(file.originalname.indexOf('.'), file.originalname.length);
        cb(null, fullName);
    }
})
const upload = multer({ storage });

var diagnosis = "";
    
fs.readdir(path.join(__dirname, 'public/images'), (err, files) => {
    if (err) throw err;

    for (const file of files) {
        fs.unlink(path.join(path.join(__dirname, 'public/images'), file), err => {
        if (err) throw err;
        });
    }
    });



    const images = [];
app.route("/")
.get((req, res) => {
    images.pop();
    fs.readdir(path.join(__dirname, 'uploads'), (err, files) => {
        if (err) throw err;

        for (const file of files) {
            fs.unlink(path.join(path.join(__dirname, 'uploads'), file), err => {
            if (err) throw err;
            });
        }
        });


    const directoryPath = path.join(__dirname, 'public/images');
    
    fs.readdir(directoryPath, function (err, files) {
        if (err) {
            return err;
        } 
        
        files.forEach(function (file) {           
            images.push(file);
        });
    
        
        res.render("index", {
            diagnosis: diagnosis,
            images: images
        });
    });

    
})
.post(upload.single("avatar"), async (req, res) => {
    fs.readdir(path.join(__dirname, 'public/images'), (err, files) => {
        if (err) throw err;
    
        for (const file of files) {
            fs.unlink(path.join(path.join(__dirname, 'public/images'), file), err => {
            if (err) throw err;
            images.pop();
            });
        }
        });
    
        
    
    fileName = req.file.filename;
    const brightness = (parseInt(req.body.brightness) + 255).toString();
    const contrast = (parseInt(req.body.contrast) + 127).toString();
    const processValue = req.body.secenekler;
    
    const python = await spawn("python", ["script2.py",fileName.toString(), processValue, brightness, contrast]);
 
    python.stdout.on('data', function (data) {
    
    
    diagnosis = data.toString();
    });
    python.on('close', (code) => {
    

    res.redirect("/");
    });
    
    
});

let port = process.env.PORT;
if (port == null || port == "") {
    port = 3000;
}

app.listen(port, () => console.log("App is listening"));
