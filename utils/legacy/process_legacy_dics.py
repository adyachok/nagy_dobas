# Script processes legacy dict files
import json
from pathlib import Path


def process_dict(filepath):
    filepath = Path(filepath)
    if filepath.exists():
        data = filepath.read_text(encoding='utf8')
        data = json.loads(data)
        words = data.get('words')

        for word in words:
            translation = word['translation']
            word['translation'] = [{'translation': translation, 'transcript': []}]

        filepath.write_text(
            json.dumps(data, ensure_ascii=False, indent=4), encoding='utf8')
    else:
        print('File doesn\'t exists')


def change_to_translations(filepath):
    filepath = Path(filepath)
    if filepath.exists():
        data = filepath.read_text(encoding='utf8')
        data = json.loads(data)
        words = data.get('words')

        for word in words:
            translations = word.pop('translation')
            word['translations'] = translations

        filepath.write_text(
            json.dumps(data, ensure_ascii=False, indent=4), encoding='utf8')
    else:
        print('File doesn\'t exists')


if __name__ == '__main__':
    filepath = '/Users/andreasgyascok/projects/IOS/skovoroda/skovoroda/fixtures/nagy_dobas.json'
    change_to_translations(filepath)