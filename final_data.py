import pandas as pd
import os

# Path to the directory containing CSV files
data_dir = 'data'

# List to store dataframes from each CSV file
dfs = []

# Read and process each CSV file
for filename in os.listdir(data_dir):
    if filename.endswith('.csv'):
        filepath = os.path.join(data_dir, filename)
        df = pd.read_csv(filepath)
        
        df = df[df['product'] == 'pink morsel']
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df['price'] = pd.to_numeric(df['price'].str.replace('$', ''), errors='coerce')
        df = df.dropna(subset=['quantity', 'price'])
        df['sales'] = df['quantity'] * df['price']
        df = df[['sales', 'date', 'region']]
        dfs.append(df)


output_df = pd.concat(dfs, ignore_index=True)
output_df.to_csv('formatted_output.csv', index=False)
