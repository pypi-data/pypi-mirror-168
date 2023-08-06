from urllib.parse import urlparse

from mext import enums, exceptions, providers


class Mext:

    def __init__(self, type_list: list = None, url: str = None):

        if type_list and url:
            self.populate(type_list, url)
        elif not (type_list and url):
            return
        else:
            raise Exception("For population during initialization both types of data and url needs to be provided")
        

    @property
    def all_providers(self):
        return providers.providers_json

    def validate_type_list(self, type_list):
        wrong_types = []
        for t in type_list:
            if t not in list(enums.Datacall.keys()):
                wrong_types.append(t)

        if wrong_types:
            raise ValueError(
                "Wrong fetch types provided: {}".format(wrong_types))

        return type_list

    def populate(self, type_list: list, url: str):
        type_list = self.validate_type_list(type_list)

        parsed_url = urlparse(url)

        data = {}
        provider_instance = providers.get_provider_instance(
            netloc=parsed_url.netloc)
        provider_instance.process_url(url)
        for data_type in type_list:
            data[data_type] = getattr(
                provider_instance, enums.Datacall[data_type].value[0]
            )(url)

        if not data:
            raise exceptions.NotYetSupported(
                'The given URL is not supported right now.')
        
        for key, value in data.items():
            setattr(self, key, value)
