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

            // Paths like /1/dotnet/system.console.writeline
            var regex = /^\/1\/([a-zA-Z]+)\/([.a-zA-Z0-9_]+)\/?$/,
                matches = regex.exec(req.url);

            if(matches) {
                var language = matches[1],
                    canonical = matches[2];

                db.collection("posts", function(err, posts) {
                    if(!err) {
                        var query = {};
                        query[language + ".page_ids"] = canonical;
                        posts.find(query).toArray(function(err, matchingPosts) {
                            console.log(matchingPosts);
                        });
                    } else {
                        console.log("MongoDB error", err);
                    }
                });
            }

        }).listen(port);

    } else {
        console.log("MongoDB error", err);
    }
});

