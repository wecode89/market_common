import json
import requests
from market_common.models.models import HistoricData


class MarketDataAPI:
    def __init__(self, host=None, port=None):
        self.protocol = 'http'
        self.host = host
        self.port = port

    def _get_url(self, path):
        url = '{}://{}:{}/{}'.format(self.protocol, self.host, self.port, path)
        print("----> url: {}".format(url))
        return url

    def _request(self, url):
        response = requests.get(url)
        data = json.loads(response.content)
        return data

    def get_quotes(self, symbols):
        url = self._get_url('/api/v1/quotes/'.format(','.join(symbols)))
        data = self._request(url)

        historic_data = [HistoricData(symbol=x['symbol'],
                                      date=convert_str_to_datetime_tz(x['date'], format='%Y-%m-%d'),
                                      open=x['open'],
                                      high=x['high'],
                                      low=x['low'],
                                      close=x['close'],
                                      volume=x['volume']) for x in data.get('data', [])]
        return historic_data

    def get_intraday(self, symbol):
        url = self._get_url('/api/v1/intraday-data/{}/{}?days='.format(symbol, days))
        data = self._request(url)

    def get_historic(self, symbol, days=100):
        url = self._get_url('/api/v1/historic-data/{}/{}?days='.format(symbol, days))
        data = self._request(url)

    def get_symbols(self):
        url = self._get_url('/api/v1/symbols')
        data = self._request(url)
        return data
    