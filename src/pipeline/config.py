"""End-to-end pipeline configuration."""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass

from src.bronze.config import default_input_dir


@dataclass(frozen=True)
class PipelineConfig:
    input_dir: str
    bronze_database: str = "bronze"
    silver_database: str = "silver"
    gold_database: str = "gold"
    batch_id: str | None = None
    skip_bronze: bool = False


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Bronze → Silver → Gold pipeline")
    parser.add_argument("--input-dir", default=default_input_dir())
    parser.add_argument("--bronze-database", default=os.environ.get("BRONZE_DATABASE", "bronze"))
    parser.add_argument("--silver-database", default=os.environ.get("SILVER_DATABASE", "silver"))
    parser.add_argument("--gold-database", default=os.environ.get("GOLD_DATABASE", "gold"))
    parser.add_argument("--batch-id", default=None)
    parser.add_argument("--skip-bronze", action="store_true", help="Run Silver and Gold only")
    return parser


def config_from_args(argv: list[str] | None = None) -> PipelineConfig:
    args = build_arg_parser().parse_args(argv)
    return PipelineConfig(
        input_dir=args.input_dir,
        bronze_database=args.bronze_database,
        silver_database=args.silver_database,
        gold_database=args.gold_database,
        batch_id=args.batch_id,
        skip_bronze=args.skip_bronze,
    )
