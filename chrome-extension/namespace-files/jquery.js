
function getCanonical() {
    var c = $('link[rel="canonical"]').attr('href'),
        matches = /http:\/\/api\.jquery\.com\/([.\-a-zA-Z0-9]+)\/?/.exec(c);

    if(matches) {
        return matches[1];
    } else {
        return null;
    }
}

stackdoc.fetchData("jquery", getCanonical(), function($sd) {
    $(".entry-title").prepend($sd);
});
