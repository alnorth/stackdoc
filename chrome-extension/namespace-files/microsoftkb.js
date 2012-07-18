
function getCanonical() {
    var matches = document.location.pathname.match(/\/kb\/(\w+)/);
    if(matches) return matches[1];
}

stackdoc.fetchData("microsoftkb", getCanonical(), function($sd) {
    $sd.insertAfter($("#mt_article_properties"));
});
