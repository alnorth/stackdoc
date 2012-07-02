
var titleTemplate = '' +
    '<div id="stackdoc-title">' +
    '   {{count}} Stack Overflow question{{^count_is_one}}s{{/count_is_one}}' +
    '</div>';

function getCanonical() {
    var c = $('link[rel="canonical"]').attr('href'),
        matches = /http:\/\/api\.jquery\.com\/([.\-a-zA-Z0-9]+)\/?/.exec(c);

    if(matches) {
        return matches[1];
    } else {
        return null;
    }
}

stackdoc.fetchData("jquery", getCanonical(), function(data, renderedList) {
    var titleText = Mustache.render(titleTemplate, {count: data.length, count_is_one: data.length === 1}),
        $sd = $(titleText),
        $sdTitle = $($.grep($sd, function(x) { return x.id === "stackdoc-title"; })[0]);

    if(data.length > 0) {
        $sdTitle.popover({
            content: renderedList,
            classes: "large"
        }).addClass("clickable");
    }

    $(".entry-title").prepend($sd);
});
