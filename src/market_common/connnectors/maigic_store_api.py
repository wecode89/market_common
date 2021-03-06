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
        logger.debug("Url : {}".format(url))
        logger.debug("data : {}".format(data))

        try:
            if method == 'GET':
                response = requests.get(url)
            elif method == 'POST':
                response = requests.post(url, data=json.dumps(data))

            data = json.loads(response.content)
            return data
        except Exception as e:
            logger.error("url: {}, error: {}".format(url, e))

    def create(self, db=None, collection=None, doc=None, criteria=None):
        logger.debug("criteria : {}".format(criteria))
        
        path = '/api/v1/{}/{}/document/create'.format(db, collection)
        if criteria:
            path = path + "?" + "&".join(["{}={}".format(k, v) for k, v in criteria.items()])
        url = self._get_url(path)
        response = self._request(url, method='POST', data=doc)
        return response

    def search(self, db=None, collection=None):
        path = '/api/v1/{}/{}/document/search'.format(db, collection)
        url = self._get_url(path)
        response = self._request(url)
        return response
