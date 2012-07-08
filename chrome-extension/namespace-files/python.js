
var titleTemplate = '' +
    '<div id="stackdoc-title">' +
    '   {{count}} Stack Overflow question{{^count_is_one}}s{{/count_is_one}}' +
    '</div>';

$(".body > .section").each(function() {
    var id = this.id.replace("module-", ""),
        $this = $(this);

    if(id === "built-in-functions") {
        id = "functions";
    }

    stackdoc.fetchData("python", id, function(data, renderedList) {
        var titleText = Mustache.render(titleTemplate, {count: data.length, count_is_one: data.length === 1}),
            $sd = $(titleText),
            $sdTitle = $($.grep($sd, function(x) { return x.id === "stackdoc-title"; })[0]);

        if(data.length > 0) {
            $sdTitle.popover({
                content: renderedList,
                classes: "large"
            }).addClass("clickable");
        }

        $sd.insertAfter($this.children("h1"));
    });
})
