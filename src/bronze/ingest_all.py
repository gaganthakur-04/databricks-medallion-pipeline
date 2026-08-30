"""Bronze layer: ingest all source CSVs into Bronze Delta tables."""

from __future__ import annotations

from src.bronze.config import EXPECTED_ROW_COUNTS, config_from_args, generate_batch_id
from src.bronze.ingest_utils import get_spark, ingest_all_datasets


def main(argv: list[str] | None = None) -> dict[str, int]:
    config = config_from_args(argv)
    batch_id = config.batch_id or generate_batch_id()
    spark = get_spark()

    print(f"Bronze ingest starting (batch_id={batch_id})")
    print(f"  input_dir : {config.input_dir}")
    print(f"  database  : {config.database}")

    results = ingest_all_datasets(spark, config, batch_id)

    print("\nBronze ingest complete:")
    for entity, count in results.items():
        expected = EXPECTED_ROW_COUNTS[entity]
        status = "OK" if count == expected else f"EXPECTED {expected:,}"
        print(f"  {config.table_name(entity)}: {count:,} rows ({status})")

    return results


if __name__ == "__main__":
    main()
