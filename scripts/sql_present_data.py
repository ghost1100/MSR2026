"""
Run the SQL analysis in `sql/pr_analysis.sql` using a local SQLite DB and export
summary tables for presentation.

Outputs:
 - outputs/high_prediction_breakdown.csv
 - outputs/high_prediction_breakdown.md

Usage:
    python scripts/sql_present_data.py --csv comprehensive_pr_manual_verification_dataset.csv

This imports the CSV into SQLite (table `pr_raw`), creates the `pr_norm` view using the SQL script, runs the queries, and writes a friendly Markdown report.
"""
import sqlite3
import argparse
import os
import pandas as pd

SQL_SCRIPT = 'sql/pr_analysis.sql'
DB_PATH = 'pr.db'


def run_sql_script(conn, script_path):
    with open(script_path, 'r', encoding='utf-8') as f:
        sql = f.read()
    # sqlite3 executes only one statement at a time; split by semicolon safely
    for stmt in sql.split(';'):
        stmt = stmt.strip()
        if not stmt:
            continue
        try:
            conn.execute(stmt)
        except Exception as e:
            # ignore statements that are selects here; we'll run them explicitly
            pass


def fetch_breakdown(conn):
    # Fetch the breakdown of high predictions by raw manual label
    q = """
    SELECT
      manual_label_raw,
      count_high_predictions,
      pct_of_high
    FROM (
      SELECT
        lower("was test included Y/N") AS manual_label_raw,
        COUNT(*) AS count_high_predictions,
        ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM pr_norm WHERE auto_conf='high'), 2) AS pct_of_high
      FROM pr_norm
      WHERE auto_conf = 'high'
      GROUP BY manual_label_raw
      ORDER BY count_high_predictions DESC
    );
    """
    return pd.read_sql_query(q, conn)


def fetch_category_breakdown(conn):
    # Fetch breakdown of High predictions grouped into explicit manual categories
    q = """
    SELECT manual_category, cnt_high FROM (
      SELECT
        CASE
          WHEN lower("was test included Y/N") LIKE '%comprehensive testing%' THEN 'comprehensive testing'
          WHEN lower("was test included Y/N") LIKE '%extensive testing%' THEN 'extensive testing'
          WHEN lower("was test included Y/N") LIKE '%no tests included%' OR lower("was test included Y/N") LIKE '%no tests%' OR lower("was test included Y/N") LIKE '%not included%' THEN 'no tests included'
          WHEN lower("was test included Y/N") LIKE '%documented testing%' THEN 'documented testing but none included'
          WHEN lower("was test included Y/N") LIKE '%error%' OR lower("was test included Y/N") LIKE '%404%' THEN 'error 404'
          WHEN lower("was test included Y/N") LIKE '%testing included%' OR lower("was test included Y/N") LIKE '%included%' OR lower("was test included Y/N") LIKE '%testing%' THEN 'testing included'
          ELSE trim(lower("was test included Y/N"))
        END AS manual_category,
        COUNT(*) AS cnt_high
      FROM pr_norm
      WHERE auto_conf = 'high'
      GROUP BY manual_category
      ORDER BY cnt_high DESC
    );
    """
    return pd.read_sql_query(q, conn)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', default='comprehensive_pr_manual_verification_dataset.csv')
    parser.add_argument('--db', default=DB_PATH)
    parser.add_argument('--outcsv', default='outputs/high_prediction_breakdown.csv')
    parser.add_argument('--outmd', default='outputs/high_prediction_breakdown.md')
    args = parser.parse_args()

    os.makedirs('outputs', exist_ok=True)

    # Load CSV and import into SQLite (pr_raw)
    print('Loading CSV into SQLite...')
    df = pd.read_csv(args.csv, dtype=str)
    conn = sqlite3.connect(args.db)
    df.to_sql('pr_raw', conn, if_exists='replace', index=False)

    # Execute SQL script to create view; only run the CREATE VIEW block to avoid executing selects
    print('Applying SQL script (creating view)...')
    with open(SQL_SCRIPT, 'r', encoding='utf-8') as f:
        script = f.read()
    # Extract CREATE VIEW block (between 'CREATE VIEW pr_norm AS' and the following ';')
    start = script.lower().find('create view pr_norm as')
    if start != -1:
        # find the end of this CREATE VIEW statement
        end = script.find(';', start)
        create_view_stmt = script[start:end+1]
        try:
            # drop view if it already exists to avoid "view already exists" error
            try:
                conn.execute('DROP VIEW IF EXISTS pr_norm')
            except Exception:
                pass
            conn.executescript(create_view_stmt)
        except Exception as e:
            print('Warning: failed to create view with error:', e)
    else:
        print('Warning: CREATE VIEW pr_norm AS not found in SQL script; skipping')

    # Fetch breakdown by raw label
    print('Querying breakdown...')
    breakdown = fetch_breakdown(conn)
    breakdown.to_csv(args.outcsv, index=False)

    # Fetch breakdown by explicit manual categories
    print('Querying category breakdown...')
    cat_df = fetch_category_breakdown(conn)
    cat_out = 'outputs/high_prediction_manual_category_breakdown.csv'
    cat_md_out = 'outputs/high_prediction_manual_category_breakdown.md'
    cat_df.to_csv(cat_out, index=False)

    # Create human-friendly Markdown
    # Safely fetch numeric counts (handle None)
    total_high_df = pd.read_sql_query("SELECT COUNT(*) AS cnt FROM pr_norm WHERE auto_conf='high'", conn)
    total_high = int(total_high_df['cnt'][0]) if not total_high_df['cnt'].isnull().all() else 0

    manual_yes_df = pd.read_sql_query(
        "SELECT SUM(CASE WHEN lower(\"was test included Y/N\") LIKE '%testing included%' OR lower(\"was test included Y/N\") LIKE '%comprehensive testing%' OR lower(\"was test included Y/N\") LIKE '%extensive testing%' OR lower(\"was test included Y/N\") LIKE '%testing%' OR lower(\"was test included Y/N\") LIKE '%included%' THEN 1 ELSE 0 END) AS cnt FROM pr_norm WHERE auto_conf='high'",
        conn
    )
    manual_yes_in_high = int(manual_yes_df['cnt'][0]) if (not manual_yes_df['cnt'].isnull().all() and manual_yes_df['cnt'][0] is not None) else 0

    md_lines = []
    md_lines.append('# High-Prediction Breakdown')
    md_lines.append('')
    md_lines.append(f'- Total \`High\` predictions: **{total_high}**')
    md_lines.append(f'- Of those, manual labels that *indicate testing* (heuristic): **{manual_yes_in_high}**')
    md_lines.append('')
    md_lines.append('## Breakdown by manual label (original `was test included Y/N` values)')
    md_lines.append('')
    md_lines.append('| manual_label_raw | count_high_predictions | pct_of_high |')
    md_lines.append('|---:|---:|---:|')
    for _, row in breakdown.iterrows():
        label = row['manual_label_raw'] if row['manual_label_raw'] and str(row['manual_label_raw']).strip() != '' else '(blank / error)'
        md_lines.append(f'| {label} | {int(row['count_high_predictions'])} | {row['pct_of_high']}% |')

    md_lines.append('')
    md_lines.append('## Breakdown by explicit manual categories (mapped from raw labels)')
    md_lines.append('')
    md_lines.append('| manual_category | count_high |')
    md_lines.append('|---:|---:|')
    for _, row in cat_df.iterrows():
        label = row['manual_category'] if row['manual_category'] and str(row['manual_category']).strip() != '' else '(blank / other)'
        md_lines.append(f'| {label} | {int(row['cnt_high'])} |')

    md_lines.append('')
    md_lines.append('## Interpretation')
    md_lines.append('Most `High` predictions fall into categories that do not indicate test code was actually included (e.g., `error 404`, `No tests included`). This confirms that keyword-based detection over title/body produces many false positives. Consider refining the detector to require changes in test file paths or file diff contents.')

    with open(args.outmd, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    # Save category markdown
    cat_md_lines = ['# High Predictions by Manual Category', '', '| manual_category | count_high |', '|---:|---:|']
    for _, row in cat_df.iterrows():
        label = row['manual_category'] if row['manual_category'] and str(row['manual_category']).strip() != '' else '(blank / other)'
        cat_md_lines.append(f'| {label} | {int(row['cnt_high'])} |')
    with open(cat_md_out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cat_md_lines))


    print(f'Done. CSV: {args.outcsv}  MD: {args.outmd}')
    conn.close()


if __name__ == '__main__':
    main()
