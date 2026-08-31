"""Bundle configuration and packaging tests."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_databricks_yml_exists():
    bundle_path = REPO_ROOT / "databricks.yml"
    content = bundle_path.read_text(encoding="utf-8")
    assert bundle_path.exists()
    assert "name: medallion-pipeline" in content
    assert "targets:" in content
    assert "dev:" in content


def test_job_resource_file_exists():
    job_path = REPO_ROOT / "resources" / "medallion_pipeline.job.yml"
    content = job_path.read_text(encoding="utf-8")
    assert job_path.exists()
    assert "setup_schema" in content
    assert "run_pipeline" in content
    assert "medallion_pipeline" in content


def test_bundle_scripts_exist():
    assert (REPO_ROOT / "scripts" / "run_pipeline.py").exists()
    assert (REPO_ROOT / "scripts" / "setup_schema.py").exists()


def test_sync_excludes_sensitive_and_local_paths():
    content = (REPO_ROOT / "databricks.yml").read_text(encoding="utf-8")
    assert "data/**" in content
    assert ".venv/**" in content


def test_pipeline_entry_point_exists():
    run_all_path = REPO_ROOT / "src" / "pipeline" / "run_all.py"
    content = run_all_path.read_text(encoding="utf-8")
    assert run_all_path.exists()
    assert "def main" in content
    assert "bronze_main" in content


def test_setup_schema_splits_sql():
    from scripts.setup_schema import _split_sql_statements

    statements = _split_sql_statements("CREATE DATABASE bronze;\n-- comment\nCREATE TABLE t (id INT);")
    assert len(statements) == 2
    assert statements[0].startswith("CREATE DATABASE")

    # Semicolons inside SQL comments must not create extra statements.
    statements = _split_sql_statements(
        "CREATE DATABASE silver;\n-- note; populated later\nCREATE TABLE silver.t (id INT);"
    )
    assert len(statements) == 2
    assert statements[1].startswith("CREATE TABLE")
