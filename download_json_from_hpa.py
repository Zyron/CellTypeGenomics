#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests

def download_file(url, save_path):
    """
    Download a file from a given URL and save it to a specified path.
    
    Args:
    - url (str): The URL of the file to be downloaded.
    - save_path (str): The local path where the file should be saved.
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an error for bad responses
    
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

# Example usage:
# Assuming you've identified the exact URL of the file you want
file_url = "http://www.proteinatlas.org/ENSG00000134057.json"
local_path = "C:/Users/alexm/Human_Protein_Atlas/ENSG00000134057.json"

download_file(file_url, local_path)


# In[ ]:


import requests
from bs4 import BeautifulSoup

def download_files_from_hpa(url, max_size_gb=1):
    # Convert the max size from GB to bytes
    max_size_bytes = max_size_gb * 1e9

    # Make an HTTP GET request to the provided URL
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Search for all <a> tags with the specified href structure
    links = soup.find_all('a', href=True)

    # Base URL to prepend to relative file paths
    base_url = "https://www.proteinatlas.org"

    for link in links:
        file_url = link['href']
        if file_url.endswith('.zip'):  # Check if the link is to a .zip file
            full_url = base_url + file_url

            # Check file size without downloading the entire file
            file_response = requests.head(full_url)
            file_size = int(file_response.headers.get('Content-Length', 0))

            if file_size <= max_size_bytes:
                # Download the file if it's within the size limit
                filename = file_url.split('/')[-1]  # Extract filename from the URL
                print(f"Downloading {filename}...")
                file_response = requests.get(full_url, stream=True)
                with open(filename, 'wb') as file:
                    for chunk in file_response.iter_content(chunk_size=8192):
                        file.write(chunk)
                print(f"{filename} downloaded!")
            else:
                print(f"Skipping {filename} as it exceeds the size limit.")

# Example usage
download_files_from_hpa("https://www.proteinatlas.org/about/download")


# In[ ]:


import pandas as pd

def process_and_sort_tsv(input_file_path, output_file_path):
    # Read the tsv file into a DataFrame
    df = pd.read_csv(input_file_path, sep='\t')

    # Extract the 'Ensembl gene ID' and 'Cell type' columns
    extracted_df = df[['Gene', 'Cell type']]

    # Sort by 'Cell type'
    sorted_df = extracted_df.sort_values(by='Cell type')
    
    # Save the sorted data to a new .tsv file
    sorted_df.to_csv(output_file_path, sep='\t', index=False)
    print(f"Sorted data saved to {output_file_path}")

# Example usage
process_and_sort_tsv('\normal_tissue.tsv\normal_tissue.tsv', '\sorted_data\sorted_normal_tissue.tsv')


# In[ ]:


import os
import json
import pandas as pd

# Directory containing the .tsv files
directory = "C:\\Users\\alexm\\Human Protein Atlas"

# Extract Ensembl Gene IDs from all .tsv files and store in a set (to avoid duplicates)
ensembl_gene_ids = set()

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.tsv'):
        filepath = os.path.join(directory, filename)
        # Read the tsv file into a DataFrame
        df = pd.read_csv(filepath, sep='\t')
        if 'Gene' in df.columns:
            ensembl_gene_ids.update(df['Gene'].unique())

# Convert set to list (for JSON serialization)
ensembl_gene_ids_list = list(ensembl_gene_ids)

# Write the Ensembl Gene IDs to a .json file
output_path = os.path.join(directory, "ensembl_gene_ids.json")
with open(output_path, 'w') as json_file:
    json.dump(ensembl_gene_ids_list, json_file)

print(f"Ensembl Gene IDs written to: {output_path}")


# In[ ]:


import pandas as pd

# Read the provided tsv file into a DataFrame again
df_normal_tissue = pd.read_csv("C:/Users/alexm/Human Protein Atlas/normal_tissue.tsv/normal_tissue.tsv", sep='\t')

# Extract the unique Ensembl Gene IDs
ensembl_gene_ids_normal_tissue = df_normal_tissue['Gene'].unique().tolist()

ensembl_gene_ids_normal_tissue[:10], len(ensembl_gene_ids_normal_tissue)  # Display the first 10 IDs and the total count

print(ensembl_gene_ids_normal_tissue[:])


# In[ ]:


import os
import pandas as pd
import json

# Directory containing the .tsv files
directory = "C:/Users/alexm/Human Protein Atlas"

# Set to hold unique Ensembl Gene IDs from all files
ensembl_gene_ids_aggregated = set()

# Iterate over all files in the directory
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    
    # Check if the entry is a file and has a .tsv extension
    if os.path.isfile(filepath) and filename.endswith('.tsv'):
        print(f"Reading file: {filepath}")
        
        # Read the .tsv file into a DataFrame
        df = pd.read_csv(filepath, sep='\t')
        
        if 'Gene' in df.columns:
            print(f"Found 'Gene' column in {filename}. Number of unique IDs: {len(df['Gene'].unique())}")
            ensembl_gene_ids_aggregated.update(df['Gene'].unique())
        else:
            print(f"'Gene' column not found in {filename}. Columns are: {df.columns.tolist()}")

# Convert the set to a list for JSON serialization
ensembl_gene_ids_list = list(ensembl_gene_ids_aggregated)

# Write the aggregated Ensembl Gene IDs to a .json file
output_path = os.path.join(directory, "aggregated_ensembl_gene_ids.json")
with open(output_path, 'w') as json_file:
    json.dump(ensembl_gene_ids_list, json_file)

print(f"Ensembl Gene IDs from all files written to: {output_path}")


# In[2]:


import pandas as pd
import json

# Optimized approach to aggregate Ensembl Gene IDs by cell type

# Read both files into DataFrames
df_normal_tissue = pd.read_csv("C:/Users/alexm/Human Protein Atlas/normal_tissue.tsv/normal_tissue.tsv", sep='\t')
df_rna_single_cell = pd.read_csv("C:/Users/alexm/Human Protein Atlas/rna_single_cell_type.tsv/rna_single_cell_type.tsv", sep='\t')
df_rna_single_cell_tissue = pd.read_csv("C:/Users/alexm/Human Protein Atlas/rna_single_cell_type_tissue.tsv/rna_single_cell_type_tissue.tsv", sep='\t')

# Filter rows where 'Gene' column is not NaN for both dataframes
df_normal_tissue = df_normal_tissue[df_normal_tissue['Gene'].notna()]
df_rna_single_cell = df_rna_single_cell[df_rna_single_cell['Gene'].notna()]
df_rna_single_cell_tissue = df_rna_single_cell_tissue[df_rna_single_cell_tissue['Gene'].notna()]

# Group by 'Cell type' and aggregate unique 'Gene' values
grouped_normal_tissue = df_normal_tissue.groupby('Cell type')['Gene'].unique()
grouped_rna_single_cell = df_rna_single_cell.groupby('Cell type')['Gene'].unique()
grouped_rna_single_cell_tissue = df_rna_single_cell_tissue.groupby('Cell type')['Gene'].unique()

# Merge the three groupings
ensembl_gene_ids_by_cell_type = {}
for cell_type, gene_ids in grouped_normal_tissue.items():
    ensembl_gene_ids_by_cell_type[cell_type] = list(gene_ids)
for cell_type, gene_ids in grouped_rna_single_cell.items():
    if cell_type in ensembl_gene_ids_by_cell_type:
        ensembl_gene_ids_by_cell_type[cell_type] = list(set(ensembl_gene_ids_by_cell_type[cell_type] + list(gene_ids)))
    else:
        ensembl_gene_ids_by_cell_type[cell_type] = list(gene_ids)
for cell_type, gene_ids in grouped_rna_single_cell_tissue.items():
    if cell_type in ensembl_gene_ids_by_cell_type:
        ensembl_gene_ids_by_cell_type[cell_type] = list(set(ensembl_gene_ids_by_cell_type[cell_type] + list(gene_ids)))
    else:
        ensembl_gene_ids_by_cell_type[cell_type] = list(gene_ids)

# Save the aggregated results to a JSON file
output_path = "C:/Users/alexm/Human Protein Atlas/aggregated_ensembl_gene_ids_by_cell_type_jupyter.json"
with open(output_path, 'w') as json_file:
    json.dump(ensembl_gene_ids_by_cell_type, json_file)

output_path


# In[5]:


import pandas as pd
import json
import os

# Ask the user for the directory containing the files or set it through configuration
directory_path = input("Please enter the directory path containing the TSV files: ")

# Construct paths to the files
path_normal_tissue = os.path.join(directory_path, "normal_tissue.tsv", "normal_tissue.tsv")
path_rna_single_cell = os.path.join(directory_path, "rna_single_cell_type.tsv", "rna_single_cell_type.tsv")
path_rna_single_cell_tissue = os.path.join(directory_path, "rna_single_cell_type_tissue.tsv", "rna_single_cell_type_tissue.tsv")

# Read the files into DataFrames
df_normal_tissue = pd.read_csv(path_normal_tissue, sep='\t')
df_rna_single_cell = pd.read_csv(path_rna_single_cell, sep='\t')
df_rna_single_cell_tissue = pd.read_csv(path_rna_single_cell_tissue, sep='\t')

print("Normal Tissue Data:")
print(df_normal_tissue.head())

print("\nRNA Single Cell Data:")
print(df_rna_single_cell.head())

print("\nRNA Single Cell Tissue Data:")
print(df_rna_single_cell_tissue.head())

# Save the aggregated results to a JSON file
output_path = os.path.join(directory_path, "aggregated_ensembl_gene_ids_by_cell_type_jupyter.json")
with open(output_path, 'w') as json_file:
    json.dump(ensembl_gene_ids_by_cell_type, json_file)

print(f"Results saved to: {output_path}")

# Load the data from the JSON file
with open(output_path, 'r') as json_file:
    ensembl_gene_ids_by_cell_type_loaded = json.load(json_file)

# Print the first 5 rows of the loaded data
first_5_items = dict(list(ensembl_gene_ids_by_cell_type_loaded.items())[:5])
for cell_type, gene_ids in first_5_items.items():
    print(f"Cell Type: {cell_type}\nGene IDs: {gene_ids}\n")


# In[ ]:


import os
print(os.getcwd())


# In[8]:


import pandas as pd
import os
import json

# Ask the user for the directory containing the files or set it through configuration
directory_path = input("Please enter the directory path containing the TSV files: ")

# Construct paths to the files
path_normal_tissue = os.path.join(directory_path, "normal_tissue.tsv", "normal_tissue.tsv")
path_rna_single_cell = os.path.join(directory_path, "rna_single_cell_type.tsv", "rna_single_cell_type.tsv")
path_rna_single_cell_tissue = os.path.join(directory_path, "rna_single_cell_type_tissue.tsv", "rna_single_cell_type_tissue.tsv")

# Read the files into DataFrames
df_normal_tissue = pd.read_csv(path_normal_tissue, sep='\t')
df_rna_single_cell = pd.read_csv(path_rna_single_cell, sep='\t')
df_rna_single_cell_tissue = pd.read_csv(path_rna_single_cell_tissue, sep='\t')

# Filter rows where 'Gene' column is not NaN for all dataframes
dfs = [df_normal_tissue, df_rna_single_cell, df_rna_single_cell_tissue]
for df in dfs:
    df.dropna(subset=['Gene'], inplace=True)

# Create an empty DataFrame to hold the aggregated results
ensembl_gene_ids_by_cell_type = pd.DataFrame(columns=['Cell Type', 'Gene IDs'])

# Aggregate unique 'Gene' values by 'Cell type'
for df in dfs:
    grouped = df.groupby('Cell type')['Gene'].unique().reset_index()
    grouped.columns = ['Cell Type', 'Gene IDs']
    ensembl_gene_ids_by_cell_type = pd.concat([ensembl_gene_ids_by_cell_type, grouped], ignore_index=True)

# Group by 'Cell type' and merge gene lists
ensembl_gene_ids_by_cell_type['Gene IDs'] = ensembl_gene_ids_by_cell_type['Gene IDs'].apply(lambda x: set(x))
ensembl_gene_ids_by_cell_type = ensembl_gene_ids_by_cell_type.groupby('Cell Type').agg(lambda x: list(set().union(*x))).reset_index()

# Convert the DataFrame to a dictionary format suitable for JSON serialization
result_dict = dict(zip(ensembl_gene_ids_by_cell_type['Cell Type'], ensembl_gene_ids_by_cell_type['Gene IDs']))
result_dict = {key: list(value) for key, value in result_dict.items()}

# Save the aggregated results to a JSON file
output_path = os.path.join(directory_path, "aggregated_ensembl_gene_ids_by_cell_type_jupyter.json")
with open(output_path, 'w') as json_file:
    json.dump(result_dict, json_file)

# Load the data from the JSON file
with open(output_path, 'r') as json_file:
    ensembl_gene_ids_by_cell_type_loaded = json.load(json_file)

# Print the first 5 rows of the loaded data
first_5_items = dict(list(ensembl_gene_ids_by_cell_type_loaded.items())[:5])
for cell_type, gene_ids in first_5_items.items():
    print(f"Cell Type: {cell_type}\nGene IDs: {gene_ids[:5]}\n")


# In[9]:


import pandas as pd

# Read the three files into DataFrames
df_immune_cell = pd.read_csv("C:/Users/alexm/Human Protein Atlas/rna_immune_cell.tsv/rna_immune_cell.tsv", sep='\t')
df_immune_cell_monaco = pd.read_csv("C:/Users/alexm/Human Protein Atlas/rna_immune_cell_monaco.tsv/rna_immune_cell_monaco.tsv", sep='\t')
df_immune_cell_schmiedel = pd.read_csv("C:/Users/alexm/Human Protein Atlas/rna_immune_cell_schmiedel.tsv/rna_immune_cell_schmiedel.tsv", sep='\t')


# Check the columns of each DataFrame to identify the columns corresponding to cell type and gene IDs
df_columns = {
    "rna_immune_cell": df_immune_cell.columns.tolist(),
    "rna_immune_cell_monaco": df_immune_cell_monaco.columns.tolist(),
    "rna_immune_cell_schmiedel": df_immune_cell_schmiedel.columns.tolist()
}

df_columns


# Group by 'Immune cell' and aggregate unique 'Gene' values for each file
grouped_immune_cell = df_immune_cell.groupby('Immune cell')['Gene'].unique()
grouped_immune_cell_monaco = df_immune_cell_monaco.groupby('Immune cell')['Gene'].unique()
grouped_immune_cell_schmiedel = df_immune_cell_schmiedel.groupby('Immune cell')['Gene'].unique()

# Merge the three groupings
ensembl_gene_ids_by_immune_cell_type = {}
for immune_cell_type, gene_ids in grouped_immune_cell.items():
    ensembl_gene_ids_by_immune_cell_type[immune_cell_type] = list(gene_ids)
for immune_cell_type, gene_ids in grouped_immune_cell_monaco.items():
    if immune_cell_type in ensembl_gene_ids_by_immune_cell_type:
        ensembl_gene_ids_by_immune_cell_type[immune_cell_type] = list(set(ensembl_gene_ids_by_immune_cell_type[immune_cell_type] + list(gene_ids)))
    else:
        ensembl_gene_ids_by_immune_cell_type[immune_cell_type] = list(gene_ids)
for immune_cell_type, gene_ids in grouped_immune_cell_schmiedel.items():
    if immune_cell_type in ensembl_gene_ids_by_immune_cell_type:
        ensembl_gene_ids_by_immune_cell_type[immune_cell_type] = list(set(ensembl_gene_ids_by_immune_cell_type[immune_cell_type] + list(gene_ids)))
    else:
        ensembl_gene_ids_by_immune_cell_type[immune_cell_type] = list(gene_ids)

# Save the aggregated results to a JSON file
import json
output_path_immune = "C:/Users/alexm/Human Protein Atlas/aggregated_ensembl_gene_ids_by_immune_cell_type.json"
with open(output_path_immune, 'w') as json_file:
    json.dump(ensembl_gene_ids_by_immune_cell_type, json_file)

output_path_immune


# In[ ]:




