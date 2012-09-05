# StackDoc #

StackDoc is a Chrome extension that inserts lists of Stack Overflow questions into online documentation. It's [available in the Chrome webstore](https://chrome.google.com/webstore/detail/hfdanbnpljnbncjbdcbmbieeoicdlhbe) if you would simply like to use it. The rest of this document is aimed at those that would like to extend it.

StackDoc currently supports a handful of different online documentation websites. These are the main ones that I use day to day, that's why I added them first. If you'd like your favourite language or library to be included then your best bet is to add support for it yourself. I've tried to make this as simple as possible.


## A brief overview ##

There are three parts to StackDoc:

* **chrome-extension** - This are the files that get uploaded to the Chrome webstore, and that users download and install.
* **data-api** - This is a node.js web service that serves data to the Chrome extension.
* **update-database** - This is a Python script that keeps the database on the server up to date. It starts by parsing a file from one of the Stack Overflow data dump and then uses the API to keep up to date.

In order to add support for an extra language you will need to extend the database update script and the Chrome extension. This is so that StackDoc can find references to language elements in questions, and then insert data about them into documentation websites.


## Setting up your development environment ##

*These instructions are written with Linux in mind. As a result they may well work fine on OS X but require some tweaking for Windows. Let me know how you get on.*

For working with the database update script you'll need **Python**, **virtualenv** and **MongoDB** installed. In order to run the data API locally you'll need **node**. For the Chrome extension you'll need **Chrome/Chromium**, but if you're interested in this extension you've probably got this already.

And, of course, you'll need a clone of the StackDoc repository.

The other big thing that you'll need before you can start work is a set of Stack Overflow data. On the live server StackDoc uses the script in [stack-db](https://github.com/alnorth29/stack-db) to keep a full database of questions and answers up to date. For development you don't need all this, you just need a sample of the database. You should download a [database dump](http://files.alnorth.com/so/sample.7z) containing about 10% of questions. Unzip this and then import it into MongoDB with the following command:

    mongoimport -d stackdb -c questions --file sample.json


### Running the database update script ###

In the update-database directory you'll find a script called `update-database.sh`. This is the actual script that gets run on the server. As you can see, all it does is create a virtual environment, install the required libraries and run the python script `update-database.py`. It also cleans up the virtual environment once it's done. You could run this script every time you want to update the database but you'll probably get irritated with how long it takes to install the libraries.

You can set up an equivalent environment with this code:

    cd update-database
    virtualenv venv
    venv/bin/pip install -r requirements.txt
    venv/bin/python update-database.py

That last line will start processing SO question data. The first time it runs it will process the whole database. If that completes successfully then it will only process newly added questions next time round. That's unless the questions processors change. Feel free to stop it with Ctrl + C at any point, it should recover fine.


### Running the API server ###

When you've got data being imported you'll want it to be visible in your copy of the Chrome extension. This is only going to happen if your Chrome extension is getting data from your local database. For this to happen you need to set up and run the data API.

    cd data-api
    npm install
    node main.js 8080


### Installing a test version of the Chrome extension ###

Go to [chrome://chrome/extensions/](chrome://chrome/extensions/) and switch on "Developer mode" (top right). Now click on "Load unpacked extension..." and select the chrome-extension directory. Every time you make changes to the extension files you'll need to come to this page and click on "Reload".

While you're here you might want to disable the official version of the extension so you don't have both running at the same time.

You also need to set your installed copy to take data from your local database. To do this uncomment the line at the top of chrome-extension/main.js.


## Extending StackDoc ##

I've tried to make this whole process as easy as I can. If you've got any ideas of how to make it easier or better then do let me know.


### Pick a namespace ###

In the StackDoc database questions are categorised into namespaces. For example, questions about .NET code are in the `dotnet` namespace. A full list of the namespaces currently in use can be found [in the wiki](https://github.com/alnorth29/stackdoc/wiki/Namespaces).

You need to decide on a namespace name for the library you're adding support for. This name must be entirely lower case characters, no digits or punctuation are allowed.


### Decide how you're going to represent packages/classes/functions ###

Individual elements of the library should have a unique, canonical representation. This will normally just follow the package/namespace hierarchy, but occaisionally it's more subtle. It'll make life easier if you can determine this canonical ID from the URL of its page in the documentation, for example `http://msdn.microsoft.com/en-us/library/system.console.writeline(v=vs.110).aspx` --> `system.console.writeline`.

These canonical IDs should all match the regex `[.a-zA-Z0-9_\-]+` (i.e. characters, digits, dots, dashes and underscores). They will be lower-cased before being used in comparisons.


### Extend the database processor ###

In update-database/stackdoc/namespaces you'll find a python file for each namespace. Create one for your namespace and implement the functions below. If you'd like an example to work from then `pythonpep.py` is a pretty simple one.

#### get_version() ####
This should return an integer which acts as a version number for your file. Increment this whenever you make changes that will return better results. The update script uses these version numbers to determine whether it needs to process the whole question database again. They are only recorded once it has finished processing a full import, so you don't need to increment this if you stopped the update script before that point.

#### get_ids(title, body, tags) ####
* `title` - a string containing the title of the question.
* `body` - a string containing the HTML content a question or an answer.
* `tags` - a list of strings. The tags applied to this particular question.

This should return a list of the canonical IDs that you've found in the text.

All the processors so far work by looking for URLs in the question body and extracting IDs from them, and that's a good start. Have a look at how the current processors do it and then have a go yourself. Keep in mind that there may be several different URL structures that point to the same page. For example, all these URLs lead to the same article:

* http://support.microsoft.com/kb/836436
* http://support.microsoft.com/?id=836436
* http://support.microsoft.com/?kbid=836436
* http://support.microsoft.com/?scid=836436
* http://support.microsoft.com/?scid=KB;EN-US;836436
* http://support.microsoft.com/default.aspx?id=836436
* http://support.microsoft.com/default.aspx?kbid=836436
* http://support.microsoft.com/default.aspx?scid=836436
* http://support.microsoft.com/default.aspx?scid=KB;EN-US;836436

I've written a python script to help you find out what variants are used. It's in the scripts directory and it's called `urls-starting-with.py`. This script scans through questions in the question database and looks for URLs with a prefix you give it. An example call would be:

    python urls-starting-with.py http://support.microsoft.com/

This would help you find the URL forms shown above. You can then write a regex or some sort of URL parser to extract the canonical IDs from these URLs.

You should also be wary of hostname changes. For example, the docs at http://docs.oracle.com/ used to be at http://java.sun.com/.

Feel free to be a bit more sophisticated if you want and parse code or whatever, but do be careful not to introduce too many false positives.

#### get_tags() ####
This should return a list of the tags that might appear on questions relating to your library. This might be one or two like for the `jquery` namespace, or loads like the `dotnet` namespace. A question will only be passed to `get_ids` if it's tagged with at least one of the tags from `get_tags`.

Sometimes there's no reliable set of tags that can be used. This will probably only be the case with general support databases like Microsoft's Knowledge Base. In this case you should return `None`. I expect this will be very rare though.


### Extend the Chrome extension ###

In chrome-extension/namespace-files you'll find a JavaScript and CSS file for each documentation website that StackDoc supports. You'll need to create a pair for whatever website you'll be inserting data into. If there will be multiple websites for a namespace then use the namespace name, followed by a dash, followed by the name of the particular website.

Once you've created the files you need to update `manifest.json` so that the Chrome extension loads them on the correct site.

#### Creating the JavaScript file ####
The best thing to do here is to take a look at the existing files. They all do roughly the same thing.

    function getCanonical() {
        var matches = document.location.pathname.match(/\/(?:javase|j2se|javaee|j2ee)\/\d(?:\.\d)*\/docs\/api\/(\w+(?:\/\w+)*)\.html/);
        if(matches) return matches[1].replace(/\//g, ".");
    }

    stackdoc.fetchData("java", getCanonical(), function($sd) {
        $sd.insertAfter($("body h2"));
    });

- Work out the canonical ID of the language element described on this particular page. You might be able to do this by looking at the `document.location.pathname`, or by looking at the title of the page, etc.
- Pass it, along with the namespace name, to `stackdoc.fetchData`. Passing a `null` here is fine and will simply result in the callback not being fired, this is probably the easiest way for a script to handle being loaded on a page without a canonical ID.
- Insert the jQuery object that gets returned into an appropriate place on the page. This object will be a `div` containing text like "7 Stack Overflow questions". Clicking on this `div` will open a pop up containing a list of the questions. If there are no questions then clicking on the `div` will do nothing.

#### Creating the CSS file ####
You'll have inserted an element like this on to your page:

    <div id="stackdoc-title" class="clickable">
        4 Stack Overflow questions
    </div>

Now you need to style it. Use the CSS to position it correctly and make it fit into the page visually. We don't want this sticking out, but it should be easily visible near the top of the page.

If there are no questions (and clicking on the `div` will do nothing) then it will not have the `clickable` class.

#### Updating the manifest ####
For your JavaScript and CSS file to be loaded on the correct page you will need to tell Chrome to do so. This is done in the `manifest.json` file in the chrome-extension directory.

Add another entry to `content_scripts` like the existing ones. Please do this in alphabetical order of the JS and CSS file names. The rules for the patterns in `matches` can be seen in [Google's documentation](http://code.google.com/chrome/extensions/match_patterns.html).

You will also need to add your URL pattern to the array in the first `content_scripts` entry. This will tell Chrome to load the rest of the StackDoc code on your site. Again, please do this in alphabetical order of file name.


### Submit your pull request ###

That's it! You're done! Submit a pull request so I can add your code to the extension.

Fancy adding another namespace?


## License ##

Unless otherwise stated in comments, files included in this project are provided under the Modified BSD License as described in LICENSE.txt. This will also apply to any contributions accepted to this project.
