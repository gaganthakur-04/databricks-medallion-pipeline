"""Configuration for Gold transformations."""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class GoldConfig:
    silver_database: str = "silver"
    gold_database: str = "gold"

    def silver_table(self, entity: str) -> str:
        return f"{self.silver_database}.{entity}"

    def gold_table(self, name: str) -> str:
        return f"{self.gold_database}.{name}"


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gold layer business aggregations")
    parser.add_argument(
        "--silver-database",
        default=os.environ.get("SILVER_DATABASE", "silver"),
        help="Source Hive database (default: silver)",
    )
    parser.add_argument(
        "--gold-database",
        default=os.environ.get("GOLD_DATABASE", "gold"),
        help="Target Hive database (default: gold)",
    )
    return parser


def config_from_args(argv: list[str] | None = None) -> GoldConfig:
    args = build_arg_parser().parse_args(argv)
    return GoldConfig(
        silver_database=args.silver_database,
        gold_database=args.gold_database,
    )
