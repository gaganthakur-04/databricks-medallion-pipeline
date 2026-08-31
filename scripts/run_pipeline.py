#!/usr/bin/env python3
"""Databricks job entry point for the Medallion pipeline (Bronze → Silver → Gold)."""

from src.pipeline.run_all import main

if __name__ == "__main__":
    main()
