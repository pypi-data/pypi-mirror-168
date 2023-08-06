import json
import functools

from mext import enums

# Get Selenium Status Code
def get_status(logs):
    for log in logs:
        if log['message']:
            d = json.loads(log['message'])
            try:
                content_type = 'text/html' in d['message']['params']['response']['headers']['content-type']
                response_received = d['message']['method'] == 'Network.responseReceived'
                if content_type and response_received:
                    return d['message']['params']['response']['status']
            except:
                pass

# Decorator
def data_page(func):

    attribute_name = enums.DatacallAttributes[func.__name__]

    @functools.wraps(func)
    def wrapper(instance, url, refresh=False):

        attribute_value = getattr(instance, attribute_name, None)

        try:
            if attribute_value and refresh is False:
                return attribute_value

            instance.selenium.get_cfpage(url)
            instance.find_error(url)

            return_data = func(instance)
            
            instance.selenium.exit()

            setattr(instance, attribute_name, return_data)
            return getattr(instance, attribute_name)
        except Exception as e:
            raise e

    return wrapper
