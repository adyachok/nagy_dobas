import json
from pathlib import Path


def open_words_file(filename):
    p = Path().parent.absolute().parent.joinpath('final/result_hu')
    p = p.joinpath(filename)
    with open(p, 'r') as f:
        return json.load(f)


def remove_us_transcript(sk_dict):
    words = []
    for word in sk_dict.get('words', list):
        translations = []
        for translation in word.get('translations', []):
            transcripts = translation.get('transcript')
            new_transcripts = []
            for transcript in transcripts:
                if transcript.startswith('US'):
                    continue
                elif transcript.startswith('UK'):
                    transcript = transcript.replace('UK:', '').strip()
                else:
                    continue
                new_transcripts.append(transcript)
            translation['transcript'] = new_transcripts
            translations.append(translation)
        word['translations'] = translations
        words.append(word)
    sk_dict['words'] = words
    return sk_dict


def save_data_back(filename, sk_dict):
    p = Path().parent.absolute().parent.joinpath('final/result_hu')
    p = p.joinpath(filename)
    with open(p, 'w', encoding='utf8') as f:
        json.dump(sk_dict, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    sk_dict = open_words_file('nagy_dobas.json')
    sk_dict = remove_us_transcript(sk_dict)
    save_data_back('nagy_dobas.json', sk_dict)
