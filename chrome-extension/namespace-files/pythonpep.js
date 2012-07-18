
function getPepNo() {
    var matches = document.location.pathname.match(/[0-9]+/);
    if(matches) return matches[0];
}

stackdoc.fetchData("pythonpep", getPepNo(), function($sd) {
    $sd.insertAfter($("#content table.rfc2822"));
});
