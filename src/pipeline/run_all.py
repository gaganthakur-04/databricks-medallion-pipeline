"""Run Bronze → Silver → Gold end-to-end."""

from __future__ import annotations

from src.bronze.config import generate_batch_id
from src.bronze.ingest_all import main as bronze_main
from src.gold.build_all import main as gold_main
from src.pipeline.config import config_from_args
from src.silver.validate_all import main as silver_main


def main(argv: list[str] | None = None) -> dict[str, object]:
    config = config_from_args(argv)
    batch_id = config.batch_id or generate_batch_id()

    print("=" * 60)
    print("Medallion pipeline starting")
    print("=" * 60)

    results: dict[str, object] = {}

    if not config.skip_bronze:
        print("\n[1/3] Bronze ingestion")
        results["bronze"] = bronze_main(
            [
                "--input-dir",
                config.input_dir,
                "--database",
                config.bronze_database,
                "--batch-id",
                batch_id,
            ]
        )
    else:
        print("\n[1/3] Bronze ingestion skipped")

    print("\n[2/3] Silver validation")
    results["silver"] = silver_main(
        [
            "--bronze-database",
            config.bronze_database,
            "--silver-database",
            config.silver_database,
        ]
    )

    print("\n[3/3] Gold aggregations")
    results["gold"] = gold_main(
        [
            "--silver-database",
            config.silver_database,
            "--gold-database",
            config.gold_database,
        ]
    )

    print("\n" + "=" * 60)
    print("Medallion pipeline complete")
    print("=" * 60)
    return results


if __name__ == "__main__":
    main()
