var mongo = require("mongodb"),
    Server = mongo.Server,
    Db = mongo.Db,
    http = require("http");

var server = new Server("localhost", 27017, {auto_reconnect: true});
var db = new Db("stack_doc", server);

var port = process.argv[2] || 8000;

db.open(function(err, db) {
    if(!err) {

        http.createServer(function (req, res) {
            console.log(req.url);

        }).listen(port);

    } else {
        console.log("MongoDB error", err);
    }
});

