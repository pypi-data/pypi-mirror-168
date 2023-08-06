#!/usr/bin/env python
import os

from lazy_budget.cli import CLIConfig


def main():
    config = CLIConfig.from_file()
    args = config.get_args()
    if not os.path.isfile(args.budget_file):
        print(f"No budget file found at {args.budget_file}, exiting.")
        exit(1)

    args.action_func(args)


if __name__ == "__main__":
    main()
