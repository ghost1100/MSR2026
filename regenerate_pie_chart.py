"""
Quick script to regenerate just the pie chart with fixed layout
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load data
print("Loading data...")
df = pd.read_csv('data/raw/aidata.csv')

# Create output directory if needed
os.makedirs('outputs/figures', exist_ok=True)

# Calculate agent distribution
print("Analyzing agent distribution...")
agent_counts = df['agent'].value_counts()

# Create pie chart with legend (no overlapping labels)
print("Generating pie chart...")
plt.figure(figsize=(12, 10))

# Colors for each agent
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']

# Explode slices slightly for better visibility
explode = [0.05, 0.02, 0.02, 0.02, 0.02]

# Create pie without labels on the chart itself
wedges, texts, autotexts = plt.pie(
    agent_counts.values, 
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    explode=explode,
    textprops={'fontsize': 14, 'weight': 'bold'}
)

plt.title('Distribution of AI Coding Agents in Pull Requests', fontsize=16, pad=20)

# Create legend with agent names and counts
legend_labels = [f'{name}: {count:,} PRs' for name, count in agent_counts.items()]
plt.legend(
    legend_labels,
    loc='center left',
    bbox_to_anchor=(1, 0.5),
    fontsize=12
)

# Save figure
output_path = 'outputs/figures/complete_dataset_agent_distribution.png'
plt.tight_layout()
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f" Pie chart saved to: {output_path}")

plt.close()

# Verify file was created
if os.path.exists(output_path):
    file_size = os.path.getsize(output_path)
    print(f" File verified: {file_size:,} bytes")
else:
    print(" ERROR: File not created")
