
var titleTemplate = '' +
    '<div id="stackdoc-title">' +
    '   {{count}} Stack Overflow question{{^count_is_one}}s{{/count_is_one}}' +
    '</div>';

function getPepNo() {
    return document.location.pathname.match(/[0-9]+/)[0];
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

    $("#contents").prepend($sd);
});

console.log(getPepNo());
