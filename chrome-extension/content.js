
// Templates
var sdTemplate = '' +
	'<table class="stackdoc">' +
	'{{#questions}}' +
	'	<tr>' +
	'		<td><span class="sd_score {{#accepted_answer}}sd_accepted{{/accepted_answer}}">{{score}}</span></td>' +
	'		<td class="stackdoc-question-title"><a href="{{url}}" title="{{answers}} answers{{#accepted_answer}}, with one accepted answer{{/accepted_answer}}">{{title}}</a></td>' +
	'	</tr>' +
	'{{/questions}}' +
	'</table>';
var msdnSurrounding = '' +
	'<div class="cl_lw_vs_seperator" style="display: block; "></div>' +
	'<div id="stackdoc-title">' +
	'	{{count}} Stack Overflow questions' +
	'</div>';

var className = $('link[rel="canonical"]').attr('href');
// Remove the hostname and first part of the path.
className = className.replace(/^.*\//, "");
// Remove the aspx extension and optional bits on the end of the class name like "_events".
className = className.replace(/(_[a-z]+)?\.aspx$/, "");

var shortId = $('meta[name="Search.ShortId"]').attr('content');

function url(language, id) {
	return "http://stackdocapi.alnorth.com/1/" + encodeURIComponent(language) + "/" + encodeURIComponent(id);
}

function compareQuestions(a, b) {
	return b.score - a.score;
}

$.getJSON(url("dotnet", className), function(data) {
	data.sort(compareQuestions);
	var sdText = Mustache.render(sdTemplate, {questions: data}),
		fullText = Mustache.render(msdnSurrounding, {count: data.length}),
		$sd = $(fullText),
		$sdTitle = $($.grep($sd, function(x) { return x.id === "stackdoc-title"; })[0]);

	if(data.length > 0) {
		$sdTitle.popover({
			content: sdText,
			classes: "large"
		});
	}

	$sd.insertAfter($("#vsPanel"));
});
