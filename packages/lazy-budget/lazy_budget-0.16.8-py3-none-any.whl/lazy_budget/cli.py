import os
import subprocess
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from os import PathLike
from os.path import expanduser

import yaml

from lazy_budget.budget import Budget, FinancialOperation
from lazy_budget.charts import BurnDownChart, CategoryBarPlot
from lazy_budget.constants import (
    BUDGET_FILE,
    CONFIG_FILE_PATH,
    DEFAULT_LOCALE,
    HISTORY_FILE,
)
from lazy_budget.display import (
    BasicStatsDisplay,
    NextDaysDisplay,
    SpentByCategoryDisplay,
)
from lazy_budget.money_provider import DEFAULT_CURRENCY, parse_money, str_to_currency
from lazy_budget.stats import BasicBudgetStats


def do_nothing(args):
    print("specify a valid operation!")
    exit(2)


def _get_budget(args) -> Budget:
    return Budget.from_file(args.budget_file, args.currency, args.today)


def _get_history(args) -> FinancialOperation:
    return FinancialOperation.from_file(args.history_file, args.currency)


def add_new_operation(args):
    budget = _get_budget(args)
    op = FinancialOperation(
        money_value=parse_money(args.value, budget.currency),
        description=args.description,
        dttm=datetime.fromisoformat(args.dttm),
    )
    op.save(args.history_file)


def list_stats(args):
    budget = _get_budget(args)
    ops = _get_history(args)
    stats = BasicBudgetStats.get_stats(budget=budget, operations=ops)
    display = BasicStatsDisplay(budget_stats=stats, locale=args.locale)
    print(display)


def spendings_by_category(args):
    budget = _get_budget(args)
    ops = _get_history(args)
    display = SpentByCategoryDisplay(budget=budget, operations=ops, locale=args.locale)
    print(display)


def show_burndown_chart(args):
    budget = _get_budget(args)
    ops = _get_history(args)
    chart = BurnDownChart(
        budget=budget,
        operations=ops,
        show_zero=args.show_zero,
        savings=args.savings,
        show_both=args.show_both,
        whole_budget=args.whole_budget,
    )
    chart.plot()


def show_category_chart(args):
    budget = _get_budget(args)
    ops = _get_history(args)
    chart = CategoryBarPlot(budget=budget, operations=ops)
    chart.plot()


def edit_budget(args):
    exit(subprocess.call([os.getenv("EDITOR"), args.budget_file]))


def edit_history(args):
    exit(subprocess.call([os.getenv("EDITOR"), args.history_file]))


def next_days(args):
    budget = _get_budget(args)
    ops = _get_history(args)
    stats = BasicBudgetStats.get_stats(budget=budget, operations=ops)
    display = NextDaysDisplay(
        budget_stats=stats,
        locale=args.locale,
        how_many_days=args.N,
        factor_in_average_spendings=args.factor_in_average_spendings
        or args.no_spendings_today,
        no_spendings_today=args.no_spendings_today,
        prediction_coeff=args.prediction_coeff,
    )
    print(display)


def save_file(args):
    budget = _get_budget(args)
    ops = _get_history(args)
    chart = BurnDownChart(
        budget=budget,
        operations=ops,
        show_zero=args.show_zero,
        savings=args.savings,
        show_both=args.show_both,
        whole_budget=args.whole_budget,
    )
    b = chart.get_file()
    with open("img.png", "wb") as fp:
        fp.write(b)


@dataclass
class CLIConfig:
    history_file: PathLike = HISTORY_FILE
    budget_file: PathLike = BUDGET_FILE
    locale: str = DEFAULT_LOCALE
    currency: str = DEFAULT_CURRENCY.name

    def get_args(self, argv=None):
        parser = ArgumentParser()
        parser.add_argument(
            "-f",
            "--history-file",
            help=f"history file to use (default is {self.history_file})",
            default=self.history_file,
        )
        parser.add_argument(
            "-c",
            "--budget-file",
            help=f"budget file to use (default is {self.budget_file})",
            default=self.budget_file,
        )
        parser.add_argument(
            "-L",
            "--locale",
            help=f"locale to use (default is {self.locale})",
            default=self.locale,
        )
        parser.add_argument(
            "-C",
            "--currency",
            help=f"default currency to use in uncertain situations (default is {self.currency})",
            default=self.currency,
            type=str_to_currency,
        )
        parser.add_argument(
            "-t",
            "--today",
            help='a date used as "today" during stats, useful for seeing old budget info',
            type=date.fromisoformat,
            default=None,
        )

        parser.set_defaults(action_func=lambda args: None)
        subparsers = parser.add_subparsers(help="budget operation to perform")

        parser_savefile = subparsers.add_parser("save")
        parser_savefile.add_argument(
            "-z",
            "--show-zero",
            action="store_true",
            default=False,
            help="plot or show the zero line",
        )
        parser_savefile.add_argument(
            "-s",
            "--savings",
            action="store_true",
            default=False,
            help="plot savings instead of spendings",
        )
        parser_savefile.add_argument(
            "-S",
            "--show-both",
            action="store_true",
            default=False,
            help="plot both savings and spendings",
        )
        parser_savefile.add_argument(
            "-w",
            "--whole-budget",
            action="store_true",
            default=False,
            help="plot whole budgeting period instead of until today",
        )
        parser_savefile.set_defaults(action_func=save_file)
        parser_add = subparsers.add_parser(
            "add", aliases=["a", "new", "n"], help="add a new financial operation"
        )
        parser_add.set_defaults(action_func=add_new_operation)
        parser_add.add_argument(
            "value",
            help='amount (and optionally currency) of financial operation, e.g. "-10.99 USD", "2.50", "+3.65"',
        )
        parser_add.add_argument("description")
        parser_add.add_argument(
            "dttm",
            nargs="?",
            default=datetime.now().isoformat(),
            help="date and time of the operation; now is default",
        )

        parser_today = subparsers.add_parser(
            "list-stats",
            aliases=["ls", "now", "today", "list", "stats", "s", "get"],
            help="list statistics",
        )
        parser_today.set_defaults(action_func=list_stats)

        parser_burndown = subparsers.add_parser(
            "burndown", aliases=["bd"], help="shows a burndown chart of the budget"
        )
        parser_burndown.add_argument(
            "-z",
            "--show-zero",
            action="store_true",
            default=False,
            help="plot or show the zero line",
        )
        parser_burndown.add_argument(
            "-s",
            "--savings",
            action="store_true",
            default=False,
            help="plot savings instead of spendings",
        )
        parser_burndown.add_argument(
            "-S",
            "--show-both",
            action="store_true",
            default=False,
            help="plot both savings and spendings",
        )
        parser_burndown.add_argument(
            "-w",
            "--whole-budget",
            action="store_true",
            default=False,
            help="plot whole budgeting period instead of until today",
        )
        parser_burndown.set_defaults(action_func=show_burndown_chart)

        parser_categories = subparsers.add_parser(
            "categories", aliases=["cats"], help="display money flow by category"
        )
        parser_categories.set_defaults(action_func=spendings_by_category)

        parser_categories = subparsers.add_parser(
            "category-chart",
            aliases=["catsc", "catc", "cat-chart"],
            help="display money flow by category in a chart",
        )
        parser_categories.set_defaults(action_func=show_category_chart)

        parser_edit_budget = subparsers.add_parser(
            "edit-budget",
            aliases=["eb"],
            help="edit the budget file",
        )
        parser_edit_budget.set_defaults(action_func=edit_budget)

        parser_edit_history = subparsers.add_parser(
            "edit-history",
            aliases=["eh"],
            help="edit the history file",
        )
        parser_edit_history.set_defaults(action_func=edit_history)

        parser_next_days = subparsers.add_parser(
            "next-days",
            aliases=["nd"],
            help="view how much will you be able to spend during the next N days",
        )
        parser_next_days.add_argument(
            "N",
            nargs="?",
            type=int,
            default=5,
            help="how many days of stats to show (default = 5)",
        )
        parser_next_days.add_argument(
            "-f",
            "--factor-in-average-spendings",
            help="try to predict how you are gonna spend during the next N days",
            action="store_true",
            default=False,
        )
        parser_next_days.add_argument(
            "-n",
            "--no-spendings-today",
            help="when predicting spendings, today will not contain any spendings",
            action="store_true",
            default=False,
        )
        parser_next_days.add_argument(
            "-p",
            "--prediction-coeff",
            help="a number to multiply average spendings by",
            type=Decimal,
            default=Decimal("1"),
        )
        parser_next_days.set_defaults(action_func=next_days)

        parser_help = subparsers.add_parser(
            "help",
            aliases=["h"],
            help="show this help",
        )
        parser_help.set_defaults(action_func=lambda *args: parser.print_help())

        return parser.parse_args(argv)

    @classmethod
    def from_file(cls, filename: PathLike = None) -> "CLIConfig":
        if not filename:
            filename = os.getenv("LBUDRC") or expanduser(CONFIG_FILE_PATH)

        try:
            with open(filename, "r") as fp:
                data = yaml.safe_load(fp)
        except IOError:
            print(f"config file not found at {filename}, using the defaults")
            return cls()

        return cls(**data)
