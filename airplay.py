import inspect
import logging
import random
import string
import requests
import yaml
from requests.exceptions import RequestException


logging.basicConfig(filename='airtest.log', filemode='w', format='%(asctime)s-%(levelname)s-%(message)s')
logger = logging.getLogger()
logger.setLevel(20)

with open(r'config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class HTTPStatusCodeException(RequestException):
    def __init__(self, status):
        self.status = status


class Table:
    def __init__(self, base_key, table_name, api_key):
        self._base_key = base_key
        self._table_name = table_name
        self._api_key = api_key

    def _get_headers(self):
        logger.debug("Build headers for {} method".format(inspect.stack()[1].function))
        return {'Authorization': 'Bearer {}'.format(self._api_key)}

    def _get_url(self):
        logger.debug("Build url for {} method".format(inspect.stack()[1].function))
        return 'https://api.airtable.com/v0/{}/{}'.format(self._base_key, self._table_name)

    def items(self):
        logger.info("get table items for {}".format(self._table_name))
        resp = requests.get(self._get_url(), headers=self._get_headers())
        if not 200 <= resp.status_code < 300:
            raise HTTPStatusCodeException(resp.status_code)
        return resp.json()

    def insert(self, **fields_dict):
        resp = requests.post(self._get_url(), headers=self._get_headers(), json={'fields': fields_dict})
        logger.info("Insert record:{} on {}, with response {}".format(fields_dict, self._table_name, resp.status_code))
        if not 200 <= resp.status_code < 300:
            raise HTTPStatusCodeException(resp.status_code)
        return resp.json()

    def modify(self, target_id, **fields_dict):
        resp = requests.patch('{}/{}'.format(self._get_url(), target_id), headers=self._get_headers(),
                              json={'fields': fields_dict})
        logger.info(
            "Record:{} modified on {}, with response {}".format(fields_dict, self._table_name, resp.status_code))
        if not 200 <= resp.status_code < 300:
            raise HTTPStatusCodeException(resp.status_code)
        return resp.json()

    def delete(self, target_id):
        resp = requests.delete('{}/{}'.format(self._get_url(), target_id), headers=self._get_headers())
        logger.info(
            "Record:{} deleted on {}, with response {}".format(target_id, self._table_name, resp.status_code))
        if not 200 <= resp.status_code < 300:
            raise HTTPStatusCodeException(resp.status_code)
        return resp.json()


def random_str(kind, nr_char):
    letters = string.ascii_letters
    numbers = string.digits
    if kind == "l":
        char = letters
    else:
        char = numbers
    output = [y for nr in range(nr_char) for y in random.choice(list(char))]
    try:
        return int(''.join(output))
    except ValueError:
        return ''.join(output)


def rand_item(count=1):
    logger.debug("Random item generated for {}".format(inspect.stack()[1].function))
    res = []
    for _ in range(count):
        res.append({'Name': random_str("l", 10), 'Code': random_str("n", 10)})
    return res


def _wrap_insert(x):
    logger.debug("I'm in {}".format(inspect.stack()[0].function))
    tbl, item = x
    return tbl.insert(**item)


tbl = Table(config['base_key'], config['table_name'], config['api_key'])
