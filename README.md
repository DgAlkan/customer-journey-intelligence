## v2.0 dashboard update

[Live demo](https://dgalkan-customer-journey.streamlit.app) (deployment and public access to be verified).

Executive dashboard presentation, configurable synthetic demonstration volume and consistent portfolio branding. Existing analytical engine, SQL and tests are unchanged. v2.0 CI and manual browser review remain pending; prior v1.1 approval does not certify this revision.

# Customer Journey Intelligence

Independent portfolio project by Rodrigo Alcantara (DgAlkan), developed with AI assistance. Version 1.0 initial implementation.

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

No employer data or proprietary code. Synthetic demonstration only. No hosted deployment or production performance claims. Test execution must be verified before release.

## Original introduction

# customer-journey-intelligence
A longitudinal analytics framework for customer lifecycle modeling, cohort analysis, angagement and retention.
