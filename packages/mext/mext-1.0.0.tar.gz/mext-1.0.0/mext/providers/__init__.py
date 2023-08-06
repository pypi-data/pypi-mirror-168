import os
import json
import importlib

provider_module = 'mext.providers'
provider_file_name = 'mext/all_providers.json'
provider_file_path = os.path.abspath(provider_file_name)
providers_json = json.load(open(provider_file_path))


def get_provider_instance(name=None, netloc=None):
    for provider_info in providers_json:
        if (name and provider_info['name'] == name) or \
            (netloc and provider_info['netloc'] == netloc):
            ProviderClass = globals()[provider_info['class']]
            return ProviderClass(
                name=provider_info['name'],
                siteUrl=provider_info['netloc'],
            )
    raise ValueError("No such provider netloc {}".format(netloc))


def get_all_providers_classes():
    all_providers = {}
    for provider in providers_json:
        provider_filename, provider_class = provider['file'], provider['class']
        ProviderModule = importlib.import_module(
            '{}.{}'.format(provider_module, provider_filename),
        )
        ProviderClass = getattr(ProviderModule, provider_class)
        all_providers[provider_class] = ProviderClass
    return all_providers


globals().update(get_all_providers_classes())
