import datetime
from magic_lib.misc.encode import JsonBase


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
                 previous_close=None, previous_volume=None):
        self.symbol = symbol
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.previous_close = previous_close
        self.previous_volume = previous_volume

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
            'volume': self.volume
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

        assert self.date is not None
        assert isinstance(self.date, datetime.datetime)

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
                 quote_obj=None):
        self.symbol = symbol
        self.trading_type = trading_type
        self.scanner = scanner
        self.condition = condition
        self.rate = rate
        self.detail = detail
        self.quote_obj = quote_obj
        
    def to_json(self):
        # dump data
        quote_obj = {
            'symbol': self.quote_obj.symbol,
            'date': self.quote_obj.date.strftime('%Y-%m-%d %H:%M:%S'),
            'open': self.quote_obj.open,
            'high': self.quote_obj.high,
            'low': self.quote_obj.low,
            'close': self.quote_obj.close,
            'volume': self.quote_obj.volume
        }

        data = {
            'symbol': self.symbol,
            'date': self.date.strftime('%Y-%m-%d'),
            'trading_type': self.trading_type,
            'scanner': self.scanner,
            'condition': self.condition,
            'rate': self.rate,
            'detail': self.detail,
            'quote': quote_obj
        }
        return data
