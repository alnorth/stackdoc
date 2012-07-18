# StackDoc #

StackDoc is a Chrome extension that inserts lists of Stack Overflow questions into online documentation. It's [available in the Chrome webstore](https://chrome.google.com/webstore/detail/hfdanbnpljnbncjbdcbmbieeoicdlhbe) if you would simply like to use it. The rest of this document is aimed at those that would like to extend it.

StackDoc currently supports a handful of different online documentation websites. These are the main ones that I use day to day, that's why I added them first. If you'd like your favourite language or library to be included then your best bet is to add support for it yourself. I've tried to make this as simple as possible.


## A brief overview ##

There are three parts to StackDoc:

* **chrome-extension** - This are the files that get uploaded to the Chrome webstore, and that users download and install.
* **data-api** - This is a node.js web service that serves data to the Chrome extension.
* **update-database** - This is a Python script that keeps the database on the server up to date.

In order to add support for an extra language you will need to extend the database update script and the Chrome extension. This is so that StackDoc can find references to language elements in questions, and then insert data about them into documentation websites.


## Setting up your development environment ##


## License ##

Unless otherwise stated in comments, files included in this project are provided under the Modified BSD License as described in LICENSE.txt.
