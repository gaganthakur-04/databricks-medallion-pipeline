"""Bronze layer: ingest orders.csv into bronze.orders."""

from __future__ import annotations

from src.bronze.config import config_from_args, generate_batch_id
from src.bronze.ingest_utils import get_spark, ingest_dataset


def ingest_orders(spark, config, batch_id: str) -> int:
    return ingest_dataset(spark, config, "orders", batch_id)


def main(argv: list[str] | None = None) -> int:
    config = config_from_args(argv)
    batch_id = config.batch_id or generate_batch_id()
    spark = get_spark()
    row_count = ingest_orders(spark, config, batch_id)
    print(f"Ingested {row_count:,} rows into {config.table_name('orders')} (batch_id={batch_id})")
    return row_count


if __name__ == "__main__":
    main()
