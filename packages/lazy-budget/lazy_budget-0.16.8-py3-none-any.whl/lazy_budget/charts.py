from abc import abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from io import BytesIO
from itertools import takewhile
from typing import Iterable

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from pandas.core.frame import DataFrame

from lazy_budget.budget import Budget, FinancialOperation
from lazy_budget.stats import get_categories_to_spendings


@dataclass
class BaseChart:
    budget: Budget
    operations: Iterable[FinancialOperation]

    def plot(self):
        df = self.get_dataframe()
        self.display_dataframe(df)
        plt.show()

    def get_file(self) -> bytes:
        df = self.get_dataframe()
        self.display_dataframe(df)
        bio = BytesIO()
        plt.savefig(bio, dpi=600, format="png")
        plt.close()
        return bio.getvalue()

    @abstractmethod
    def get_dataframe(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def display_dataframe(self, dataframe: pd.DataFrame):
        pass


@dataclass
class BurnDownChart(BaseChart):
    show_zero: bool = False
    savings: bool = False
    show_both: bool = False
    whole_budget: bool = False

    def get_dataframe(self):
        max_date = self.budget.end if self.whole_budget else self.budget.today
        operations = self.budget.filter(self.operations)
        spent_per_day = self.budget.get_spent_by_day(operations)
        for_df = []
        total_spent = self.budget.total.amount
        budget = deepcopy(self.budget)
        for day in takewhile(lambda x: x <= max_date, iter(budget)):
            budget.today = day
            ops = budget.filter(operations)
            total_spent += spent_per_day[day].amount
            should_be_available = (
                budget.days_left * budget.available_per_day.amount + budget.keep.amount
            )

            for_df.append(
                (
                    day.strftime("%d"),
                    total_spent,
                    should_be_available,
                    0,
                    budget.available_per_day.amount,
                    budget.get_currently_keeping(ops).amount,
                    budget.keep.amount,
                )
            )

        return pd.DataFrame(
            for_df,
            columns=[
                "day",
                "money",
                "should_be_available",
                "zero",
                "available_per_day",
                "currently_keeping",
                "keep",
            ],
        )

    def display_dataframe(self, dataframe: DataFrame):
        sns.set_theme()
        sns.set_style("darkgrid")

        if self.savings or self.show_both:
            plt.plot(
                "day",
                "currently_keeping",
                data=dataframe,
                color="green",
                label="real savings",
            )
            plt.plot(
                "day",
                "keep",
                data=dataframe,
                color="green",
                linestyle=":",
                label="planned savings",
            )
        if not self.savings or self.show_both:
            plt.plot("day", "money", data=dataframe, color="red", label="real burndown")
            plt.plot(
                "day",
                "should_be_available",
                data=dataframe,
                linestyle="dotted",
                color="red",
                label="planned burndown",
            )

        if self.show_zero:
            plt.plot("day", "zero", data=dataframe, linestyle="dashed")

        if self.whole_budget:
            max_date = self.budget.today
            plt.axvline(
                x=max_date.strftime("%d"), linestyle=(0, (5, 10)), label="today"
            )

        plt.legend()
        plt.xlabel("Day of month")
        plt.ylabel(f"Spendings, {self.budget.currency.name}")


class CategoryBarPlot(BaseChart):
    def get_dataframe(self) -> pd.DataFrame:
        operations = self.budget.filter(self.operations)
        sps = get_categories_to_spendings(self.budget, operations)
        return pd.DataFrame(
            map(lambda x: (x[0], x[1].amount), sps.items()),
            columns=["category", "money_spent"],
        )

    def display_dataframe(self, dataframe: pd.DataFrame):
        sns.set(style="darkgrid")

        # Set the figure size
        # plt.figure(figsize=(10, 7))

        # plot a bar chart
        ax = sns.barplot(
            x="category",
            y="money_spent",
            data=dataframe,
            estimator=sum,
            ci=None,
            color="#69b3a2",
        )
        ax.set(xlabel="category", ylabel=f"money spent, {self.budget.currency.name}")
        plt.gca().invert_yaxis()
