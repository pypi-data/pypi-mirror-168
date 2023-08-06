from lazy_budget.constants import DAYS_IN_A_SECOND


def timedelta_to_days(seconds) -> int:
    return int(seconds * DAYS_IN_A_SECOND)
