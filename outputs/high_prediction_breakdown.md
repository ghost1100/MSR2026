# High-Prediction Breakdown

- Total \`High\` predictions: **0**
- Of those, manual labels that *indicate testing* (heuristic): **0**

## Breakdown by manual label (original `was test included Y/N` values)

| manual_label_raw | count_high_predictions | pct_of_high |
|---:|---:|---:|

## Breakdown by explicit manual categories (mapped from raw labels)

| manual_category | count_high |
|---:|---:|

## Interpretation
Most `High` predictions fall into categories that do not indicate test code was actually included (e.g., `error 404`, `No tests included`). This confirms that keyword-based detection over title/body produces many false positives. Consider refining the detector to require changes in test file paths or file diff contents.