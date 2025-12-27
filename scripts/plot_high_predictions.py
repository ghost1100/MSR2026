"""
Create visualizations for High predictions vs manual review labels.
Outputs:
 - outputs/figures/high_by_manual_norm.png
 - outputs/figures/high_by_manual_label_stacked.png
 - outputs/figures/high_pie_manual_yes.png

Usage:
    python scripts/plot_high_predictions.py --csv comprehensive_pr_manual_verification_dataset.csv
"""
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')


def normalize_manual_label(x):
    s = str(x).strip().lower()
    if s == '':
        return ''
    if 'error' in s or '404' in s or 'n/a' in s or 'unknown' in s:
        return ''
    if 'no tests' in s or s in ('no', 'n', 'none') or 'not included' in s:
        return 'no'
    if 'partial' in s or 'partially' in s:
        return 'partial'
    if 'testing included' in s or 'extensive testing' in s or 'comprehensive testing' in s or 'included' in s or 'testing' in s:
        return 'yes'
    return s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', default='comprehensive_pr_manual_verification_dataset.csv')
    parser.add_argument('--outdir', default='outputs/figures')
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    df = pd.read_csv(args.csv, dtype=str).fillna('')

    # Normalize manual label
    if 'was test included Y/N' in df.columns:
        df['manual_raw'] = df['was test included Y/N'].astype(str).str.strip()
    elif 'manual_testing_present' in df.columns:
        df['manual_raw'] = df['manual_testing_present'].astype(str).str.strip()
    else:
        df['manual_raw'] = ''
    df['manual_norm'] = df['manual_raw'].apply(normalize_manual_label)

    # Normalize auto confidence
    if 'test detection' in df.columns:
        df['auto_conf'] = df['test detection'].astype(str).str.strip().str.lower()
    elif 'auto_conf' in df.columns:
        df['auto_conf'] = df['auto_conf'].astype(str).str.strip().str.lower()
    else:
        # derive from keywords if missing
        df['auto_conf'] = 'low'

    high_df = df[df['auto_conf'] == 'high'].copy()

    # Plot 1: Bar - manual_norm counts among High predictions
    counts = high_df['manual_norm'].value_counts().reindex(['yes', 'no', 'partial', ''], fill_value=0)
    plt.figure(figsize=(6,4))
    sns.barplot(x=counts.index.map(lambda x: x if x!='' else '(blank)'), y=counts.values, palette='Set2')
    plt.title('High predictions by manual normalized label')
    plt.xlabel('Manual label')
    plt.ylabel('Count (High predictions)')
    plt.tight_layout()
    p1 = os.path.join(args.outdir, 'high_by_manual_norm.png')
    plt.savefig(p1, dpi=200)
    plt.close()

    # New: Map manual_raw to explicit categories for clearer presentation
    def map_manual_category(s):
        s = str(s).strip().lower()
        if s == '':
            return '(blank)'
        if 'comprehensive testing' in s:
            return 'comprehensive testing'
        if 'extensive testing' in s:
            return 'extensive testing'
        if 'no tests included' in s or 'no tests' in s or 'not included' in s:
            return 'no tests included'
        if 'documented testing' in s:
            return 'documented testing but none included'
        if 'error' in s or '404' in s:
            return 'error 404'
        if 'testing included' in s or 'included' in s or 'testing' in s:
            return 'testing included'
        return s

    high_df['manual_category'] = high_df['manual_raw'].apply(map_manual_category)

    # Plot 2 (new): Bar - counts of explicit manual categories among High predictions
    cat_counts = high_df['manual_category'].value_counts()
    plt.figure(figsize=(8,4))
    sns.barplot(x=cat_counts.values, y=cat_counts.index, palette='Spectral')
    plt.title('High predictions by explicit manual category')
    plt.xlabel('Count')
    plt.ylabel('Manual category')
    plt.tight_layout()
    p_cat = os.path.join(args.outdir, 'high_by_manual_category.png')
    plt.savefig(p_cat, dpi=200)
    plt.close()

    # Plot 3 (updated): Stacked bar - top manual_category (top 6) and their manual_norm split
    top_cats = high_df['manual_category'].value_counts().head(6).index.tolist()
    stacked_cat = high_df[high_df['manual_category'].isin(top_cats)].copy()
    pivot_cat = pd.crosstab(stacked_cat['manual_category'], stacked_cat['manual_norm'])
    # Ensure columns order
    for c in ['yes','no','partial','']:
        if c not in pivot_cat.columns:
            pivot_cat[c]=0
    pivot_cat = pivot_cat[['yes','no','partial','']]
    pivot_cat.plot(kind='barh', stacked=True, figsize=(10,5), colormap='tab20')
    plt.title('Top manual categories among High predictions (stacked by manual_norm)')
    plt.xlabel('Count')
    plt.ylabel('Manual category')
    plt.legend(title='Manual norm')
    plt.tight_layout()
    p2 = os.path.join(args.outdir, 'high_by_manual_category_stacked.png')
    plt.savefig(p2, dpi=200)
    plt.close()

    # Plot 4: Pie - proportion of High predictions by explicit category (top 6 combined, others grouped)
    pie_df = cat_counts.copy()
    top6 = pie_df.head(6)
    others_sum = pie_df.sum() - top6.sum()
    labels = list(top6.index) + ['other']
    sizes = list(top6.values) + [others_sum]
    plt.figure(figsize=(7,7))
    # choose colors
    colors = sns.color_palette('tab10', len(labels))

    # draw pie without slice labels (we'll use legend for names)
    wedges, texts, autotexts = plt.pie(sizes, labels=None, autopct='%1.1f%%', startangle=140, colors=colors, textprops={'color':'white'})
    plt.title('High predictions by manual category (top 6 + other)')

    # Create legend with color-coded entries and labels
    from matplotlib.patches import Patch
    legend_labels = [f"{lab} ({val})" for lab, val in zip(labels, sizes)]
    patches = [Patch(facecolor=colors[i], label=legend_labels[i]) for i in range(len(labels))]
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left')

    # Improve layout and save
    plt.tight_layout()
    p3 = os.path.join(args.outdir, 'high_pie_manual_category.png')
    plt.savefig(p3, dpi=200, bbox_inches='tight')
    plt.close()

    print('Plots saved:')
    print(' -', p1)
    print(' -', p_cat)
    print(' -', p2)
    print(' -', p3)
    print('Plots saved:')
    print(' -', p1)
    print(' -', p2)
    print(' -', p3)

if __name__ == '__main__':
    main()
