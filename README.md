# CI/CD Capstone Project

[![CI](https://github.com/Al-AnAti/CI-CD-capstone-project/actions/workflows/ci.yml/badge.svg)](https://github.com/Al-AnAti/CI-CD-capstone-project/actions/workflows/ci.yml)

A small Python application that retrieves data from a REST API and stores it in a SQLite database. The project was built as a practical exercise in GitHub Actions, cross-platform CI, and reliable data ingestion.

## Tech Stack

- Python
- Requests
- SQLite
- GitHub Actions

## How It Works

The application:

1. Fetches posts from JSONPlaceholder.
2. Validates the HTTP response.
3. Parses the returned JSON data.
4. Creates a SQLite database and `posts` table if they do not exist.
5. Inserts the retrieved records while ignoring duplicate IDs.

The database path is resolved relative to the script location using Python's `pathlib`, allowing the application to run consistently across operating systems.

## CI Pipeline

GitHub Actions runs the application automatically on every push using a matrix strategy.

The pipeline tests:

| Operating System | Python Versions |
|---|---|
| Ubuntu | 3.10, 3.11, 3.12 |
| Windows | 3.10, 3.11, 3.12 |

This results in **6 CI environments** being tested for each push.

The workflow:

1. Checks out the repository.
2. Installs the selected Python version.
3. Installs the required dependency.
4. Runs the application.

A failure in any matrix configuration causes the corresponding CI job to fail.

## Engineering Decisions

### Cross-Platform Paths

`pathlib` is used instead of hardcoded filesystem paths. This keeps path handling platform-independent and allows the same script to run on both Windows and Linux.

### Duplicate-Safe Database Insertion

The `id` column is used as the primary key, while records are inserted using `INSERT OR IGNORE`.

This allows the script to be executed repeatedly without failing when a record with the same ID already exists.

### Parameterized SQL

SQL parameters are passed separately from the query rather than constructing SQL statements through string formatting. This is safer and avoids SQL injection risks when handling external data.

### Fail-Fast Behavior

HTTP errors are re-raised after being classified as client/server errors. Because the exception is not swallowed, the Python process exits unsuccessfully and GitHub Actions reports the run as failed.

## Running Locally

Clone the repository and run:

```bash
pip install requests
python main.py
```

The script will create `api_data.db` in the same directory as the application.

## Future Improvements

Possible improvements include:

- Add automated unit tests with `pytest`
- Add dependency pinning
- Add linting and formatting checks
- Add test coverage reporting
- Cache Python dependencies in GitHub Actions
- Separate the application into modules
- Add a build/deployment stage to turn the CI workflow into a complete CI/CD pipeline