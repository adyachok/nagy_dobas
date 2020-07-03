import logging
import os

from .external_stardict_processor.stardict import IdxFileReader, \
    IfoFileReader, DictFileReader

logger = logging.basicConfig()

class Dictionary:

    def __init__(self, ifo_path, idx_path, dict_path):
        self._ifo_path = ifo_path
        self._idx_path = idx_path
        self._dict_path = dict_path
        self.dict_reader = self.init_dict_reader()

    def init_dict_reader(self):
        ifo_reader = IfoFileReader(self._ifo_path)
        idx_reader = IdxFileReader(self._idx_path,
                                   compressed=False,
                                   index_offset_bits=32)
        return DictFileReader(self._dict_path,
                              dict_ifo=ifo_reader,
                              dict_index=idx_reader,
                              compressed=True)


ROOT_PATH = os.path.dirname(__file__)
DICTS_PATH = os.path.join(ROOT_PATH, 'stardict')

class DictionariesManager:

    @staticmethod
    def get_dict_files(dicts_path):
        dicts = []
        for root, dirs, files in os.walk(dicts_path):
            dict_files = {}
            for f in files:
                if f.endswith('dict.dz'):
                    dict_files['dict_path'] = os.path.join(root, f)
                elif f.endswith('.idx'):
                    dict_files['idx_path'] = os.path.join(root, f)
                elif f.endswith('.ifo'):
                    dict_files['ifo_path'] = os.path.join(root, f)
                else:
                    file_path = os.path.join(root, f)
                    # logger.warn(f'Found file {file_path}')
            dicts.append(dict_files)
        return dicts

    @staticmethod
    def build_dicts(dict_files):
        dict_files = [d for d in dict_files if len(d) == 3]
        dicts = [Dictionary(ifo_path=d.get('ifo_path'),
                            idx_path=d.get('idx_path'),
                            dict_path=d.get('dict_path')) for d in dict_files]
        return dicts

    @staticmethod
    def init_dicts(dicts):
        return [d.init_dict_reader() for d in dicts]


def build(DICTS_PATH):
    dicts = DictionariesManager.get_dict_files(DICTS_PATH)
    dicts = DictionariesManager.build_dicts(dicts)
    return DictionariesManager.init_dicts(dicts)


if __name__ == '__main__':
    dicts = build(DICTS_PATH)
    print(dicts[0].get_dict_by_word('Hello'))
