
function getCanonical() {
    var matches = document.location.pathname.match(/\/(?:javase|j2se|javaee|j2ee)\/\d(?:\.\d)*\/docs\/api\/(\w+(?:\/\w+)*)\.html/);
    if(matches) return matches[1].replace(/\//g, ".");
}

stackdoc.fetchData("java", getCanonical(), function($sd) {
    $sd.insertAfter($("body h2"));
});
