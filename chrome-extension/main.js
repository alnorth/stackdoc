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
        '       <td class="stackdoc-question-title"><a class="stackdoc-question-link" href="{{url}}" title="{{answers}} answers{{#accepted_answer}}, with one accepted answer{{/accepted_answer}}">{{title}}</a></td>' +
        '   </tr>' +
        '{{/questions}}' +
        '</table>';

    var titleTemplate = '' +
        '<div id="stackdoc-title">' +
        '   {{count}} Stack Overflow question{{^count_is_one}}s{{/count_is_one}}' +
        '</div>';

    var pageIndex = 1; // Used to differentiate multiple StackDoc inserts on the same page.

    function url(namespace, id) {
        return "http://" + dataApiHostName + "/1/" + encodeURIComponent(namespace) + "/" + encodeURIComponent(id);
    }

    function compareQuestions(a, b) {
        return b.score - a.score;
    }

    function trackEvent(id, eventType) {
        chrome.extension.sendRequest({gaEvent: {id: id, eventType: eventType}});
    }

    function getQuestionTrackFn(i) {
        return function() {
            trackEvent("question-link-" + (i + 1), "clicked");
        };
    }

    module.fetchData = function(namespace, id, callback) {
        if(id) {
            $.getJSON(url(namespace, id), function(data) {
                data.sort(compareQuestions);
                var renderedList = Mustache.render(sdTemplate, {questions: data}),
                    titleText = Mustache.render(titleTemplate, {count: data.length, count_is_one: data.length === 1}),
                    $sd = $(titleText),
                    thisIndex = pageIndex;

                pageIndex++;

                if(data.length > 0) {
                    $sd.popover({
                        content: renderedList,
                        classes: "large stackdoc-popover-" + thisIndex
                    }).addClass("clickable");

                    // Add events for Google Analytics tracking
                    trackEvent(namespace, "loaded");

                    $sd.click(function() {
                        trackEvent(namespace, "clicked");

                        var questionLinks = $(".stackdoc-popover-" + thisIndex + " .stackdoc-question-link");
                        for(var i = 0; i < questionLinks.length; i++) {
                            $(questionLinks[i]).click(getQuestionTrackFn(i));
                        }
                    });
                }

                callback($sd);
            });
        }
    }

    return module;
}());
