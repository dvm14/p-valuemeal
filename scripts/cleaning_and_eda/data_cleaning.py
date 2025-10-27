##########################################################################
# This script is responsible for checking for missing values, dropping   #
# recipes with 10 < calorie count < 5000, verifying the ratings lie      #
# between 0 and 5, creating features "is_5_star" , calorie_category      #
# uses recipes_with_calories_and_ratings.csv file for this.              # 
# saves cleaned data to recipes_cleaned.csv                              #     
##########################################################################

# imports
import pandas as pd
import numpy as np

# Load the data
print("Loading data...")
df = pd.read_csv('../../processed_data/recipes_with_calories_and_ratings.csv')
print(f"Initial dataset: {len(df):,} recipes")

# ============================================================
# STEP 1: CHECK FOR MISSING VALUES
# ============================================================
print("\n" + "="*60)
print("STEP 1: CHECKING MISSING VALUES")
print("="*60)

print("\nMissing values:")
print(df.isnull().sum())

# Remove recipes with missing values
df_clean = df.dropna()
removed_missing = len(df) - len(df_clean)
print(f"\nRemoved {removed_missing:,} recipes with missing values")
print(f"  Remaining: {len(df_clean):,} recipes")

# ============================================================
# STEP 2: REMOVE UNREALISTIC CALORIE VALUES
# ============================================================
print("\n" + "="*60)
print("STEP 2: REMOVING CALORIE OUTLIERS")
print("="*60)

print(f"\nCalorie range before cleaning:")
print(f"  Min: {df_clean['calories'].min():.1f}")
print(f"  Max: {df_clean['calories'].max():.1f}")
print(f"  Mean: {df_clean['calories'].mean():.1f}")
print(f"  Median: {df_clean['calories'].median():.1f}")

# Remove unrealistic values
# Most recipes should be between 10 and 5000 calories
min_calories = 10
max_calories = 5000

df_clean = df_clean[
    (df_clean['calories'] >= min_calories) & 
    (df_clean['calories'] <= max_calories)
]

removed_outliers = len(df.dropna()) - len(df_clean)
print(f"\nRemoved {removed_outliers:,} recipes with unrealistic calories (<{min_calories} or >{max_calories})")
print(f"  Remaining: {len(df_clean):,} recipes")

print(f"\nCalorie range after cleaning:")
print(f"  Min: {df_clean['calories'].min():.1f}")
print(f"  Max: {df_clean['calories'].max():.1f}")
print(f"  Mean: {df_clean['calories'].mean():.1f}")
print(f"  Median: {df_clean['calories'].median():.1f}")

# ============================================================
# STEP 3: VERIFY RATING RANGE
# ============================================================
print("\n" + "="*60)
print("STEP 3: VERIFYING RATING RANGE")
print("="*60)

print(f"\nRating range:")
print(f"  Min: {df_clean['avg_rating'].min():.1f}")
print(f"  Max: {df_clean['avg_rating'].max():.1f}")

# Ratings should be between 0 and 5
df_clean = df_clean[
    (df_clean['avg_rating'] >= 0) & 
    (df_clean['avg_rating'] <= 5)
]

print(f"All ratings are in valid range (0-5)")

# ============================================================
# STEP 4: CREATE ADDITIONAL VARIABLES
# ============================================================
print("\n" + "="*60)
print("STEP 4: CREATING NEW VARIABLES")
print("="*60)

# Binary indicator: Is this a 5-star recipe?
df_clean['is_five_star'] = (df_clean['avg_rating'] == 5.0).astype(int)
print(f"\n✓ Created 'is_five_star' variable")
print(f"  5-star recipes: {df_clean['is_five_star'].sum():,} ({df_clean['is_five_star'].mean()*100:.1f}%)")

# Calorie categories (Low, Medium, High)
df_clean['calorie_category'] = pd.qcut(
    df_clean['calories'], 
    q=3, 
    labels=['Low', 'Medium', 'High']
)
print(f"\nCreated 'calorie_category' variable")
print(df_clean['calorie_category'].value_counts().sort_index())

# ============================================================
# STEP 5: FINAL SUMMARY
# ============================================================
print("\n" + "="*60)
print("CLEANING SUMMARY")
print("="*60)

print(f"\nOriginal dataset: {len(df):,} recipes")
print(f"Removed (missing values): {removed_missing:,}")
print(f"Removed (calorie outliers): {removed_outliers:,}")
print(f"Final cleaned dataset: {len(df_clean):,} recipes")
print(f"Total removed: {len(df) - len(df_clean):,} ({(len(df) - len(df_clean))/len(df)*100:.1f}%)")

print(f"\nFinal dataset shape: {df_clean.shape}")
print(f"\nColumns: {df_clean.columns.tolist()}")

# ============================================================
# STEP 6: SAVE CLEANED DATA
# ============================================================
print("\n" + "="*60)
print("SAVING CLEANED DATA")
print("="*60)

df_clean.to_csv('../../processed_data/recipes_data_cleaned.csv', index=False)
print("Saved to 'processed_data/recipes_cleaned.csv'")

# Display first few rows
print("\n" + "="*60)
print("CLEANED DATA PREVIEW:")
print("="*60)
print(df_clean.head(10))

print("\n" + "="*60)
print("DESCRIPTIVE STATISTICS:")
print("="*60)
print(df_clean[['calories', 'avg_rating']].describe())

print("\nDATA CLEANING COMPLETE!")