 I'm trying to make the code:

1. Scrape the Bible text off bible.com for any defined Bible translation.
      The URL for the Bible text is: https://www.bible.com/no/bible/"+TRANSLATION_NUMBER+"/"+BOOK+"."+CHAPTER+".nb"
      The translation number defines which translation is used.  E.g. the Norwegian 1988 translation is version number 102.
      The Bible book is a three-letter abbreviation for the book.  The abbreviations used on the site are defined in the array "booklist" (not to be confused with bbooklist, which are the abbreviations used on Logos)

2. Separate out just the text - remove all HTML tags, and add Logos program tags.
      The information on Logos formatting is found on https://wiki.logos.com/Personal_Books
      What is needed here is basically the "field on/off:bible" and Bible verse link.  For instance, in John 1:1, you might get:

      {{field-off:bible}}
      KAPITTEL 1
[[@BibleNO2011:jn 1:1]]  1 {{field-on:bible}}I begynnelsen var Ordet, og Ordet var hos Gud, og Ordet var Gud. {{field-off:bible}}

      For the Bible verse link in Logos, the syntax is: [[@Bible "TRANSLATION" : "BOOK" "CHAPTER":"VERSE"]]
      The Bible book abbreviations in Logos are different than the ones used on bible.com, and are found in the list "bbooklist".

I'm attaching my awesome code.

Thanks - this will make studying the Bible much easier both for me, and for many other pastors and Bible students in Norway.
