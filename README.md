# Title

[![matrix ci](https://github.com/Al-AnAti/CI-CD-capstone-project/actions/workflows/ci.yml/badge.svg)](https://github.com/Al-AnAti/CI-CD-capstone-project/actions/workflows/ci.yml)

## System Architecture & Engineering Principles

This project serves as a validation pipeline to demonstrate robust CI/CD practices, automated cross-OS testing, and safe database operations. The architecture was designed around three core DevOps principles:

### 1. Matrix Automation & Cross-OS Compatibility
The CI/CD pipeline utilizes a GitHub Actions Matrix Strategy to ensure absolute cross-platform stability. On every repository push, the workflow spins up 6 concurrent runners:
* **Operating Systems:** `ubuntu-latest`, `windows-latest`
* **Environments:** Python 3.10, 3.11, 3.12

To support this OS-agnostic execution, the application utilizes dynamic absolute pathing via Python's `pathlib`. This eliminates brittle relative paths and hardcoded slashes, ensuring the database correctly initializes in the exact execution directory regardless of whether the host OS uses forward slashes (Linux) or backslashes (Windows).

### 2. Idempotent Database Operations
In an automated pipeline, scripts are executed repeatedly (via schedules, triggers, or retries). The database interactions are strictly idempotent, meaning the script can run 1 time or 10,000 times without generating duplicate records or corrupting the schema.
* **Mechanism:** The SQLite schema strictly enforces a `PRIMARY KEY` constraint on the dataset ID. The ingestion engine executes `INSERT OR IGNORE` parameterized queries.
* **Result:** Re-running the pipeline safely updates the local state without throwing constraint violation errors or duplicating existing ingested payload data.

### 3. Fail-Fast Integration
Silent failures in automated pipelines lead to false-positive green builds. The API extraction layer is designed to "fail loudly." If the external data source returns a 404 or 500-level HTTP status, the exception is intentionally re-raised to force a non-zero exit code (`1`). This ensures the GitHub Actions runner immediately halts and correctly flags the job as a failure, preventing compromised data from advancing down the pipeline.