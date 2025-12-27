-- pr_analysis.sql
-- Instructions:
-- 1) Start sqlite3 and run: .read sql/pr_analysis.sql
-- Or run step-by-step commands shown below.

-- Import CSV into sqlite (run inside sqlite3):
-- .mode csv
-- .import comprehensive_pr_manual_verification_dataset.csv pr_raw

-- If import creates a table with awkward column names (headers with spaces or Unnamed:N), you can reference them with double quotes. Example: "was test included Y/N" and "test detection".

-- Create a normalized view with manual_norm and auto_conf
DROP VIEW IF EXISTS pr_norm;
CREATE VIEW pr_norm AS
SELECT
  pr_raw.*, 
  CASE
    WHEN lower("was test included Y/N") LIKE '%no tests%' OR lower("was test included Y/N") LIKE '%no tests included%' OR lower("was test included Y/N") LIKE '%no tests%' OR lower("was test included Y/N") LIKE '%none%' OR lower("was test included Y/N") LIKE '%not included%' THEN 'no'
    WHEN lower("was test included Y/N") LIKE '%partial%' THEN 'partial'
    WHEN lower("was test included Y/N") LIKE '%testing included%' OR lower("was test included Y/N") LIKE '%comprehensive testing%' OR lower("was test included Y/N") LIKE '%extensive testing%' OR lower("was test included Y/N") LIKE '%included%' OR lower("was test included Y/N") LIKE '%testing%' THEN 'yes'
    WHEN lower("was test included Y/N") LIKE '%error%' OR lower("was test included Y/N") LIKE '%404%' THEN ''
    ELSE lower("was test included Y/N")
  END AS manual_norm,
  lower("test detection") AS auto_conf
FROM pr_raw;

-- Basic counts
SELECT count(*) AS total FROM pr_norm;
SELECT count(*) AS manual_yes FROM pr_norm WHERE manual_norm = 'yes';
SELECT count(*) AS predicted_high FROM pr_norm WHERE auto_conf = 'high';

-- Confusion matrix for High threshold
SELECT
  SUM(CASE WHEN auto_conf = 'high' AND manual_norm = 'yes' THEN 1 ELSE 0 END) AS TP,
  SUM(CASE WHEN auto_conf = 'high' AND (manual_norm != 'yes' OR manual_norm = '') THEN 1 ELSE 0 END) AS FP,
  SUM(CASE WHEN (auto_conf != 'high' OR auto_conf IS NULL) AND manual_norm = 'yes' THEN 1 ELSE 0 END) AS FN,
  SUM(CASE WHEN (auto_conf != 'high' OR auto_conf IS NULL) AND (manual_norm != 'yes' OR manual_norm = '') THEN 1 ELSE 0 END) AS TN
FROM pr_norm;

-- Precision / Recall (High)
SELECT
  (1.0 * SUM(CASE WHEN auto_conf = 'high' AND manual_norm = 'yes' THEN 1 ELSE 0 END) ) / NULLIF(SUM(CASE WHEN auto_conf = 'high' THEN 1 ELSE 0 END),0) AS precision_high,
  (1.0 * SUM(CASE WHEN auto_conf = 'high' AND manual_norm = 'yes' THEN 1 ELSE 0 END) ) / NULLIF(SUM(CASE WHEN manual_norm = 'yes' THEN 1 ELSE 0 END),0) AS recall_high;

-- Extract false positives (auto_conf='high' but manual_norm != 'yes') and save to CSV from sqlite CLI:
-- .headers on
-- .mode csv
-- .once outputs/false_positives_sql.csv
-- SELECT * FROM pr_norm WHERE auto_conf='high' AND (manual_norm != 'yes' OR manual_norm = '');
-- .once stdout

-- Extract false negatives (auto_conf != 'high' and manual_norm='yes')
-- .once outputs/false_negatives_sql.csv
-- SELECT * FROM pr_norm WHERE (auto_conf != 'high' OR auto_conf IS NULL) AND manual_norm = 'yes';
-- .once stdout

-- Example: Top keywords in false positives (simple LIKE counts)
SELECT
  SUM(CASE WHEN lower(pr_title) LIKE '%test%' OR lower(pr_body) LIKE '%test%' THEN 1 ELSE 0 END) AS mentions_test,
  SUM(CASE WHEN lower(pr_title) LIKE '%doc%' OR lower(pr_body) LIKE '%doc%' OR lower(pr_title) LIKE '%documentation%' OR lower(pr_body) LIKE '%documentation%' THEN 1 ELSE 0 END) AS mentions_docs
FROM pr_norm WHERE auto_conf='high' AND (manual_norm != 'yes' OR manual_norm = '');

-- Breakdown of 'High' predictions by raw manual label (original column)
SELECT
  lower("was test included Y/N") AS manual_label_raw,
  COUNT(*) AS count_high_predictions
FROM pr_norm
WHERE auto_conf = 'high'
GROUP BY manual_label_raw
ORDER BY count_high_predictions DESC;

-- Compute total high predictions and how many of them were manual positives
SELECT
  SUM(CASE WHEN auto_conf='high' THEN 1 ELSE 0 END) AS total_high_predictions,
  SUM(CASE WHEN auto_conf='high' AND (lower("was test included Y/N") LIKE '%testing included%' OR lower("was test included Y/N") LIKE '%comprehensive testing%' OR lower("was test included Y/N") LIKE '%extensive testing%' OR lower("was test included Y/N") LIKE '%testing%' OR lower("was test included Y/N") LIKE '%included%') THEN 1 ELSE 0 END) AS high_and_manual_say_yes
FROM pr_norm;

-- Compute percentages for each manual label within High predictions
SELECT
  manual_label_raw,
  count_high_predictions,
  ROUND(100.0 * count_high_predictions / (SELECT SUM(count_high_predictions) FROM (
    SELECT lower("was test included Y/N") AS manual_label_raw, COUNT(*) AS count_high_predictions FROM pr_norm WHERE auto_conf='high' GROUP BY manual_label_raw
  )), 2) AS pct_of_high
FROM (
  SELECT lower("was test included Y/N") AS manual_label_raw, COUNT(*) AS count_high_predictions FROM pr_norm WHERE auto_conf='high' GROUP BY manual_label_raw
) ORDER BY count_high_predictions DESC;

-- Map raw manual labels into explicit categories and show breakdown for High predictions
SELECT
  CASE
    WHEN lower("was test included Y/N") LIKE '%comprehensive testing%' THEN 'comprehensive testing'
    WHEN lower("was test included Y/N") LIKE '%extensive testing%' THEN 'extensive testing'
    WHEN lower("was test included Y/N") LIKE '%no tests included%' OR lower("was test included Y/N") LIKE '%no tests%' OR lower("was test included Y/N") LIKE '%not included%' OR lower("was test included Y/N") LIKE '%not included%' THEN 'no tests included'
    WHEN lower("was test included Y/N") LIKE '%documented testing%' THEN 'documented testing but none included'
    WHEN lower("was test included Y/N") LIKE '%error%' OR lower("was test included Y/N") LIKE '%404%' THEN 'error 404'
    WHEN lower("was test included Y/N") LIKE '%testing included%' OR lower("was test included Y/N") LIKE '%included%' OR lower("was test included Y/N") LIKE '%testing%' THEN 'testing included'
    ELSE trim(lower("was test included Y/N"))
  END AS manual_category,
  COUNT(*) AS cnt_high
FROM pr_norm
WHERE auto_conf = 'high'
GROUP BY manual_category
ORDER BY cnt_high DESC;

-- End of script
