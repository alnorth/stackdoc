
var titleTemplate = '' +
    '<div id="stackdoc-title">' +
    '   {{count}} Stack Overflow question{{^count_is_one}}s{{/count_is_one}}' +
    '</div>';

function getPepNo() {
    var matches = document.location.pathname.match(/[0-9]+/);
    if(matches) return [0];
}

stackdoc.fetchData("pythonpep", getPepNo(), function(data, renderedList) {
    var titleText = Mustache.render(titleTemplate, {count: data.length, count_is_one: data.length === 1}),
        $sd = $(titleText),
        $sdTitle = $($.grep($sd, function(x) { return x.id === "stackdoc-title"; })[0]);

    if(data.length > 0) {
        $sdTitle.popover({
            content: renderedList,
            classes: "large"
        }).addClass("clickable");
    }

    $sd.insertAfter($("#content table.rfc2822"));
});
