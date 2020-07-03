import json
import os
import pathlib
import random
import re
import time

from hu.sztaki_translator import SztakiTranslator


def get_corpus(filename='../felirat/nagy_dobas.txt'):
    with open(filename, 'r') as felirat:
        corpus = []
        for line in felirat:
            if not re.match('^\d.*', line):
                line = line.strip()
                if line:
                    corpus.append(line)
        return corpus


def remove_tags_and_chars(corpus):
    tags = ['<i>', '</i>', '\'', '"', '!', '?', '.', ',', '-']
    new_corpus = []
    for line in corpus:
        for tag in tags:
            if tag in line:
                line = line.replace(tag, '')
        new_corpus.append(line)
    return new_corpus


stop_words = {'és', 'is', 'több', 'a', 'ha', 'egy', 'az', 'volt', 'úgy',
              'azt', 'de', 'ezek', 'vagyok', 'én', 'nem', 'igaz', 'történet',
              '&', 'moodys', 'poors', 'venni', 'adja', 'okos', 'mondott',
              'semmit', 'menj', 'hozzájuk', 'azzal', 'kerülsz', 'bajba',
              'amit', 'tudsz', 'hanem', 'biztosan', 'van', 'mark', 'twain',
              'üdv', 'frank', 'asszony', 'gyerekek', 'úr', '\ufeff1', 'adunk',
              'évek', 'végén', 'ember', 'azért', 'lett', 'hogy', 'nagy',
              'pénzeket', 'keressen', 'mint', 'vagy', 'bank', 'maga', 'lesz',
              'talán', 'ez', '"', '”'}


def unite_stopwords():
    utils_path = pathlib.Path().parent.joinpath('utils/hu')
    for file_name in os.listdir(utils_path):
        with open(utils_path.joinpath(file_name)) as f:
            stop_words.update(f.read().split())


def lowercase_corpus(corpus):
    new_corpus = []
    for line in corpus:
        new_corpus.append(line.lower())
    return new_corpus


def is_stopword(word):
    return word in stop_words or re.match('^\d.*', word)


def split_and_remove_stopwords(corpus):
    words_corpus = []
    words_corpus_set = set()
    for line in corpus:
        line = line.split()
        for idx, word in enumerate(line):
            if is_stopword(word):
                continue
            elif word not in words_corpus_set:
                words_corpus_set.add(word)
                words_corpus.append(word)
    return words_corpus


def process_text(corpus):
    import hu_core_ud_lg

    nlp = hu_core_ud_lg.load()
    doc = nlp(corpus)
    return {str(token): str(token.lemma_) for token in doc
            if token.tag_ not in ['PUNCT', 'NUM']
            and not token.is_stop}


def filter_and_sort_lemmas(lemmas_dict, words_corpus):
    processed_corpus_set = set()
    processed_corpus = []
    for word in words_corpus:
        if word in lemmas_dict:
            lemma = lemmas_dict[word]
            if lemma not in processed_corpus_set:
                processed_corpus_set.add(lemma)
                processed_corpus.append(lemma)
    return processed_corpus


def build_unknown_words_list(words_corpus):
    lemmas_dict = process_text(" ".join(words_corpus))
    # print(lemmas_dict)
    processed_corpus = filter_and_sort_lemmas(lemmas_dict, words_corpus)
    # print(processed_corpus)
    # print(len(processed_corpus))
    processed_corpus = [word for word in processed_corpus
                        if word not in stop_words]
    # print(processed_corpus)
    # print(len(processed_corpus))
    return processed_corpus



def save_translation_results(translation, translation_path):
    with open(translation_path, 'w', encoding='utf8') as s:
        json.dump(translation, s, ensure_ascii=False, indent=4)


def save_not_translated_words(not_translated_words, not_translated_words_path):
    with open(not_translated_words_path, 'w') as ns:
        ns.write("\n".join(not_translated_words))


def translate(translator, wordspath, translation_path,
              not_translated_words_path):
    with open(wordspath) as f:
        for line in f.readlines():
            delay = random.randint(5, 30)
            search_word = line.strip()
            translator.translate_word_with_sztaki(search_word)
            time.sleep(delay)
            if delay < 13:
                save_translation_results(translator.sdict.to_dict(),
                                         translation_path)
                save_not_translated_words(translator.not_translated_words,
                                          not_translated_words_path)
        save_translation_results(translator.sdict.to_dict(), translation_path)
        save_not_translated_words(translator.not_translated_words,
                                  not_translated_words_path)


if __name__ == '__main__':
    # unite_stopwords()
    # corpus = remove_tags_and_chars(get_corpus())
    # corpus = lowercase_corpus(corpus)
    # # print(corpus)
    # words_corpus = split_and_remove_stopwords(corpus)
    # # print(words_corpus)
    # # print(len(words_corpus))
    #
    # processed_corpus = words_corpus
    # for _ in range(4):
    #     processed_corpus = build_unknown_words_list(processed_corpus)
    # print(processed_corpus)
    #
    # filepath = pathlib.Path().cwd().joinpath('result').joinpath('words.txt')
    # with open(filepath, 'w') as f:
    #     f.write("\n".join(processed_corpus))

    # d = dictdlib.DictReader(basename='freedict_hu_en/hun-eng')
    # with open(pathlib.Path().cwd().joinpath('result').joinpath('words.txt')) as f:
    #     not_translated_words = []
    #     for line in f.readlines():
    #         line = line.strip()
    #         result_list = d.getdef(line)
    #         if not result_list:
    #             not_translated_words.append(line)
    #         result_list = [s.decode("utf-8", "strict") for s in result_list]
    #         print( " ".join(result_list) )
    #
    #     print(f'Not translated words: {len(not_translated_words)}')
    # with open(pathlib.Path().cwd().joinpath('result').joinpath('not_translated_words.txt'), 'w') as f:
    #     f.write('\n'.join(not_translated_words))

        corpus = pathlib.Path().parent.joinpath(f'felirat/4 fejezet.txt').read_text().lower()
        lemmas_dict = process_text(corpus)
        wordsfile = f'words_{time.time()}.txt'
        wordspath = pathlib.Path().parent.joinpath(f'final/from_hu/{wordsfile}')
        not_translated_words_path = pathlib.Path().parent \
            .joinpath(f'final/result_hu/4 fejezet not translated.txt')
        translated_words_path = pathlib.Path().parent \
            .joinpath(f'final/result_hu/4 fejezet translated.json')
        unite_stopwords()
        lemmas = {l for l in lemmas_dict.values() if l.strip()
                  and not is_stopword(l)}
        wordspath.write_text('\n'.join(lemmas))

        translator = SztakiTranslator(dict_name='JW.org Stay In God\'s Love.',
                                      dict_description='Translated 4th chapter '
                                                       'of Hundatian version Stay '
                                                       'In God\'s Love',
                                      dict_language='Hungarian')
        translate(translator, wordspath, translated_words_path,
                  not_translated_words_path)
        print(f'Not translated words {len(translator.sdict.not_translated_words)}')



