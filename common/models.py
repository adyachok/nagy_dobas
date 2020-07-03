from dataclasses import dataclass, field
from datetime import datetime
from time import time
from typing import List

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Translation:
    translation: str
    part_of_speech: str = ''
    transcript: List[str] = field(default_factory=list)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class WordMetadata:
    foreign_word: str
    test: str = ''
    translations: List[Translation] = field(default_factory=list)
    usage: List[str] = field(default_factory=set)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SkovorodaDict:
    name: str               # "Petra's dict 2"
    description: str        # "Useful Hungarian words",
    language: str           # "Hungarian",
    date_created: str  = datetime.now().strftime('%d-%m-%Y %H:%S')  # "28-05-2020 15:15",
    words: List[WordMetadata] = field(default_factory=list)

# MARK: This models represent Kindle DB structure
@dataclass_json
@dataclass
class Word:
    id: str
    word: str
    stem: str
    lang: str
    timestamp: int = time()
    usage: List[str] = field(default_factory=list)

    @staticmethod
    def from_db_tupple(db_tupple):
        return Word(id=db_tupple[0], word=db_tupple[1],
                    stem=db_tupple[2], lang=db_tupple[3],
                    timestamp=db_tupple[5])


@dataclass_json
@dataclass
class Lookup:
    id: str
    word_key: str
    book_key: str
    dict_key: str
    pos: int
    usage: str
    timestamp: int