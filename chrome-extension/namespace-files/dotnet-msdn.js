
function getCanonical() {
    var className = $('link[rel="canonical"]').attr('href');
    // Remove the hostname and first part of the path.
    className = className.replace(/^.*\//, "");
    // Remove the aspx extension and optional bits on the end of the class name like "_events".
    className = className.replace(/(_[a-z]+)?(\(v=vs\.\d+\))?(\(v=sql\.\d+\))?\.aspx$/, "");

    return className;
}

stackdoc.fetchData("dotnet", getCanonical(), function($sd) {
    var after = $("#vsPanel").length > 0 ? $("#vsPanel") : $("#curversion");
    if(after.length > 0) {
        var sep = $('<div class="cl_lw_vs_seperator" style="display: block; "></div>');
        sep.insertAfter(after);
        $sd.insertAfter(sep);
    } else {
        // When those two elements aren't visible we insert the title on a line of its own.
        $sd.insertAfter($("h1.title"));
    }
});
