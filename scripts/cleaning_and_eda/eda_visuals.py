##########################################################################
# This script is responsible for creating a boxplot and countplot for    #
# the calories and ratings column respectively. It uses the processed    #
# recipes_with_calories_and_ratings.csv file for this.                   #
##########################################################################

# imports

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_style("whitegrid")

# Load data
df = pd.read_csv('../../processed_data/recipes_with_calories_and_ratings.csv')

print(f"Loaded {len(df):,} recipes")

# Check calorie outliers
print("\nCalorie statistics:")
print(df['calories'].describe())
print(f"\n99th percentile: {df['calories'].quantile(0.99):.1f}")
print(f"95th percentile: {df['calories'].quantile(0.95):.1f}")

# Create figure
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# ============================================================
# PLOT 1: BOXPLOT FOR CALORIES
# ============================================================

# Set y-axis limit to show most data clearly
ylim_max = df['calories'].quantile(0.95)

axes[0].boxplot(df['calories'].dropna(), vert=True)
axes[0].set_ylabel('Calories', fontsize=12)
axes[0].set_title('Distribution of Recipe Calories', fontsize=14, fontweight='bold')
axes[0].set_ylim(0, ylim_max)
axes[0].grid(axis='y', alpha=0.3)

# Add statistics
median_cal = df['calories'].median()
mean_cal = df['calories'].mean()
q25 = df['calories'].quantile(0.25)
q75 = df['calories'].quantile(0.75)

stats_text = f'Median: {median_cal:.1f}\nMean: {mean_cal:.1f}\nQ1: {q25:.1f}\nQ3: {q75:.1f}'
axes[0].text(1.15, ylim_max * 0.7, stats_text, 
             fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Add note about outliers
n_outliers = df[df['calories'] > ylim_max].shape[0]
axes[0].text(0.5, -0.15, f'Note: {n_outliers:,} extreme outliers (>{ylim_max:.0f} cal) not shown for clarity',
            transform=axes[0].transAxes, ha='center', fontsize=9, style='italic')

# ============================================================
# PLOT 2: RATING DISTRIBUTION
# ============================================================

# Count ratings
rating_counts = df['avg_rating'].value_counts().sort_index()

# Create bar plot
bars = axes[1].bar(rating_counts.index, rating_counts.values, 
                   color='steelblue', edgecolor='black', alpha=0.7, width=0.3)

axes[1].set_xlabel('Average Rating', fontsize=12)
axes[1].set_ylabel('Number of Recipes', fontsize=12)
axes[1].set_title('Distribution of Recipe Ratings (Imbalanced)', 
                  fontsize=14, fontweight='bold')
axes[1].grid(axis='y', alpha=0.3)

# Highlight high ratings (≥4.5) in red
for i, (rating, count) in enumerate(zip(rating_counts.index, rating_counts.values)):
    if rating >= 4.5:
        bars[i].set_color('red')
        bars[i].set_alpha(0.8)

# Add imbalance text box
total_recipes = len(df)
high_rated_count = df[df['avg_rating'] >= 4.5].shape[0]
high_rated_pct = (high_rated_count / total_recipes) * 100

textstr = f'Imbalance Alert:\n{high_rated_pct:.1f}% of recipes\nhave ratings ≥ 4.5'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
axes[1].text(0.05, 0.95, textstr, transform=axes[1].transAxes, fontsize=10,
            verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('../../plots/eda_plots.png', dpi=300, bbox_inches='tight')
print("\nPlots saved as 'plots/eda_plots.png'")

# ============================================================
# PRINT DETAILED STATISTICS
# ============================================================
print("\n" + "="*60)
print("CALORIE STATISTICS:")
print("="*60)
print(df['calories'].describe())
print(f"\nOutliers (>95th percentile): {n_outliers:,} recipes")
print(f"Max calorie recipe: {df['calories'].max():.1f} calories")

print("\n" + "="*60)
print("RATING DISTRIBUTION:")
print("="*60)
for rating, count in rating_counts.items():
    pct = (count / total_recipes) * 100
    print(f"  Rating {rating:.1f}: {count:,} recipes ({pct:.1f}%)")

print(f"\n IMBALANCE SUMMARY:")
print(f"  High-rated (≥4.5): {high_rated_count:,} ({high_rated_pct:.1f}%)")
print(f"  Lower-rated (<4.5): {total_recipes - high_rated_count:,} ({100-high_rated_pct:.1f}%)")