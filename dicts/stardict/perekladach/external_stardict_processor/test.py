from .dictutils import find_installed_dictionaries_paths
from .app import StarDict, DictionarySettings


from ..html_output.html_convertor import build_report

DICTS_DIRPATH = 'dictionaries'
SETTINGS_DIRPATH = 'settings'


def test(word_str_list):
    settings = DictionarySettings(DICTS_DIRPATH, SETTINGS_DIRPATH)
    stardict = StarDict(settings)
    text = []
    fail = 0
    failed_words = []

    # word_str_list = ['hallo', 'happy', 'Tier', 'Elefant']
    for word_str in word_str_list:
        enabled_dictionaries_definitions = stardict.get_definitions_from_enabled_dictionaries(
            word_str)
        for dictionary, definitions in enabled_dictionaries_definitions:
            # print(dictionary.name)
            # Calculating translation coverage
            if not definitions:
                fail += 1
                failed_words.append(word_str)

            for definition in definitions:
                for k, v in definition.items():
                    d = v.decode('utf-8', errors='ignore')
                    d = tuple(d.split('\n', 1))
                    text.append(d)
    fail_percentage = fail / len(word_str_list) * 100
    build_report(text, fail_percentage, failed_words)


def install_dictionaries():
    settings = DictionarySettings(DICTS_DIRPATH, SETTINGS_DIRPATH)

    installed_dictionaries_paths = find_installed_dictionaries_paths(
        DICTS_DIRPATH)
    for dictionary_path in installed_dictionaries_paths:
        settings.install_dictionary(dictionary_path)


install_dictionaries()

# with open('../words/word_list.txt', 'r', encoding='UTF-8') as w:
#     word_list = [word for word in w.read().split('\n') if word.strip()]
#     test(word_list)
