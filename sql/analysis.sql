-- DuckDB; generate data first with python generate_data.py
WITH events AS (SELECT * FROM read_csv_auto('data/synthetic.csv') WHERE date <= DATE '2025-12-31'),
firsts AS (SELECT customer_id,date_trunc('month',min(date)) AS cohort FROM events GROUP BY 1),
sizes AS (SELECT cohort,count(*) AS n FROM firsts GROUP BY 1)
SELECT cohort,date_diff('month',cohort,date_trunc('month',date)) AS month_offset,
count(DISTINCT e.customer_id)::DOUBLE / n AS activity_rate
FROM events e JOIN firsts f USING(customer_id) JOIN sizes s USING(cohort)
GROUP BY cohort,month_offset,n ORDER BY 1,2;
