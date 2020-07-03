import time

import requests
from bs4 import SoupStrainer, BeautifulSoup

from common.models import WordMetadata, Translation, SkovorodaDict


class SztakiTranslator:
    def __init__(self, dict_name, dict_description, dict_language,
                 max_translations_per_word=1):
        self.sdict = SkovorodaDict(name=dict_name,
                                   description=dict_description,
                                   language=dict_language)
        self.max_translations_per_word = max_translations_per_word
        self.not_translated_words = []

    def parse_sztaki_response(self, html, search_word):
        '''
                {
                    'mama':
                        {
                            'noun': {
                                'example': 'mama,
                                'translations: {
                                    'mum': [ 'USA: mum', 'UK: mam'],
                                    ...
                                }
                            },
                            'adv': {
                                ...
                            }
                        }
                }

        '''
        klass = SoupStrainer(
            attrs={'class': 'firefoxstupidtablepositionbugwrapper'})
        soup = BeautifulSoup(html, 'html.parser', parse_only=klass)
        translation_divs = soup.find_all(
            attrs={'class': 'firefoxstupidtablepositionbugwrapper'})
        divs_counter = 0
        if not translation_divs:
            self.not_translated_words.append(search_word)
            return
        for div in translation_divs:
            if divs_counter > self.max_translations_per_word:
                break
            divs_counter += 1
            try:
                translated_word = div.find(attrs={'class': 'Word eNodeText'}).find(
                    attrs={'class': 'prop prop_content freetext'}).text
            except AttributeError:
                print(f'Error processing word {search_word} option.')
                continue

            word = WordMetadata(foreign_word=translated_word)
            part_of_speach = div.find(attrs={'class': 'Word eNodeText'}).find(
                attrs={'class': 'pos prop prop_pos qualmenu'}).text
            word.part_of_speech = part_of_speach

            translation_ol = div.find('ol', attrs={
                'class': 'meaningList MeaningList WordMeaningList num'})
            translation_divs = translation_ol.find_all(
                attrs={'class': 'translation eNodeText'})

            for div in translation_divs:
                translation = Translation(translation=div.find('a').text)
                pronunciation_spans = div.find_all('span')
                for span in pronunciation_spans:
                    pronunciation = span.text
                    translation.transcript.append(pronunciation)
                word.translations.append(translation)
            self.sdict.words.append(word)

    def translate_word_with_sztaki(self, search_word):
        while True:
            try:
                url = f'http://szotar.sztaki.hu/en/search?fromlang=hun&' \
                      f'tolang=eng&searchWord={search_word}'
                response = requests.get(url)
                if response.status_code == 200:
                    html = response.text
                    try:
                        return self.parse_sztaki_response(html, search_word)
                    except Exception as e:
                        print(f'While parsing search word {search_word} next '
                              f'exception occured {e}')
            except requests.exceptions.ConnectionError:
                print("Network connection error.")
            time.sleep(5)


if __name__ == '__main__':
    translator = SztakiTranslator(dict_name='JW.org Stay In God\'s Love.',
                                  dict_description='Translated 4th chapter '
                                                   'of Hundatian version Stay '
                                                   'In God\'s Love',
                                  dict_language='Hungarian')
    translator.translate_word_with_sztaki('világ')
    print(translator.sdict.to_dict())
    print(translator.not_translated_words)