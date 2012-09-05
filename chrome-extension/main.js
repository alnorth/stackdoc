var stackdoc = (function() {
    var module = {};

    var dataApiHostName = "stackdocapi.alnorth.com";
    // Uncomment this for testing on a local database
    //var dataApiHostName = "localhost:8080";

    var sdTemplate = '' +
        '<table class="stackdoc">' +
        '{{#questions}}' +
        '   <tr>' +
        '       <td><span class="sd_score {{#accepted_answer}}sd_accepted{{/accepted_answer}}">{{score}}</span></td>' +
        '       <td class="stackdoc-question-title"><a href="{{url}}" title="{{answers}} answers{{#accepted_answer}}, with one accepted answer{{/accepted_answer}}">{{title}}</a></td>' +
        '   </tr>' +
        '{{/questions}}' +
        '</table>';

    var titleTemplate = '' +
        '<div id="stackdoc-title">' +
        '   {{count}} Stack Overflow question{{^count_is_one}}s{{/count_is_one}}' +
        '</div>';

    function url(namespace, id) {
        return "http://" + dataApiHostName + "/1/" + encodeURIComponent(namespace) + "/" + encodeURIComponent(id);
    }

    function compareQuestions(a, b) {
        return b.score - a.score;
    }

    module.fetchData = function(namespace, id, callback) {
        if(id) {
            $.getJSON(url(namespace, id), function(data) {
                data.sort(compareQuestions);
                var renderedList = Mustache.render(sdTemplate, {questions: data}),
                    titleText = Mustache.render(titleTemplate, {count: data.length, count_is_one: data.length === 1}),
                    $sd = $(titleText);

                if(data.length > 0) {
                    $sd.popover({
                        content: renderedList,
                        classes: "large"
                    }).addClass("clickable");
                }

                callback($sd);
            });
        }
    }

    return module;
}());
