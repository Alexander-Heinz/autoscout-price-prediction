import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, df):
        self.df = df

    @staticmethod
    def is_valid_year(value):
        return value.isdigit() and len(value) == 4

    @staticmethod
    def is_valid_power(value):
        if pd.isna(value):  # Check if the value is NaN
            return False
        # Check if the value is a number or a valid power entry
        return value.replace(',', '.').replace('.', '', 1).isdigit() or value.isdigit()

    def clean_data(self):
         # Convert price_in_euro to numeric
        if 'price_in_euro' in self.df.columns:
            self.df['price_in_euro'] = pd.to_numeric(self.df['price_in_euro'], errors='coerce')
            # Drop rows where price_in_euro is NaN
            self.df = self.df.dropna(subset=['price_in_euro'])

            # Remove extreme prices (e.g., keeping prices below the 95th percentile)
            price_threshold = self.df['price_in_euro'].quantile(0.95)
            self.df = self.df[self.df['price_in_euro'] <= price_threshold]
 
        # Replace invalid years with NaN and convert to numeric
        self.df['year'] = self.df['year'].apply(lambda x: str(x) if self.is_valid_year(str(x)) else np.nan)

        # self.df['year'] = self.df['year'].apply(lambda x: x if self.is_valid_year(x) else np.nan)
        self.df['year'] = pd.to_numeric(self.df['year'], errors='coerce')

        # Replace invalid power entries with NaN, convert to float and replace commas with dots
        if 'power_kw' in self.df.columns:
            self.df['power_kw'] = self.df['power_kw'].apply(lambda x: str(x) if self.is_valid_power(str(x)) else np.nan)
            self.df['power_kw'] = self.df['power_kw'].str.replace(',', '.').astype(float)
        
        
        self.df['power_ps'] = self.df['power_ps'].apply(lambda x: str(x) if self.is_valid_power(str(x)) else np.nan)
        self.df['power_ps'] = self.df['power_ps'].str.replace(',', '.').astype(float)
        self.df['power_ps'] = pd.to_numeric(self.df['power_ps'], errors='coerce')

        # Convert mileage_in_km to numeric
        self.df['mileage_in_km'] = pd.to_numeric(self.df['mileage_in_km'], errors='coerce')

        # Define columns to keep
        categorical_cols = ['brand', 'model', 'transmission_type']
        numerical_cols = ['year', 'power_ps', 'mileage_in_km']
        # cols_to_keep = categorical_cols + numerical_cols
        cols_to_keep = [col for col in ['price_in_euro'] + categorical_cols + numerical_cols if col in self.df.columns]

        # Keep only the specified columns
        self.df = self.df[cols_to_keep]

    def get_features(self):
        # Separate features and target variable
        features = self.df.drop('price_in_euro', axis=1, errors='ignore')
        return features

    def get_features_and_target(self):
        # Separate features and target variable
        X = self.df.drop('price_in_euro', axis=1, errors='ignore')
        y = self.df['price_in_euro'] if 'price_in_euro' in self.df.columns else None
        return X, y

    def get_cleaned_data(self):
        return self.df
