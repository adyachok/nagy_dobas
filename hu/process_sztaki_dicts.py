# Script for converting web scraper output to the common application format.
import json
from datetime import datetime
from typing import List, Dict

from common.models import Translation, WordMetadata, SkovorodaDict


def prepare_sztaki_translation(translations: Dict[str, List[str]]) \
        -> List[Translation]:
    word_translations = []
    for k, v in translations.items():
        word_translations.append(Translation(translation=k,
                                             transcript=v))
    return word_translations


def prepare_sztaki_dict(sztaki_dict):
    for k, v in sztaki_dict.items():
        part_of_speech = k
        foreign_word = v.get('example')
        translation_dict = v.get('translation')
        translation = prepare_sztaki_translation(translation_dict)
        return WordMetadata(foreign_word=foreign_word,
                            part_of_speech=part_of_speech,
                            translations=translation)


def process_and_save(sztaki_translation_list: List):
    '''Processes translated by Sztaki web scraper words in to common format,
    acceptable by the application.
    :param sztaki_translation_list:
    :return:
    '''
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    new_dict = SkovorodaDict(name='The Big Short',
                             description='This dictionary contains translated '
                                         'words from The Big Short film',
                             language='Hungarian',
                             date_created=date_time,
                             words=[])
    for word_translation in sztaki_translation_list:
        sztaki_translation_dict = list(word_translation.values())[0]
        sztaki_dict = prepare_sztaki_dict(sztaki_translation_dict)
        new_dict.words.append(sztaki_dict)
    with open('final/translated.json', 'w', encoding='utf8') as w:
        json.dump(new_dict.to_dict(), w, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    sztaki_translation_list = []
    with open('../final/result_hu/sztaki_translated.json', 'rb') as f:
        sztaki_translation_list = json.load(f)
    with open('../final/result_hu/sztaki_translated_2.json', 'rb') as f:
        sztaki_translation_list.extend(json.load(f))
    process_and_save(sztaki_translation_list)

