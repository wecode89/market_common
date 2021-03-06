import datetime
import math
import os
from magic_lib.misc.log import get_logger
from magic_lib.misc.encode import JsonBase


logger = get_logger(os.path.basename(__file__), level=os.environ.get('LOG_LEVEL', 'DEBUG'))
millnames = ['',' Thousand',' Million',' Billion',' Trillion']


def millify(n):
    n = float(n)
    millidx = max(0, min(len(millnames)-1, int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


class Symbol(JsonBase):
    def __init__(self, symbol=None, exchange=None, region=None):
        self.symbol = symbol
        self.exchange = exchange
        self.region = region

        assert self.symbol is not None


class CompanyInfo(JsonBase):
    def __init__(self, symbol=None, company=None, exchange=None, industry=None, sector=None):
        self.symbol = symbol
        self.company = company
        self.exchange = exchange
        self.industry = industry
        self.sector = sector

        assert self.company is not None


class CompanyLogo(JsonBase):
    def __init__(self, symbol=None, url=None):
        self.symbol = symbol
        self.url = url

        assert self.url is not None


class Quote(JsonBase):
    def __init__(self, symbol=None, date=None, open=None, high=None, low=None, close=None, volume=None,
                 previous_close=None, previous_volume=None, market_cap=None):
        self.symbol = symbol
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.previous_close = previous_close
        self.previous_volume = previous_volume
        self.market_cap = market_cap

        assert isinstance(self.date, datetime.datetime)

    def to_json(self):
        # dump data
        data = {
            'symbol': self.symbol,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume,
            'market_cap': self.market_cap
        }
        return data


class IntradayData(JsonBase):
    def __init__(self, symbol=None, open=None, high=None, low=None, close=None, volume=None,
                 previous_close=None, previous_volume=None, interval=None):
        self.symbol = symbol
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.previous_close = previous_close
        self.previous_volume = previous_volume
        self.interval = interval


class HistoricData:
    def __init__(self, symbol=None, date=None, open=None, high=None, low=None, close=None, volume=None):
        self.symbol = symbol
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

        if isinstance(self.date, datetime.datetime):
            self.date = self.date.date()

        assert self.date is not None
        assert not isinstance(self.date, str)

    def to_json(self):
        # dump data
        data = {
            'symbol': self.symbol,
            'date': self.date.strftime('%Y-%m-%d'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume
        }
        return data


class StockAlert(JsonBase):
    def __init__(self, symbol=None, date=None, trading_type=None, scanner=None, condition=None, rate=None, detail=None,
                 quote_obj=None, company_obj=None):
        self.symbol = symbol
        self.date = date
        self.trading_type = trading_type
        self.scanner = scanner
        self.condition = condition
        self.rate = rate
        self.detail = detail
        self.quote_obj = quote_obj
        self.company_obj = company_obj
        
    def to_json(self):
        # quote json
        quote = {
            'symbol': self.quote_obj.symbol,
            'date': self.quote_obj.date.strftime('%Y-%m-%d %H:%M:%S'),
            'open': self.quote_obj.open,
            'high': self.quote_obj.high,
            'low': self.quote_obj.low,
            'close': self.quote_obj.close,
            'volume': self.quote_obj.volume,
            'market_cap': self.quote_obj.market_cap
        }

        logger.debug("quote['volume']: %s", quote['volume'])
        if quote['volume']:
            quote['volume_verbal'] = millify(quote['volume'])

        logger.debug("quote['market_cap']: %s", quote['market_cap'])
        if quote['market_cap']:
            quote['market_cap_verbal'] = millify(quote['market_cap'])

        # company json
        company = {
            'symbol': self.company_obj.symbol,
            'company': self.company_obj.company,
            'exchange': self.company_obj.exchange,
            'industry': self.company_obj.industry,
            'sector': self.company_obj.sector
        }

        # alert json
        data = {
            'symbol': self.symbol,
            'date': self.date.strftime('%Y-%m-%d'),
            'trading_type': self.trading_type,
            'scanner': self.scanner,
            'condition': self.condition,
            'rate': self.rate,
            'detail': self.detail,
            'quote': quote,
            'company': company
        }
        return data
