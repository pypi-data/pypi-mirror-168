import os
import json
import importlib

bases_module = 'mext.providers.bases'
bases_file_name = 'mext/all_bases.json'
bases_file_path = os.path.abspath(bases_file_name)
bases_json = json.load(open(bases_file_path))


def get_all_bases_classes():
    all_bases = {}
    for base_info in bases_json:
        base_filename, base_class = base_info['file'], base_info['class']
        BaseModule = importlib.import_module(
            '{}.{}'.format(bases_module, base_filename),
        )
        BaseClass = getattr(BaseModule, base_class)
        all_bases[base_class] = BaseClass
    return all_bases


globals().update(get_all_bases_classes())
