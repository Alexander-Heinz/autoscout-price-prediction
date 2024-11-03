import pandas as pd
import json

# Load your dataset
df = pd.read_csv('data/data.csv')  # Adjust the path to your dataset

# Function to filter out models that are the same as their brand
# Function to filter out models that are the same as their brand
def filter_models(models, brand):
    brand_normalized = brand.lower().replace('-', ' ').replace('_', ' ')
    filtered_models = []
    for model in models:
        model_normalized = model.lower().replace('-', ' ').replace('_', ' ')
        if model_normalized != brand_normalized:
            filtered_models.append(model)
    return filtered_models

# Extract unique brands and their corresponding models
brands_models = {brand: sorted(filter_models(models.unique(), brand)) for brand, models in df.groupby('brand')['model']}

# Sort brands alphabetically
sorted_brands_models = dict(sorted(brands_models.items()))

# Extract unique transmission types
transmission_types = sorted(df['transmission_type'].dropna().unique().tolist())


# Combine into a single dictionary
unique_values = {
    'brands_models': brands_models,
    'transmission_types': transmission_types
}

# Save unique values to a JSON file
with open('unique_values.json', 'w') as json_file:
    json.dump(unique_values, json_file, indent=4)

print('Unique values have been extracted and saved to unique_values.json')