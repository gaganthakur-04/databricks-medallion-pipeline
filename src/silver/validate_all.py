"""Silver layer: orchestrate all quality checks and write Silver tables."""

from __future__ import annotations

from src.bronze.config import EXPECTED_ROW_COUNTS
from src.silver.config import config_from_args
from src.silver.quality_metrics import print_quality_metrics
from src.silver.transforms import get_spark, validate_all_entities


def main(argv: list[str] | None = None) -> dict[str, int]:
    config = config_from_args(argv)
    spark = get_spark()

    print("Silver validation starting")
    print(f"  bronze_database : {config.bronze_database}")
    print(f"  silver_database : {config.silver_database}")

    results = validate_all_entities(spark, config)

    print("\nSilver validation complete:")
    for entity, count in results.items():
        expected = EXPECTED_ROW_COUNTS[entity]
        status = "OK" if count == expected else f"EXPECTED {expected:,}"
        print(f"  {config.silver_table(entity)}: {count:,} rows ({status})")

    print_quality_metrics(spark, config)
    return results


if __name__ == "__main__":
    main()
