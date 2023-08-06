# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bibelen']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'html5lib>=1.1,<2.0',
 'requests>=2.28.1,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'bibelen',
    'version': '0.1.3',
    'description': 'Scrape norwegian Bibles on Youversion website and generate a Logos compatible format',
    'long_description': ' I\'m trying to make the code:\n\n1. Scrape the Bible text off bible.com for any defined Bible translation.\n\u2002\u2002\u2002\u2002\u2002\u2002The URL for the Bible text is: https://www.bible.com/no/bible/"+TRANSLATION_NUMBER+"/"+BOOK+"."+CHAPTER+".nb"\n\u2002\u2002\u2002\u2002\u2002\u2002The translation number defines which translation is used.  E.g. the Norwegian 1988 translation is version number 102.\n\u2002\u2002\u2002\u2002\u2002\u2002The Bible book is a three-letter abbreviation for the book.  The abbreviations used on the site are defined in the array "booklist" (not to be confused with bbooklist, which are the abbreviations used on Logos)\n\n2. Separate out just the text - remove all HTML tags, and add Logos program tags.\n\u2002\u2002\u2002\u2002\u2002\u2002The information on Logos formatting is found on https://wiki.logos.com/Personal_Books\n\u2002\u2002\u2002\u2002\u2002\u2002What is needed here is basically the "field on/off:bible" and Bible verse link.  For instance, in John 1:1, you might get:\n\n\u2002\u2002\u2002\u2002\u2002\u2002{{field-off:bible}}\n\u2002\u2002\u2002\u2002\u2002\u2002KAPITTEL 1\n[[@BibleNO2011:jn 1:1]]  1 {{field-on:bible}}I begynnelsen var Ordet, og Ordet var hos Gud, og Ordet var Gud. {{field-off:bible}}\n\n\u2002\u2002\u2002\u2002\u2002\u2002For the Bible verse link in Logos, the syntax is: [[@Bible "TRANSLATION" : "BOOK" "CHAPTER":"VERSE"]]\n\u2002\u2002\u2002\u2002\u2002\u2002The Bible book abbreviations in Logos are different than the ones used on bible.com, and are found in the list "bbooklist".\n\nI\'m attaching my awesome code.\n\nThanks - this will make studying the Bible much easier both for me, and for many other pastors and Bible students in Norway.\n',
    'author': 'Paul Mairo',
    'author_email': 'herrmpr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
