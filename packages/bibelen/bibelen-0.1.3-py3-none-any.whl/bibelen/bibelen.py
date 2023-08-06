"""
Scrape all the norwegian Bibles on https://www.bible.com/no/bible/
 and return them in a Logos https://www.logos.com/ compatible format
"""

# bibelen: Scrape norwegian Bibles on Youversion website and generate
# a Logos compatible format
#
# Copyright (C) 2022 Paul Mairo <github@rmpr.xyz>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from bs4 import BeautifulSoup
from tqdm.contrib.concurrent import process_map
from dataclasses import dataclass, field
from datetime import datetime
import re
import requests
import string


@dataclass
class Translation:
    name: str
    code: int
    has_old_testament: bool = True
    language: str = "NO"


@dataclass
class _Book:
    name: str
    number_of_chapters: int
    logos_name: str
    chapters: list[list[str]] = field(default_factory=list)

    def chapter(self, number) -> list[str]:
        if 0 < number <= self.number_of_chapters:
            return self.chapters[number - 1]
        raise RuntimeError(
            f"Invalid chapter number, {self.name} only has {self.number_of_chapters} chapters"
        )


class Bible:
    def __init__(self, translation: Translation):
        self._base_url = "https://www.bible.com/bible/"
        self._translation = translation
        self.new_testament: list[_Book] = [
            _Book("mat", 28, "mt"),
            _Book("MRK", 16, "mk"),
            _Book("luk", 24, "lk"),
            _Book("JHN", 21, "jn"),
            _Book("act", 28, "acts"),
            _Book("rom", 16, "rom"),
            _Book("1co", 16, "1cor"),
            _Book("2co", 13, "2cor"),
            _Book("gal", 6, "gal"),
            _Book("eph", 6, "eph"),
            _Book("PHP", 4, "phil"),
            _Book("col", 4, "col"),
            _Book("1th", 5, "1th"),
            _Book("2th", 3, "2th"),
            _Book("1ti", 6, "1tim"),
            _Book("2ti", 4, "2tim"),
            _Book("tit", 3, "tit"),
            _Book("phm", 1, "phm"),
            _Book("heb", 13, "heb"),
            _Book("JAS", 5, "james"),
            _Book("1pe", 5, "1pet"),
            _Book("2pe", 3, "2pet"),
            _Book("1JN", 5, "1jn"),
            _Book("2JN", 1, "2jn"),
            _Book("3JN", 1, "3jn"),
            _Book("jud", 1, "jd"),
            _Book("rev", 22, "rev"),
        ]
        if self._translation.has_old_testament:
            self.old_testament: list[_Book] = [
                _Book("gen", 50, "gen"),
                _Book("exo", 40, "ex"),
                _Book("lev", 27, "lev"),
                _Book("num", 36, "num"),
                _Book("deu", 34, "deut"),
                _Book("jos", 24, "josh"),
                _Book("jdg", 21, "judg"),
                _Book("rut", 4, "ruth"),
                _Book("1sa", 31, "1sam"),
                _Book("2sa", 24, "2sam"),
                _Book("1ki", 22, "1ki"),
                _Book("2ki", 25, "2ki"),
                _Book("1ch", 29, "1chr"),
                _Book("2ch", 36, "2chr"),
                _Book("ezr", 10, "ezra"),
                _Book("neh", 13, "neh"),
                _Book("est", 10, "est"),
                _Book("job", 42, "job"),
                _Book("psa", 150, "ps"),
                _Book("pro", 31, "prov"),
                _Book("ecc", 12, "ecc"),
                _Book("SNG", 8, "song"),
                _Book("isa", 66, "isa"),
                _Book("jer", 52, "jer"),
                _Book("lam", 5, "lam"),
                _Book("EZK", 48, "ezek"),
                _Book("dan", 12, "dan"),
                _Book("hos", 14, "hos"),
                _Book("JOL", 3, "joel"),
                _Book("amo", 9, "amos"),
                _Book("oba", 1, "obad"),
                _Book("jon", 4, "jonah"),
                _Book("mic", 7, "mic"),
                _Book("NAM", 3, "nah"),
                _Book("hab", 3, "hab"),
                _Book("zep", 3, "zeph"),
                _Book("hag", 2, "hag"),
                _Book("zec", 14, "zech"),
                _Book("mal", 4, "mal"),
            ]
        else:
            self.old_testament = []

    @property
    def translation(self) -> int:
        return self._translation

    @translation.setter
    def translation(self, translation: Translation):
        self._translation = translation

    def scrape_book(self, book: _Book) -> tuple[str, list[list[str]]]:
        def _clean_verses(chapter_text: str) -> str:
            cleaned_verses: list = []
            chapter_text_cleaned = chapter_text.replace("\n", "")
            chapter_text_cleaned = chapter_text_cleaned.replace("(-)", "-")
            verses = re.split(r"\d+", chapter_text_cleaned)
            for verse in verses:
                clean_verse = verse.strip()
                if clean_verse in f"{string.whitespace}{string.punctuation}":
                    continue
                cleaned_verses.append(clean_verse)
            return cleaned_verses

        chapters: list[list[str]] = []
        for i in range(book.number_of_chapters):
            request = requests.get(
                f"{self._base_url}{self._translation.code}/{book.name}.{i+1}"
            )
            soup = BeautifulSoup(request.text, "html.parser")
            for element in soup.findAll("span", "note"):
                element.decompose()
            chapter_text: str = ""
            for element in soup.findAll("div", "p"):
                chapter_text = f"{chapter_text}{element.get_text()}"
            chapters.append(_clean_verses(chapter_text))
        return chapters

    def scrape_all(self) -> None:
        result = process_map(
            self.scrape_book,
            self.new_testament + self.old_testament,
            desc=f"Fetching {self.translation.name}",
        )
        for i in range(len(self.new_testament)):
            self.new_testament[i].chapters = result[i]
        for i in range(len(self.new_testament), len(result)):
            self.old_testament[i - len(self.new_testament)].chapters = result[i]

    def book(self, number: int) -> _Book:
        if not 0 < number <= 66:
            raise IndexError("Invalid number, remember, the Bible has 66 books")
        if number > 39:
            return self.new_testament[number - 40]
        if number <= 39 and self.translation.has_old_testament:
            return self.old_testament[number - 1]
        raise RuntimeError(f"{self.translation} doesn't have OT")

    def save_to_logos(self) -> None:
        def _line_prefix(
            book_name: str,
            chapter_num: int,
            verse_num: int,
            logos_translation: str = "NO2011",
        ) -> str:
            return f"[[@Bible{logos_translation}:{book_name} {chapter_num}:{verse_num}]]  {verse_num} "

        def _line_suffix(verse: str) -> str:
            return f"{{{{field-on:bible}}}}{verse}{{{{field-off:bible}}}}\n"

        def _chapter_separator(num: int, language: str = "NO"):
            title: str = "KAPITTEL"
            if language == "NO":
                return f"\n{title} {num}{{{{field-on:bible}}}}{{{{field-off:bible}}}}\n"
            else:
                raise RuntimeError(f"Language {language} not supported")

        with open(
            f"{self.translation.name}{self.translation.code}{datetime.now()}.txt", "w"
        ) as bible_file:
            lines = ["{{field-off:bible}}\n"]
            for book in self.old_testament + self.new_testament:
                for i, chapter in enumerate(book.chapters, start=1):
                    lines.append(f"{_chapter_separator(i)}")
                    for j, verse in enumerate(chapter, start=1):
                        lines.append(
                            f"{_line_prefix(book.logos_name, i, j)}"
                            f"{_line_suffix(verse)}"
                        )
            bible_file.writelines(lines)
