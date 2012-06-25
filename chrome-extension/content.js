
// Templates
var sdTemplate = '' +
	'<ul class="stackdoc">' +
	'{{#questions}}' +
	'	<li>' +
	'		<span class="sd_score {{#accepted_answer}}sd_accepted{{/accepted_answer}}">{{score}}</span>' +
	'		<a href="{{url}}" title="{{answers}} answers{{#accepted_answer}}, with one accepted answer{{/accepted_answer}}">{{title}}</a>' +
	'	</li>' +
	'{{/questions}}' +
	'</ul>';
var msdnSurrounding = '' +
	'<div>' +
	'	<div class="LW_CollapsibleArea_TitleDiv">' +
	'		<div>' +
	'			<a href="javascript:void(0)" class="LW_CollapsibleArea_TitleAhref" title="Collapse">' +
	'				<img src="http://i3.msdn.microsoft.com/Areas/Global/Content/clear.gif" class="cl_CollapsibleArea_expanding LW_CollapsibleArea_Img"' +
	'				><span class="LW_CollapsibleArea_Title">Stack Overflow</span>' +
	'			</a>' +
	'			<div class="LW_CollapsibleArea_HrDiv">' +
	'				<hr class="LW_CollapsibleArea_Hr">' +
	'			</div>' +
	'		</div>' +
	'	</div>' +
	'	<div class="sectionblock">' +
	'		<a id="stackDocToggle" xmlns="http://www.w3.org/1999/xhtml"></a>' +
	'		{{&sd}}' +
	'	</div>' +
	'</div>';

var maxDisplay = 7;

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
	console.log(data);
	data.sort(compareQuestions);
	var sdText = Mustache.render(sdTemplate, {questions: data.slice(0, maxDisplay)});
	$("#mainBody").append(Mustache.render(msdnSurrounding, {sd: sdText}));
});
