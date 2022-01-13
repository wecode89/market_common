import json
import os
import requests
from magic_lib.misc.log import get_logger


logger = get_logger(os.path.basename(__file__), level=os.environ.get('LOG_LEVEL', 'DEBUG'))


class MagicStoreAPI:
    def __init__(self, host=None, port=None):
        self.protocol = 'http'
        self.host = host
        self.port = port

    def _get_url(self, path):
        url = '{}://{}:{}{}'.format(self.protocol, self.host, self.port, path)
        return url

    def _request(self, url, method='GET', data=None):
        try:
            if method == 'GET':
                response = requests.get(url)
            elif method == 'POST':
                response = requests.post(url, data=json.dump(data))

            data = json.loads(response.content)
            return data
        except Exception as e:
            logger.error("url: {}".format(e))

    def create(self, db=None, collection=None, doc=None):
        path = '/{}/{}/document/create'.format(db, collection)
        url = self._get_url(path)
        response = self._request(url, method='POST', data=doc)
        return response

    def search(self, db=None, collection=None):
        path = '/{}/{}/document/search'.format(db, collection)
        url = self._get_url(path)
        response = self._request(url)
        return response
