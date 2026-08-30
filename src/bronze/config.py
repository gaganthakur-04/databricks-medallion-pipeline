"""Configuration for Bronze CSV ingestion."""

from __future__ import annotations

import argparse
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


def default_input_dir() -> str:
    """Return default CSV input directory for Databricks CE or local development."""
    if Path("/databricks").exists():
        return "dbfs:/FileStore/ecommerce/raw"
    return str(Path(__file__).resolve().parents[2] / "data")


def generate_batch_id() -> str:
    """Create a unique batch identifier for a single ingest run."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{ts}_{uuid.uuid4().hex[:8]}"


DATASETS: dict[str, str] = {
    "customers": "customers.csv",
    "orders": "orders.csv",
    "products": "products.csv",
}

EXPECTED_ROW_COUNTS: dict[str, int] = {
    "customers": 10_000,
    "orders": 100_000,
    "products": 500,
}


@dataclass(frozen=True)
class BronzeConfig:
    input_dir: str
    database: str = "bronze"
    batch_id: str | None = None

    def csv_path(self, filename: str) -> str:
        base = self.input_dir.rstrip("/")
        if base.startswith("dbfs:"):
            return f"{base}/{filename}"
        return str(Path(base) / filename)

    def table_name(self, entity: str) -> str:
        return f"{self.database}.{entity}"


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bronze layer CSV ingestion")
    parser.add_argument(
        "--input-dir",
        default=default_input_dir(),
        help="Directory containing customers.csv, orders.csv, products.csv",
    )
    parser.add_argument(
        "--database",
        default=os.environ.get("BRONZE_DATABASE", "bronze"),
        help="Hive database for Bronze tables (default: bronze)",
    )
    parser.add_argument(
        "--batch-id",
        default=None,
        help="Optional batch id; auto-generated if omitted",
    )
    return parser


def config_from_args(argv: list[str] | None = None) -> BronzeConfig:
    args = build_arg_parser().parse_args(argv)
    return BronzeConfig(
        input_dir=args.input_dir,
        database=args.database,
        batch_id=args.batch_id,
    )
