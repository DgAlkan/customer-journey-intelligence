# Customer Journey Intelligence

[Live demo](https://dgalkan-customer-journey.streamlit.app)

Independent portfolio project by Rodrigo Alcantara.

Longitudinal event analytics, monthly activity cohorts and configurable lifecycle classification using synthetic customers.

## Run locally

```bash
pip install -r requirements.txt
python generate_data.py
python -m pytest -q
streamlit run app.py
```

Run SQL with DuckDB from the repository root after generating the CSV. See [methodology](docs/methodology.md) for definitions and limitations.

## Structure

- engine.py: deterministic generator and analytical functions
- app.py: interactive dashboard and CSV export
- sql/analysis.sql: analytical SQL
- tests/: automated checks
- .github/workflows/: CI configuration

No employer data or proprietary code. Synthetic demonstration only. No production performance claims. Test execution must be verified before release.

