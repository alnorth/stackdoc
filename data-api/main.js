var mongo = require("mongodb"),
    Server = mongo.Server,
    Db = mongo.Db,
    http = require("http");

var server = new Server("localhost", 27017, {auto_reconnect: true});
var db = new Db("stack_doc", server);

var port = process.argv[2] || 8000;

function postListToArray(matchingPosts) {
    var a = [],
        i = 0;
    for(i = 0; i < matchingPosts.length; i++) {
        var q = matchingPosts[i];
        a.push({
            id: q["question_id"],
            url: q["url"],
            title: q["title"],
            score: q["score"],
            answers: q["answers"],
            accepted_answer: q["accepted_answer"]
        });
    }
    return a;
}

db.open(function(err, db) {
    if(!err) {

        http.createServer(function (req, res) {
            // Paths like /1/dotnet/system.console.writeline
            var regex = /^\/1\/([a-zA-Z]+)\/([.a-zA-Z0-9_]+)\/?$/,
                matches = regex.exec(req.url);

            if(matches) {
                var language = matches[1],
                    canonical = matches[2];

                db.collection("posts", function(err, posts) {
                    if(!err) {
                        var query = {};
                        query["page_ids." + language] = canonical;
                        posts.find(query).toArray(function(err, matchingPosts) {
                            var array = postListToArray(matchingPosts);
                            res.writeHead(200, {"Content-Type": "text/javascript"});
                            res.end(JSON.stringify(array));
                        });
                    } else {
                        console.log("MongoDB error", err);
                        res.writeHead(500, {"Content-Type": "text/javascript"});
                        res.end("Request error");
                    }
                });
            }

        }).listen(port);

    } else {
        console.log("MongoDB error", err);
    }
});

