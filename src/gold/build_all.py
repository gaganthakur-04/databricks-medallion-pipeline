"""Gold layer: build all Gold aggregation tables from Silver."""

from __future__ import annotations

from src.gold.config import config_from_args
from src.gold.transforms import build_all_gold_tables, get_spark


def main(argv: list[str] | None = None) -> dict[str, int]:
    config = config_from_args(argv)
    spark = get_spark()

    print("Gold build starting")
    print(f"  silver_database : {config.silver_database}")
    print(f"  gold_database   : {config.gold_database}")

    results = build_all_gold_tables(spark, config)

    print("\nGold build complete:")
    for table, count in results.items():
        print(f"  {config.gold_table(table)}: {count:,} rows")

    return results


if __name__ == "__main__":
    main()
