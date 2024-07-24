if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
if 'pandas' not in globals():
    import pandas as pd
if 'numpy' not in globals():
    import numpy as np


def is_valid_year(value):
    return value.isdigit() and len(value) == 4

def is_valid_power(value):
    if pd.isna(value):  # Check if the value is NaN
        return False
    # Check if the value is a number or a valid power entry
    return value.replace(',', '.').replace('.', '', 1).isdigit() or value.isdigit()

@transformer
def transform(data, *args, **kwargs):
    # Convert price_in_euro to numeric
    data['price_in_euro'] = pd.to_numeric(data['price_in_euro'], errors='coerce')

    # Drop rows where price_in_euro is NaN
    data = data.dropna(subset=['price_in_euro'])

    # Remove extreme prices (e.g., keeping prices below the 95th percentile)
    price_threshold = data['price_in_euro'].quantile(0.95)
    data = data[data['price_in_euro'] <= price_threshold]

    # Replace invalid years with NaN and convert to numeric
    data['year'] = data['year'].apply(lambda x: x if is_valid_year(x) else np.nan)
    data['year'] = pd.to_numeric(data['year'], errors='coerce')

    # Replace invalid power entries with NaN, convert to float and replace commas with dots
    data['power_kw'] = data['power_kw'].apply(lambda x: x if is_valid_power(x) else np.nan)
    data['power_kw'] = data['power_kw'].str.replace(',', '.').astype(float)
    
    data['power_ps'] = data['power_ps'].apply(lambda x: x if is_valid_power(x) else np.nan)
    data['power_ps'] = data['power_ps'].str.replace(',', '.').astype(float)
    data['power_ps'] = pd.to_numeric(data['power_ps'], errors='coerce')

    # Convert mileage_in_km to numeric
    data['mileage_in_km'] = pd.to_numeric(data['mileage_in_km'], errors='coerce')

    # Define columns to keep
    categorical_cols = ['brand', 'model', 'transmission_type']
    numerical_cols = ['year', 'power_ps', 'mileage_in_km']
    cols_to_keep = ['price_in_euro'] + categorical_cols + numerical_cols

    # Keep only the specified columns
    data = data[cols_to_keep]

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
