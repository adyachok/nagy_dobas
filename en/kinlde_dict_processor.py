import json
import pathlib
import sqlite3

from common.stardict import translate_words
from common.models import SkovorodaDict, Word, Lookup


def extract_words_from_kindle_dict_db():
    words = []
    conn = sqlite3.connect('kindle_vocab.db')
    cursor = conn.execute("SELECT * FROM words")
    result = cursor.fetchall()
    for data in result:
        word = Word.from_db_tupple(data)
        cursor = conn.execute(
            f"SELECT * FROM lookups WHERE word_key = '{word.id}'")
        lookups_result = cursor.fetchall()
        for lookup_data in lookups_result:
            lookup = Lookup(*lookup_data)
            word.usage.append(lookup.usage)
        words.append(word)
    return words


if __name__ == '__main__':
    words = extract_words_from_kindle_dict_db()
    translated_words, not_translated = translate_words(words)
    # for word in translated_words:
    #     print(word.to_dict())
    sk_dict = SkovorodaDict(name='My Kidle English Words',
                            description='This words come from Kindle Oasis '
                                        'dictionary',
                            language='English',
                            words=translated_words)
    translated_words_path = pathlib.Path().absolute().parent \
        .joinpath(f'final/result_en/oasis.json')
    # print(translated_words_path.absolute())
    with open(translated_words_path, 'w', encoding='utf8') as f:
        json.dump(sk_dict.to_dict(), f, ensure_ascii=False, indent=4)
