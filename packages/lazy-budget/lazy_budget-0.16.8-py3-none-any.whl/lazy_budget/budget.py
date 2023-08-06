import csv
import os
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from functools import partial
from math import ceil
from typing import ClassVar, Dict, Generator, Iterable, List, Tuple, Union

import yaml

from lazy_budget.money_provider import (
    DEFAULT_CURRENCY,
    Currency,
    Money,
    get_zero,
    money_mean,
    parse_money,
)


@dataclass
class FinancialOperation:
    money_value: Money
    description: str = ""
    dttm: datetime = field(default_factory=datetime.now)
    category: str = None

    CSV_FIELD_NAMES: ClassVar[List[str]] = ["money_value", "description", "dttm"]

    @property
    def currency(self) -> Currency:
        return self.money_value.currency

    @classmethod
    def from_row(cls, row, default_currency: Currency = DEFAULT_CURRENCY):
        money_value = parse_money(row["money_value"], default_currency)
        category, description = cls.parse_description(row["description"])
        return cls(
            money_value=money_value,
            description=description,
            dttm=datetime.fromisoformat(row["dttm"]),
            category=category,
        )

    @classmethod
    def parse_description(cls, raw_description: str) -> Tuple[str, str]:
        description_pattern = r"\[(.*)\]\s*(.*)"
        match = re.fullmatch(description_pattern, raw_description)
        category, description = match.groups() if match else (None, raw_description)
        category = category or None
        return category, description

    @classmethod
    def from_file(
        cls, filename: os.PathLike, default_currency: Currency = DEFAULT_CURRENCY
    ) -> None:
        with open(filename, "r") as fp:
            reader = csv.DictReader(fp, fieldnames=cls.CSV_FIELD_NAMES)
            yield from map(
                partial(cls.from_row, default_currency=default_currency), reader
            )

    def save(self, filename: os.PathLike) -> None:
        mode = "a" if os.path.isfile(filename) else "w"
        with open(filename, mode) as fp:
            writer = csv.DictWriter(fp, fieldnames=self.CSV_FIELD_NAMES)
            writer.writerow(
                {
                    "money_value": self.money_value.amount,
                    "description": (
                        f"[{self.category}] {self.description}"
                        if self.category
                        else self.description
                    ),
                    "dttm": self.dttm,
                }
            )


@dataclass
class Budget:
    total: Money
    keep: Money
    start: date
    end: date
    currency: Currency = Currency.USD
    today: date = None

    def __post_init__(self):
        if not self.today:
            self.today = date.today()

    def __contains__(self, item: Union[date, datetime]) -> bool:
        if isinstance(item, datetime):
            item = item.date()
        elif not isinstance(item, date):
            raise TypeError(
                f"cannot determine if an instance of class {item.__class__.__name__} is within a budget"
            )

        return self.start <= item <= self.end

    def __iter__(self) -> Generator[date, None, None]:
        """
        Returns an Iterable of dates within this budget.
        """
        return (
            self.end - timedelta(days=num_days)
            for num_days in range(self.total_days - 1, -1, -1)
        )

    @property
    def zero(self):
        return get_zero(self.currency)

    @property
    def past_days(self) -> Generator[date, None, None]:
        return filter(lambda x: x <= self.today, iter(self))

    @property
    def is_ongoing(self) -> bool:
        return self.today in self

    @property
    def total_days(self) -> int:
        return (self.end - self.start + timedelta(days=1)).days

    @property
    def total_available(self) -> Money:
        return self.total - self.keep

    @property
    def days_left(self) -> int:
        return (self.end - self.today).days

    @property
    def available_per_day(self) -> Money:
        return self.total_available / self.total_days

    def get_spent_by_day(
        self, operations: List[FinancialOperation]
    ) -> Dict[date, Money]:
        result = defaultdict(lambda: self.zero)
        days = list(self.past_days)
        for operation in filter(lambda op: op.dttm.date() in days, operations):
            result[operation.dttm.date()] += operation.money_value

        return result

    def get_currently_keeping(
        self,
        operations: Iterable[FinancialOperation] = None,
        can_spend_today: Money = None,
    ) -> Money:
        can_spend_today = can_spend_today or self.get_can_spend_today(operations)
        return self.keep + can_spend_today

    def get_avg_spent_per_day(self, operations: List[FinancialOperation]) -> Money:
        # TODO test
        spent_by_day = self.get_spent_by_day(operations)
        return -money_mean((spent_by_day[day] for day in self.past_days), self.currency)

    def get_can_spend_today(self, operations: List[FinancialOperation]) -> Money:
        # TODO test
        progress = self.zero
        spent_by_day = self.get_spent_by_day(operations)
        for day in self.past_days:
            progress += self.available_per_day + spent_by_day[day]

        return progress

    def get_days_until_can_spend(
        self, can_spend_today: Money, available_per_day: Money
    ) -> int:
        # TODO test
        if can_spend_today >= self.zero:
            return 0

        return int(ceil(-can_spend_today / available_per_day))

    def get_spent_today(self, operations: List[FinancialOperation]) -> Money:
        spent_by_day = self.get_spent_by_day(operations)
        spent_today = spent_by_day[self.today]
        return -spent_today if spent_today < self.zero else spent_today

    @classmethod
    def from_file(
        cls,
        filename: os.PathLike,
        default_currency: Currency = DEFAULT_CURRENCY,
        today: date = None,
    ) -> None:
        # TODO test
        with open(filename, "r") as fp:
            data = yaml.safe_load(fp)

        currency_name = data.get("currency")
        currency = getattr(Currency, currency_name.upper(), default_currency)
        if not today:
            today = date.today()

        return cls(
            total=parse_money(data["total"], default_currency=currency),
            keep=parse_money(data["keep"], default_currency=currency),
            start=data["start"],
            end=data["end"],
            currency=currency,
            today=today,
        )

    def filter(self, operations: List[FinancialOperation]) -> List[FinancialOperation]:
        # TODO test
        return list(
            filter(
                lambda op: op.dttm.date() in self and op.currency == self.currency,
                operations,
            )
        )
