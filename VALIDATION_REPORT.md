# Validation report — v1.1

## Evidence — 2026-11-26

GitHub Actions workflow Tests #7 displayed a successful result in the repository [81bf596](https://github.com/DgAlkan/customer-journey-intelligence/commit/81bf5966c213eaa794b59c7cf7fbd47bb55d9112). The workflow executes pytest, including Python, DuckDB integration and Streamlit AppTest checks. The earlier AppTest relative-path failure was corrected using an absolute path derived from the test file.

Evidence source: owner-provided screenshot of the Actions overview; detailed final test logs were not independently retrieved. This confirms the workflow result, not exhaustive coverage.

## Remaining checks

Manual visual and interaction review, performance benchmarks, publication review and deployment remain pending. Synthetic data only.

## Reproduce

```bash
pip install -r requirements.txt
python -m pytest -v
```

[Actions history](https://github.com/DgAlkan/customer-journey-intelligence/actions)
