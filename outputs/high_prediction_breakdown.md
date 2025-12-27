# High-Prediction Breakdown

- Total \`High\` predictions: **118**
- Of those, manual labels that *indicate testing* (heuristic): **57**

## Breakdown by manual label (original `was test included Y/N` values)

| manual_label_raw | count_high_predictions | pct_of_high |
|---:|---:|---:|
| error 404 | 61 | 51.69% |
| comprehensive testing  | 23 | 19.49% |
| no tests included | 21 | 17.8% |
| testing included | 7 | 5.93% |
| extensive testing was included | 6 | 5.08% |

## Breakdown by explicit manual categories (mapped from raw labels)

| manual_category | count_high |
|---:|---:|
| error 404 | 61 |
| comprehensive testing | 23 |
| no tests included | 21 |
| testing included | 7 |
| extensive testing | 6 |

## Interpretation
Most `High` predictions fall into categories that do not indicate test code was actually included (e.g., `error 404`, `No tests included`). This confirms that keyword-based detection over title/body produces many false positives. Consider refining the detector to require changes in test file paths or file diff contents.