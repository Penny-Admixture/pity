from collections import OrderedDict
from decimal import ROUND_DOWN
from functools import wraps
from time import time

import requests

from bit.utils import Decimal

DEFAULT_CACHE_TIME = 60

# Constant for use in deriving exchange
# rates when given in terms of 1 BTC.
ONE = Decimal(1)

# https://en.bitcoin.it/wiki/Units
SATOSHI = 1
uPPC = 10 ** 2
mPPC = 10 ** 5
PPC = 10 ** 6

SUPPORTED_CURRENCIES = OrderedDict([
    ('satoshi', 'Satoshi'),
    ('uppc', 'MicroPeercoin'),
    ('mppc', 'MilliPeercoin'),
    ('ppc', 'Peercoin'),
    ('usd', 'United States Dollar'),
    ('eur', 'Eurozone Euro'),
    ('gbp', 'Pound Sterling'),
    ('jpy', 'Japanese Yen'),
    ('cny', 'Chinese Yuan'),
    ('cad', 'Canadian Dollar'),
    ('aud', 'Australian Dollar'),
    ('nzd', 'New Zealand Dollar'),
    ('rub', 'Russian Ruble'),
    ('brl', 'Brazilian Real'),
    ('chf', 'Swiss Franc'),
    ('sek', 'Swedish Krona'),
    ('pln', 'Polish Zloty'),
    ('krw', 'South Korean Won'),
    ('twd', 'New Taiwan Dollar'),
])

# https://en.wikipedia.org/wiki/ISO_4217
CURRENCY_PRECISION = {
    'satoshi': 0,
    'uppc': 2,
    'mppc': 5,
    'ppc': 6,
    'usd': 2,
    'eur': 2,
    'gbp': 2,
    'jpy': 0,
    'cny': 2,
    'cad': 2,
    'aud': 2,
    'nzd': 2,
    'rub': 2,
    'brl': 2,
    'chf': 2,
    'sek': 2,
    'dkk': 2,
    'isk': 2,
    'pln': 2,
    'hkd': 2,
    'krw': 0,
    'sgd': 2,
    'thb': 2,
    'twd': 2,
    'clp': 0
}


def set_rate_cache_time(seconds):
    global DEFAULT_CACHE_TIME
    DEFAULT_CACHE_TIME = seconds


def satoshi_to_satoshi():
    return SATOSHI


def ubtc_to_satoshi():
    return uPPC


def mbtc_to_satoshi():
    return mPPC


def btc_to_satoshi():
    return PPC


class CoinPaprikaRates:
    SINGLE_RATE = 'https://api.coinpaprika.com/v1/price-converter?base_currency_id=ppc-peercoin&quote_currency_id={}&amount=1'

    @classmethod
    def currency_to_satoshi(cls, currency: str) -> int:
        rate = requests.get(cls.SINGLE_RATE.format(currency)).json()["price"]
        return int(ONE / Decimal(rate) * PPC)

    @classmethod
    def usd_to_satoshi(cls):
        return cls.currency_to_satoshi('usd-us-dollars')

    @classmethod
    def eur_to_satoshi(cls):
        return cls.currency_to_satoshi('eur-euro')

    @classmethod
    def gbp_to_satoshi(cls):
        return cls.currency_to_satoshi('gbp-pound-sterling')

    @classmethod
    def jpy_to_satoshi(cls):
        return cls.currency_to_satoshi('jpy-japanese-yen')

    @classmethod
    def cny_to_satoshi(cls):
        return cls.currency_to_satoshi('cny-yuan-renminbi')

    @classmethod
    def cad_to_satoshi(cls):
        return cls.currency_to_satoshi('cad-canadian-dollar')

    @classmethod
    def aud_to_satoshi(cls):
        return cls.currency_to_satoshi('aud-australian-dollar')

    @classmethod
    def nzd_to_satoshi(cls):
        return cls.currency_to_satoshi('nzd-new-zealand-dollar')

    @classmethod
    def rub_to_satoshi(cls):
        return cls.currency_to_satoshi('rub-russian-ruble')

    @classmethod
    def brl_to_satoshi(cls):
        return cls.currency_to_satoshi('brl-brazil-real')

    @classmethod
    def chf_to_satoshi(cls):
        return cls.currency_to_satoshi('chf-swiss-franc')

    @classmethod
    def sek_to_satoshi(cls):
        return cls.currency_to_satoshi('sek-swedish-krona')

    @classmethod
    def pln_to_satoshi(cls):
        return cls.currency_to_satoshi('pln-polish-zloty')

    @classmethod
    def krw_to_satoshi(cls):
        return cls.currency_to_satoshi('krw-south-korea-won')

    @classmethod
    def twd_to_satoshi(cls):
        return cls.currency_to_satoshi('twd-taiwan-new-dollar')


class RatesAPI:
    """Each method converts exactly 1 unit of the currency to the equivalent
    number of satoshi.
    """
    IGNORED_ERRORS = (requests.exceptions.ConnectionError,
                      requests.exceptions.HTTPError,
                      requests.exceptions.Timeout)

    USD_RATES = [CoinPaprikaRates.usd_to_satoshi]
    EUR_RATES = [CoinPaprikaRates.eur_to_satoshi]
    GBP_RATES = [CoinPaprikaRates.gbp_to_satoshi]
    JPY_RATES = [CoinPaprikaRates.jpy_to_satoshi]
    CNY_RATES = [CoinPaprikaRates.cny_to_satoshi]
    CAD_RATES = [CoinPaprikaRates.cad_to_satoshi]
    AUD_RATES = [CoinPaprikaRates.aud_to_satoshi]
    NZD_RATES = [CoinPaprikaRates.nzd_to_satoshi]
    RUB_RATES = [CoinPaprikaRates.rub_to_satoshi]
    BRL_RATES = [CoinPaprikaRates.brl_to_satoshi]
    CHF_RATES = [CoinPaprikaRates.chf_to_satoshi]
    SEK_RATES = [CoinPaprikaRates.sek_to_satoshi]
    PLN_RATES = [CoinPaprikaRates.pln_to_satoshi]
    KRW_RATES = [CoinPaprikaRates.krw_to_satoshi]
    TWD_RATES = [CoinPaprikaRates.twd_to_satoshi]

    @classmethod
    def usd_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.USD_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def eur_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.EUR_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def gbp_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.GBP_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def jpy_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.JPY_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def cny_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.CNY_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def hkd_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.HKD_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def cad_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.CAD_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def aud_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.AUD_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def nzd_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.NZD_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def rub_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.RUB_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def brl_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.BRL_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def chf_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.CHF_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def sek_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.SEK_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def pln_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.PLN_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def krw_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.KRW_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')

    @classmethod
    def twd_to_satoshi(cls):  # pragma: no cover

        for api_call in cls.TWD_RATES:
            try:
                return api_call()
            except cls.IGNORED_ERRORS:
                pass

        raise ConnectionError('All APIs are unreachable.')


EXCHANGE_RATES = {
    'satoshi': satoshi_to_satoshi,
    'uppc': ubtc_to_satoshi,
    'mppc': mbtc_to_satoshi,
    'ppc': btc_to_satoshi,
    'usd': RatesAPI.usd_to_satoshi,
    'eur': RatesAPI.eur_to_satoshi,
    'gbp': RatesAPI.gbp_to_satoshi,
    'jpy': RatesAPI.jpy_to_satoshi,
    'cny': RatesAPI.cny_to_satoshi,
    'cad': RatesAPI.cad_to_satoshi,
    'aud': RatesAPI.aud_to_satoshi,
    'nzd': RatesAPI.nzd_to_satoshi,
    'rub': RatesAPI.rub_to_satoshi,
    'brl': RatesAPI.brl_to_satoshi,
    'chf': RatesAPI.chf_to_satoshi,
    'sek': RatesAPI.sek_to_satoshi,
    'pln': RatesAPI.pln_to_satoshi,
    'hkd': RatesAPI.hkd_to_satoshi,
    'krw': RatesAPI.krw_to_satoshi,
    'twd': RatesAPI.twd_to_satoshi,
}


def currency_to_satoshi(amount, currency):
    """Converts a given amount of currency to the equivalent number of
    satoshi. The amount can be either an int, float, or string as long as
    it is a valid input to :py:class:`decimal.Decimal`.

    :param amount: The quantity of currency.
    :param currency: One of the :ref:`supported currencies`.
    :type currency: ``str``
    :rtype: ``int``
    """
    satoshis = EXCHANGE_RATES[currency]()
    return int(satoshis * Decimal(amount))


class CachedRate:
    __slots__ = ('satoshis', 'last_update')

    def __init__(self, satoshis, last_update):
        self.satoshis = satoshis
        self.last_update = last_update


def currency_to_satoshi_local_cache(f):
    start_time = time()

    cached_rates = dict([
        (currency, CachedRate(None, start_time)) for currency in EXCHANGE_RATES.keys()
    ])

    @wraps(f)
    def wrapper(amount, currency):
        now = time()

        cached_rate = cached_rates[currency]

        if not cached_rate.satoshis or now - cached_rate.last_update > DEFAULT_CACHE_TIME:
            cached_rate.satoshis = EXCHANGE_RATES[currency]()
            cached_rate.last_update = now

        return int(cached_rate.satoshis * Decimal(amount))

    return wrapper


@currency_to_satoshi_local_cache
def currency_to_satoshi_local_cached():
    pass  # pragma: no cover


def currency_to_satoshi_cached(amount, currency):
    """Converts a given amount of currency to the equivalent number of
    satoshi. The amount can be either an int, float, or string as long as
    it is a valid input to :py:class:`decimal.Decimal`. Results are cached
    using a decorator for 60 seconds by default. See :ref:`cache times`.

    :param amount: The quantity of currency.
    :param currency: One of the :ref:`supported currencies`.
    :type currency: ``str``
    :rtype: ``int``
    """
    return currency_to_satoshi_local_cached(amount, currency)


def satoshi_to_currency(num, currency):
    """Converts a given number of satoshi to another currency as a formatted
    string rounded down to the proper number of decimal places.

    :param num: The number of satoshi.
    :type num: ``int``
    :param currency: One of the :ref:`supported currencies`.
    :type currency: ``str``
    :rtype: ``str``
    """
    return '{:f}'.format(
        Decimal(
            num / Decimal(EXCHANGE_RATES[currency]())
        ).quantize(
            Decimal('0.' + '0' * CURRENCY_PRECISION[currency]),
            rounding=ROUND_DOWN
        ).normalize()
    )


def satoshi_to_currency_cached(num, currency):
    """Converts a given number of satoshi to another currency as a formatted
    string rounded down to the proper number of decimal places. Results are
    cached using a decorator for 60 seconds by default. See :ref:`cache times`.

    :param num: The number of satoshi.
    :type num: ``int``
    :param currency: One of the :ref:`supported currencies`.
    :type currency: ``str``
    :rtype: ``str``
    """
    return '{:f}'.format(
        Decimal(
            num / Decimal(currency_to_satoshi_cached(1, currency))
        ).quantize(
            Decimal('0.' + '0' * CURRENCY_PRECISION[currency]),
            rounding=ROUND_DOWN
        ).normalize()
    )
