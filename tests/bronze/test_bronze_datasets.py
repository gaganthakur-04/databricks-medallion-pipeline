"""Tests for Bronze dataset configuration (no Spark required)."""

from src.bronze.config import DATASETS, EXPECTED_ROW_COUNTS


def test_datasets_and_expected_counts_aligned():
    assert set(DATASETS.keys()) == set(EXPECTED_ROW_COUNTS.keys())
    assert EXPECTED_ROW_COUNTS["customers"] == 10_000
    assert EXPECTED_ROW_COUNTS["orders"] == 100_000
    assert EXPECTED_ROW_COUNTS["products"] == 500
