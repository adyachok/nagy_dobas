import re
from pathlib import Path

from bs4 import BeautifulSoup

from dicts.stardict.perekladach.application import build
from common.models import WordMetadata, Translation, Word


def translate_words(words: Word, dict_path='dicts/stardict/stardict-UniversalEnUk'):
    dict_path = Path().absolute().parent.joinpath(dict_path)
    dicts = build(dict_path)
    counter = 0
    translations = []
    not_translated = []
    for word in words:
        translation = dicts[0].get_dict_by_word(word.stem)
        if type(translation) is not list:
            not_translated.append(translation)
        if not len(translation):
            not_translated.append(word.stem)
            counter += 1
        else:
            translation_html = translation[0].get('x').decode('utf8')
            translated_word, meanings = process_translated_html(
                translation_html)
            skovoroda_word = create_skovoroda_word(translated_word, meanings)
            skovoroda_word.usage.update(word.usage)
            translations.append(skovoroda_word)
    return translations, not_translated


def process_translated_html(translated_html):
    """If word has multiple meanings, it splits translation."""
    soup = BeautifulSoup(translated_html, 'html.parser')
    translation_meanings = re.findall('<b>I{1,3}</b>', translated_html)
    translated_word = soup.find('k').text
    meanings = []
    if len(translation_meanings) > 1:
        spans = []
        for meaning in translation_meanings:
            result = re.search(meaning, translated_html)
            spans.append(result.span())

        for idx, span in enumerate(spans):
            if idx == len(spans) - 1:
                start = spans[idx][0]
                end = len(translated_html)
            else:
                start = spans[idx][0]
                end = spans[idx + 1][0]
            html = translated_html[start:end]
            meanings.append(html)
    else:
        meanings.append(translated_html)
    return translated_word, meanings


def create_skovoroda_word(translated_word, meanings):
    word = WordMetadata(foreign_word=translated_word)
    for meaning in meanings:
        if not meaning.strip():
            raise Exception(f'{word.foreign_word} has no meaning!!')
        soup = BeautifulSoup(meaning, 'html.parser')
        transcript = soup.find('tr')
        if transcript:
            transcript = transcript.text
        else:
            transcript = ''
        p_o_s, translation = process_word_translation_lines(meaning)
        if not translation.strip():
            # print(p_o_s)
            # print(transcript)
            # print(meaning)
            print(f'{word.foreign_word} has no translation!!')
            translation = ' '
        tr = Translation(translation=translation)
        tr.transcript.append(transcript)
        tr.part_of_speech = p_o_s
        word.translations.append(tr)
    if not word.translations:
        raise Exception(f'{word.foreign_word} has no translations!!')
    prepare_word_test(word)
    return word


def prepare_word_test(word:WordMetadata):
    test_str = "".join([tr.translation.strip() for tr in word.translations
                        if tr.translation.strip() not in
                        ['adv', 'n', 'v', 'a', 'adj']])
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

def process_word_translation_lines(translated_html):
    # print(translated_html)
    soup = BeautifulSoup(translated_html, 'html.parser')
    bqs = [b.text for b in soup.find_all('blockquote')]
    # if line len < 5 not add \t
    lines = []
    part_of_speech = find_part_of_speech(translated_html)
    for idx, line in enumerate(bqs):
        line = line.strip()
        if re.match('\d{1,3}\).*', line):
            lines.append(line)
        else:
            if not part_of_speech and len(line) < 5:
                part_of_speech = lines.append(line)
            else:
                if line not in ['adv', 'n', 'v', 'a', 'adj']:
                # If line does not start from number, for example 1)
                    if idx == 0:
                        lines.append(line)
                    else:
                        lines.append(f'\t{line}')
    return part_of_speech, '\n'.join(lines)


def find_part_of_speech(html):
    soup = BeautifulSoup(html, 'html.parser')
    part_of_speech = soup.find('c', text='')
    if not part_of_speech:
        part_of_speech = soup.find('abr', text='')
    return part_of_speech.text  if part_of_speech else ''
