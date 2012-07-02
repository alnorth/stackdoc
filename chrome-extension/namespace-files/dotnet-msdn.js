
var msdnSurrounding = '' +
    '<div class="cl_lw_vs_seperator" style="display: block; "></div>' +
    '<div id="stackdoc-title">' +
    '   {{count}} Stack Overflow question{{^count_is_one}}s{{/count_is_one}}' +
    '</div>';

function getCanonical() {
    var className = $('link[rel="canonical"]').attr('href');
    // Remove the hostname and first part of the path.
    className = className.replace(/^.*\//, "");
    // Remove the aspx extension and optional bits on the end of the class name like "_events".
    className = className.replace(/(_[a-z]+)?(\(v=vs\.\d+\))?(\(v=sql\.\d+\))?\.aspx$/, "");

    return className;
}

stackdoc.fetchData("dotnet", getCanonical(), function(data, renderedList) {
    var fullText = Mustache.render(msdnSurrounding, {count: data.length, count_is_one: data.length === 1}),
        $sd = $(fullText),
        $sdTitle = $($.grep($sd, function(x) { return x.id === "stackdoc-title"; })[0]);

    if(data.length > 0) {
        $sdTitle.popover({
            content: renderedList,
            classes: "large"
        }).addClass("clickable");
    }

    $sd.insertAfter($("#vsPanel"));
});
