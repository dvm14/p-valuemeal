##########################################################################
# This script is responsible for merging the data from RAW_recipes.csv   #
# and RAW_interactions.csv files to create a cleaned dataset containing  #
# recipe IDs, their average user ratings, and calorie information        #
##########################################################################

# imports

import pandas as pd
import numpy as np

# Step 1: Load the recipes file
print("Loading recipes...")
recipes = pd.read_csv('../../raw_data/RAW_recipes.csv')
print(f"Loaded {len(recipes):,} recipes")

# Step 2: Load the interactions file
print("\nLoading interactions...")
interactions = pd.read_csv('../../raw_data/RAW_interactions.csv')
print(f"Loaded {len(interactions):,} interactions")

# Step 3: Look at what columns we have
print("\n" + "="*60)
print("RECIPES COLUMNS:")
print(recipes.columns.tolist())

print("\nINTERACTIONS COLUMNS:")
print(interactions.columns.tolist())

# Step 4: Extract calories from the nutrition column
print("\n" + "="*60)
print("Extracting calories from nutrition column...")

# The nutrition column looks is an array and needs to be parsed

def extract_calories(nutrition_str):
    """Extract calories from nutrition string"""
    try:
        # Remove brackets and split by comma
        values = nutrition_str.strip('[]').split(',')
        # First value is calories
        return float(values[0])
    except:
        return np.nan

recipes['calories'] = recipes['nutrition'].apply(extract_calories)
print(f"Extracted calories")

# Step 5: Calculate average rating per recipe
print("\nCalculating average rating per recipe...")
avg_ratings = interactions.groupby('recipe_id')['rating'].mean().reset_index()
avg_ratings.columns = ['recipe_id', 'avg_rating']
avg_ratings['avg_rating'] = avg_ratings['avg_rating'].round(2)
print(f"Calculated average ratings for {len(avg_ratings):,} recipes")

# Step 6: Create your final dataframe
print("\nCreating final dataframe...")
df = recipes[['id', 'calories']].merge(
    avg_ratings, 
    left_on='id', 
    right_on='recipe_id', 
    how='inner'
)

# Clean up
df = df[['recipe_id', 'avg_rating', 'calories']]

print(f" Final dataframe created")

# Step 7: Print stats
print("\n" + "="*60)
print("YOUR DATAFRAME:")
print("="*60)
print(f"Shape: {df.shape}")
print(f"\nFirst 10 rows:")
print(df.head(10))

print(f"\nBasic statistics:")
print(df.describe())

print(f"\nMissing values:")
print(df.isnull().sum())

# Step 8: Save cleaned data
df.to_csv('../../processed_data/recipes_with_calories_and_ratings.csv', index=False)
print(f"Saved to 'processed_data/recipes_with_calories_and_ratings.csv'")