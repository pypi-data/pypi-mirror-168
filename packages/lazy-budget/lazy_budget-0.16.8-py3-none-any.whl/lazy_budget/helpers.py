import random
from decimal import Decimal
from math import floor
from statistics import mean, stdev
from typing import Tuple

from termcolor import colored

STD_COEFF = 2.7


def decimal_places_to_bounaries(d: int) -> tuple[int, int]:
    return 10 ** (d - 1), int("9" * d)


def inverse_average(average: Decimal, *a) -> Decimal:
    """In the equation `average = (a1 + a2 + a3 + ... + b) / (len(a) + 1)`, returns b."""
    return average * (len(a) + 1) - sum(a)


def random_decimal(a: int, b: int, decimal_places: int = 2) -> Decimal:
    int_part = random.randint(a, b)
    if int_part == b:
        dec_part = "00"
    else:
        dec_part = random.randint(*decimal_places_to_bounaries(decimal_places))
    return Decimal(f"{int_part}.{dec_part}")


def generate_pair_with_average(
    expected_avg: Decimal, a: Decimal, b: Decimal, decimal_places: int = 2
) -> Tuple[Decimal, Decimal]:
    max_delta = floor(
        min(
            abs(expected_avg - a),
            abs(b - expected_avg),
        )
    )
    delta = random_decimal(0, max_delta, decimal_places)
    return expected_avg - delta, expected_avg + delta


def generate_sequence_by_average_gauss(
    expected_avg: Decimal,
    how_many_numbers: int,
    start: Decimal,
    end: Decimal,
    decimal_places: int = 2,
):
    # buggy version
    sequence = []
    gauss_mean = float(expected_avg)
    gauss_std = float(min((expected_avg - start), (end - expected_avg))) / STD_COEFF
    print(f"{gauss_mean = }; {gauss_std = }")
    for _ in range(how_many_numbers):
        num = round(
            Decimal.from_float(
                random.gauss(
                    gauss_mean,
                    gauss_std,
                )
            ),
            decimal_places,
        )
        sequence.append(num)

    bad_mean = mean(sequence)
    bad_std = stdev(sequence)

    return [
        round(
            expected_avg + (x - bad_mean) * Decimal.from_float(gauss_std) / bad_std,
            decimal_places,
        )
        for x in sequence
    ]


def generate_sequence_by_average_tree(
    expected_avg: Decimal,
    how_many_numbers: int,
    start: Decimal,
    end: Decimal,
    decimal_places: int = 2,
):
    sequence = []
    while len(sequence) < how_many_numbers:
        if how_many_numbers - len(sequence) == 1:
            sequence.append(inverse_average(expected_avg, *sequence))
            break

        n1, n2 = generate_pair_with_average(expected_avg, start, end, decimal_places)
        sequence.extend([n1, n2])

    return sequence


if __name__ == "__main__":
    expected_avg = Decimal("900")
    how_many = 21
    start = Decimal("0")
    end = Decimal("1200")
    print(f"{how_many = }")
    print(f"{expected_avg = }")
    for _ in range(10):
        elements = sorted(
            generate_sequence_by_average_tree(expected_avg, how_many, start, end)
        )
        if any(not (start <= x <= end) for x in elements):
            print(
                "elements =",
                *map(
                    lambda x: colored(str(x), color="red"),
                    elements,
                ),
            )
        else:
            print(
                "elements =",
                *map(
                    lambda x: colored(str(x), color="green"),
                    elements,
                ),
            )

        actual_avg = sum(elements) / len(elements)
        if actual_avg != expected_avg:
            print(
                "actual avg:",
                colored(actual_avg, color="red"),
                "expected:",
                expected_avg,
            )
        else:
            print(
                "actual avg:",
                colored(actual_avg, color="green"),
                "expected:",
                expected_avg,
            )

    # a, b = random_decimal(-10, 10), random_decimal(-10, 10)
    # # a, b = Decimal("4"), Decimal("6")
    # average = (a + b) / 2
    # print(f"{a}, {b}, {average}")

    # print(inverse_average(average, a), "should equal to", b)
    # print(inverse_average(average, b), "should equal to", a)
