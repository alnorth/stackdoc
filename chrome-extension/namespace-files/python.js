
var sections = $(".body > .section");

if(sections.length > 0) {
    var section = sections[0],
        id = null;

    if(section.id.indexOf("module-") === 0) {
        id = section.id.replace("module-", "");
    } else if(section.id === "built-in-functions") {
        id = "functions";
    }

    stackdoc.fetchData("python", id, function($sd) {
        $sd.insertAfter($(section).children("h1"));
    });
}
