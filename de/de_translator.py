import json
import re
from pathlib import Path
import spacy

from common.models import Word, Translation, WordMetadata, SkovorodaDict
from dicts.stardict.perekladach.application import build

nlp = spacy.load('de_core_news_lg')

def get_words(text):
    doc = nlp(text)
    tokens = [token for token in doc if token.pos_ not in
              ['PUNCT', 'NUM', 'PROPN', 'ADP', 'AUX']]
    tokens = [token for token in tokens if token.lemma_.strip()
              not in ['', '.', ',', '(', ')', '“', '?']]
    tokens = [token for token in tokens
              if not re.match('^\d.*', token.lemma_.strip())]
    return [Word(0, token, token.lemma_, 'German') for token in tokens]


def prepare_word_test(word:WordMetadata):
    test_str = "".join([tr.translation.strip() for tr in word.translations])
    foreign_word = word.foreign_word
    # Removes foreign word occurrence in translation
    test_str = test_str.replace('\n', ' ')
    test_str = test_str.replace(foreign_word, '~')
    # Removes transcript in translation
    match = re.search('\[.*\]', test_str)
    if match:
        test_str_beginning = test_str[:match.start()]
        test_str_ending = test_str[match.end()-1:]
        test_str = test_str_beginning + test_str_ending
    word.test = test_str[:251]

if __name__ == '__main__':
    root = Path().parent.absolute().parent.absolute()
    filepath = 'final/from_de/bleib in gots liebe art 4.txt'
    filepath = root.joinpath(filepath)
    dictpath = root.joinpath('dicts/stardict/stardict-deu-ru')
    text = filepath.read_text(encoding='utf8')

    words = get_words(text)
    dicts = build(dictpath)
    counter = 0

    sk_dict = SkovorodaDict(name='Bleib in Gottes Liebe Kap.4',
                            description='Bleib in Gottes Liebe. Kapitel 4. '
                                        'Autorität respektieren.',
                            language='German')

    for word in words:
        translation = dicts[0].get_dict_by_word(word.stem)
        if translation:

            translation = translation[0].get('x')
            translation = str(translation, encoding='utf8')
            result = re.search('<k>\w.*</k>', translation)
            start, end = result.span()
            word = translation[start: end].strip('<k>').strip('</k>')
            translation = translation[end:]
            translation = Translation(translation=translation)
            word = WordMetadata(foreign_word=word)
            word.translations.append(translation)
            prepare_word_test(word)
            sk_dict.words.append(word)
        else:
            counter += 1

    translated_words_path = Path().absolute().parent \
        .joinpath(f'final/result_de/blieb_in_gottes_liebe_kap_4.json')
    with open(translated_words_path, 'w', encoding='utf8') as f:
        json.dump(sk_dict.to_dict(), f, ensure_ascii=False, indent=4)

    print(f'Not translated: {counter}')
    print(sk_dict.to_dict())
