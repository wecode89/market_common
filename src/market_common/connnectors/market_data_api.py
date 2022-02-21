import json
import os
import requests
from datetime import datetime
from magic_lib.misc.log import get_logger
from market_common.models.models import Symbol, Quote, HistoricData, CompanyInfo


logger = get_logger(os.path.basename(__file__), level=os.environ.get('LOG_LEVEL', 'DEBUG'))


class MarketDataAPI:
    def __init__(self, host=None, port=None):
        self.protocol = 'http'
        self.host = host
        self.port = port

    def _get_url(self, path):
        url = '{}://{}:{}{}'.format(self.protocol, self.host, self.port, path)
        return url

    def _request(self, url):
        try:
            response = requests.get(url)
            data = json.loads(response.content)
            return data
        except Exception as e:
            logger.error("url: {}".format(e))

    def get_company(self, symbols):
        url = self._get_url('/api/v1/quotes/{}'.format(','.join(symbols)))
        data = self._request(url)
        data = data.get('data')
        if data:
            company = CompanyInfo(symbol=data.get('symbol'),
                                  company=data.get('company'),
                                  exchange=data.get('exchange'),
                                  industry=data.get('industry'),
                                  sector=data.get('sector'),)
            return company

    def get_quotes(self, symbols):
        url = self._get_url('/api/v1/quotes/{}'.format(','.join(symbols)))
        data = self._request(url)

        quotes = []
        try:
            for x in data['data']:
                try:
                    quote = Quote(symbol=x['symbol'],
                                  date=datetime.strptime(x['date'], "%Y-%m-%d %H:%M:%S"),
                                  open=x['open'],
                                  high=x['high'],
                                  low=x['low'],
                                  close=x['close'],
                                  volume=x['volume'],
                                  previous_close=None,
                                  previous_volume=None,
                                  market_cap=float(x.get('marketCap')))
                    quotes.append(quote)
                except Exception as e:
                    logger.error("url: {}".format(e))
        except Exception as e:
            logger.error("url: {}".format(e))
        return quotes

    def get_intraday(self, symbol):
        url = self._get_url('/api/v1/intraday-data/{}/{}?days='.format(symbol, days))
        data = self._request(url)

    def get_historic(self, symbol, days=100):
        url = self._get_url('/api/v1/historic-data/{}?days={}'.format(symbol, days))
        data = self._request(url)

        ohlcs = []
        try:
            for x in data['data']:
                try:
                    item = HistoricData(symbol=symbol,
                                        date=datetime.strptime(x['date'], "%Y-%m-%d"),
                                        open=x['open'],
                                        high=x['high'],
                                        low=x['low'],
                                        close=x['close'],
                                        volume=x['volume'])
                    ohlcs.append(item)
                except Exception as e:
                    logger.error("url: {}".format(e))
        except Exception as e:
            logger.error("url: {}".format(e))
        return ohlcs

    def get_symbols(self, local=False):
        url = self._get_url('/api/v1/symbols')
        if local:
            url = url + "?local=true"

        data = self._request(url)

        try:
            symbols = [Symbol(symbol=x['symbol'],
                              exchange=x['exchange'],
                              region=x['region'], ) for x in data['data']]
            return symbols
        except Exception as e:
            logger.error("url: {}, error: {}".format(url, e))