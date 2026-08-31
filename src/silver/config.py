"""Configuration for Silver validation."""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class SilverConfig:
    bronze_database: str = "bronze"
    silver_database: str = "silver"

    def bronze_table(self, entity: str) -> str:
        return f"{self.bronze_database}.{entity}"

    def silver_table(self, entity: str) -> str:
        return f"{self.silver_database}.{entity}"


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Silver layer data-quality validation")
    parser.add_argument(
        "--bronze-database",
        default=os.environ.get("BRONZE_DATABASE", "bronze"),
        help="Source Hive database (default: bronze)",
    )
    parser.add_argument(
        "--silver-database",
        default=os.environ.get("SILVER_DATABASE", "silver"),
        help="Target Hive database (default: silver)",
    )
    return parser


def config_from_args(argv: list[str] | None = None) -> SilverConfig:
    args = build_arg_parser().parse_args(argv)
    return SilverConfig(
        bronze_database=args.bronze_database,
        silver_database=args.silver_database,
    )
