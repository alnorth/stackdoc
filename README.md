# StackDoc #

**Note: These instructions are currently incomplete, check back later for full details**

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

The big thing that you'll need before you can start work is a copy of a Stack Overflow data dump. These dumps are currently available as [torrents from ClearBits](http://www.clearbits.net/creators/146-stack-exchange-data-dump). They are quite large. Once you've downloaded this you need to decompress a copy of the `posts.xml` file from the Stack Overflow data. You can throw everything else away.

For working with the database update script you'll need **Python**, **virtualenv** and **MongoDB** installed. For the Chrome extension you'll need **Chrome/Chromium**, but if you're interested in this extension you've probably got this already.

And, of course, you'll need a clone of the StackDoc repository.


## License ##

Unless otherwise stated in comments, files included in this project are provided under the Modified BSD License as described in LICENSE.txt.
