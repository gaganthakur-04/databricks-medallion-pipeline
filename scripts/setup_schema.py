#!/usr/bin/env python3
"""Apply Hive metastore schema DDL from the synced bundle (idempotent)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _split_sql_statements(sql_text: str) -> list[str]:
    statements: list[str] = []
    for chunk in sql_text.split(";"):
        lines = [line for line in chunk.splitlines() if not line.strip().startswith("--")]
        stmt = "\n".join(lines).strip()
        if stmt:
            statements.append(stmt)
    return statements


def main() -> None:
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()
    schema_path = _repo_root() / "database" / "schema_community_edition.sql"
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
