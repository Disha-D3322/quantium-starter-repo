import pandas as pd
import os

# Define the path to the data folder
data_folder = os.path.join('data')

# List of CSV files to process
csv_files = ['daily_sales_data_0.csv', 'daily_sales_data_1.csv', 'daily_sales_data_2.csv']

# Initialize an empty list to store dataframes
dataframes = []

# Loop through each CSV file
for csv_file in csv_files:
    # Load the CSV file into a pandas DataFrame
    file_path = os.path.join(data_folder, csv_file)
    df = pd.read_csv(file_path)
    
    # Filter the rows where product is 'pink morsel'
    df = df[df['product'] == 'pink morsel']
    df['price'] = df['price'].replace({'\$': ''}, regex=True).astype(float)
    # Calculate the 'sales' column by multiplying 'quantity' and 'price'
    df['sales'] = df['quantity'] * df['price']
    
    # Select only the 'sales', 'date', and 'region' columns
    df = df[['sales', 'date', 'region']]
    
    # Append the dataframe to the list
    dataframes.append(df)

# Concatenate all dataframes into a single dataframe
final_df = pd.concat(dataframes, ignore_index=True)

# Output the result to a new CSV file
output_file = os.path.join('data', 'formatted_sales_data.csv')
final_df.to_csv(output_file, index=False)

print(f"Formatted data saved to {output_file}")
