import re
from decimal import Decimal
from typing import Iterable, Union

from money.currency import Currency
from money.money import Money

from lazy_budget.constants import DEFAULT_LOCALE

DEFAULT_CURRENCY = Currency.USD
MONEY_AMOUNT_REGEX = r"[+\-]?\d*(\.\d*)?"
MONEY_CURRENCY_REGEX = r"\w{3,}"
MONEY_REGEX = f"{MONEY_AMOUNT_REGEX} {MONEY_CURRENCY_REGEX}"


def format_money(money, locale=DEFAULT_LOCALE) -> str:
    return money.format(locale)


def get_zero(currency: Currency) -> Money:
    return Money("0.00", currency)


def parse_money(
    value: Union[int, float, Decimal, str],
    default_currency: Currency = DEFAULT_CURRENCY,
) -> Money:
    if isinstance(value, (int, float, Decimal)):
        value = str(value)

    if re.fullmatch(MONEY_REGEX, value):
        amount, currency = value.split(" ")
        currency = getattr(Currency, currency.upper())
    elif re.fullmatch(MONEY_AMOUNT_REGEX, value):
        amount = value
        currency = default_currency
    else:
        raise ValueError(f'invalid money format: "{value}"')

    return Money(amount, currency)


def money_mean(money: Iterable[Money], currency: Currency) -> Money:
    money = list(money)
    length = len(money)
    result = get_zero(currency)
    if length == 0:
        return result

    for money_ in money:
        result += money_

    return result / length


def str_to_currency(s: str) -> Currency:
    return getattr(Currency, s)


__all__ = (
    DEFAULT_CURRENCY,
    MONEY_AMOUNT_REGEX,
    MONEY_CURRENCY_REGEX,
    MONEY_REGEX,
    format_money,
    get_zero,
    parse_money,
    money_mean,
    str_to_currency,
)
