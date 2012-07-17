
var titleTemplate = '' +
    '<div id="stackdoc-title">' +
    '   {{count}} Stack Overflow question{{^count_is_one}}s{{/count_is_one}}' +
    '</div>';

function getCanonical() {
    var matches = document.location.pathname.match(/\/kb\/(\w+)/);
    if(matches) return matches[1];
}

stackdoc.fetchData("microsoftkb", getCanonical(), function(data, renderedList) {
    var titleText = Mustache.render(titleTemplate, {count: data.length, count_is_one: data.length === 1}),
        $sd = $(titleText),
        $sdTitle = $($.grep($sd, function(x) { return x.id === "stackdoc-title"; })[0]);

    if(data.length > 0) {
        $sdTitle.popover({
            content: renderedList,
            classes: "large"
        }).addClass("clickable");
    }

    $sd.insertAfter($("#mt_article_properties"));
});
