guardian-crossword-scraper
==========================

A scraper of _The Guardian_'s Crosswords, served in an API-like manner.

The magic sauce is in `parser.py`. You can call it directly to test with a given Guardian Crossword

It uses Flask to serve the crossword as XML- handily to almost the same spec as some of the endpoints (eg USA Today) called from the [Words with Crosses Android App](https://github.com/adamantoise/wordswithcrosses). 

Thanks to Chris Browne and Ethan Haley for helping me make sense of this very _soupy_ page of HTML.

##Third Party Libraries Used
* [Flask](http://flask.pocoo.org/)
* [Requests](http://docs.python-requests.org/en/latest/)
* [lxml](http://lxml.de/)
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
* [TinyCSS](https://pythonhosted.org/tinycss/)
