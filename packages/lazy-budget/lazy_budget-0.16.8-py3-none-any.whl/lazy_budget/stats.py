from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List

from lazy_budget.budget import Budget, FinancialOperation
from lazy_budget.money_provider import Currency, Money


@dataclass
class BaseBudgetStats(ABC):
    @classmethod
    @abstractmethod
    def get_stats(
        cls, budget: Budget, operations: List[FinancialOperation]
    ) -> "BaseBudgetStats":
        raise NotImplementedError


@dataclass
class BasicBudgetStats(BaseBudgetStats):
    today: date
    total_days: int
    days_left: int
    available_per_day: Money
    can_spend_today: Money
    avg_spent_per_day: Money
    currently_keeping: Money
    spent_today: Money
    currency: Currency
    total_available: Money
    total_spent: Money
    maximum_spent: Money
    days_until_can_spend: int = 0
    budget: Budget = field(compare=False, hash=False, repr=False, default=None)

    @classmethod
    def get_stats(
        cls, budget: Budget, operations: List[FinancialOperation]
    ) -> "BasicBudgetStats":
        if not budget.is_ongoing:
            raise ValueError("there can be no stats for a finished budget")

        operations = budget.filter(operations)
        can_spend_today = budget.get_can_spend_today(operations)
        available_per_day = budget.available_per_day
        total_spent = -sum(
            op.money_value.amount for op in operations if op.dttm.date() <= budget.today
        )
        spent_vals = budget.get_spent_by_day(operations).values()
        maximum_spent = -min(spent_vals) if spent_vals else budget.zero
        return cls(
            today=budget.today,
            total_days=budget.total_days,
            days_left=budget.days_left,
            available_per_day=available_per_day,
            can_spend_today=can_spend_today,
            days_until_can_spend=budget.get_days_until_can_spend(
                can_spend_today, available_per_day
            ),
            avg_spent_per_day=budget.get_avg_spent_per_day(operations),
            currently_keeping=budget.get_currently_keeping(
                can_spend_today=can_spend_today
            ),
            spent_today=budget.get_spent_today(operations),
            currency=budget.currency,
            budget=budget,
            total_available=Money(budget.total.amount - total_spent, budget.currency),
            total_spent=Money(total_spent, budget.currency),
            maximum_spent=maximum_spent,
        )


def get_categories_to_spendings(
    budget: Budget, operations: List[FinancialOperation]
) -> Dict[str, Money]:
    categories_to_spendings = defaultdict(lambda: budget.zero)
    for operation in operations:
        categories_to_spendings[operation.category] += operation.money_value

    return dict(sorted(categories_to_spendings.items(), key=lambda x: x[1]))
