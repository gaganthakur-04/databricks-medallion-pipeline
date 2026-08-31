#!/usr/bin/env python3
"""Apply Hive metastore schema DDL from the synced bundle (idempotent)."""

from __future__ import annotations

import argparse
from pathlib import Path


def _repo_root(bundle_root: str | None = None) -> Path:
    if bundle_root:
        return Path(bundle_root)
    return Path(__file__).resolve().parent.parent


def _strip_sql_comments(sql_text: str) -> str:
    """Remove line comments so semicolons inside comments do not split statements."""
    lines: list[str] = []
    for line in sql_text.splitlines():
        if "--" in line:
            line = line[: line.index("--")]
        lines.append(line)
    return "\n".join(lines)


def _split_sql_statements(sql_text: str) -> list[str]:
    statements: list[str] = []
    for chunk in _strip_sql_comments(sql_text).split(";"):
        lines = [line for line in chunk.splitlines() if not line.strip().startswith("--")]
        stmt = "\n".join(lines).strip()
        if stmt:
            statements.append(stmt)
    return statements


def main(argv: list[str] | None = None) -> None:
    from pyspark.sql import SparkSession

    parser = argparse.ArgumentParser(description="Apply Community Edition schema DDL")
    parser.add_argument(
        "--bundle-root",
        default=None,
        help="Synced bundle files root on Databricks (required for serverless spark_python_task)",
    )
    args = parser.parse_args(argv)

    spark = SparkSession.builder.getOrCreate()
    schema_path = _repo_root(args.bundle_root) / "database" / "schema_community_edition.sql"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    sql_text = schema_path.read_text(encoding="utf-8")
    statements = _split_sql_statements(sql_text)
    print(f"Applying {len(statements)} schema statements from {schema_path.name}")
    for stmt in statements:
        spark.sql(stmt)
    print("Schema setup complete")


if __name__ == "__main__":
    main()
