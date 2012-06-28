var stackdoc = (function() {
	var module = {};

	var sdTemplate = '' +
		'<table class="stackdoc">' +
		'{{#questions}}' +
		'	<tr>' +
		'		<td><span class="sd_score {{#accepted_answer}}sd_accepted{{/accepted_answer}}">{{score}}</span></td>' +
		'		<td class="stackdoc-question-title"><a href="{{url}}" title="{{answers}} answers{{#accepted_answer}}, with one accepted answer{{/accepted_answer}}">{{title}}</a></td>' +
		'	</tr>' +
		'{{/questions}}' +
		'</table>';

	function url(namespace, id) {
		return "http://stackdocapi.alnorth.com/1/" + encodeURIComponent(namespace) + "/" + encodeURIComponent(id);
	}

	function compareQuestions(a, b) {
		return b.score - a.score;
	}

	module.fetchData = function(namespace, id, callback) {
		$.getJSON(url(namespace, id), function(data) {
			data.sort(compareQuestions);
			var renderedList = Mustache.render(sdTemplate, {questions: data});

			callback(data, renderedList);
		});
	}

	return module;
}());
