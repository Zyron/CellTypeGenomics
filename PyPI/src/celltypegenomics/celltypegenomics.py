#pip install pandas
#pip install scipy statsmodels
import json
import pandas as pd
import pkg_resources
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests

def celltypefishertest(ensembl_ids):
    # Get the correct path for the JSON files
    cell_types_to_ensembl_path = pkg_resources.resource_filename('celltypegenomics', 'data/cell_types_to_ensembl.json')
    protein_atlas_ensembl_ids_path = pkg_resources.resource_filename('celltypegenomics', 'data/protein_atlas_ensembl_ids.json')
    
    # Read necessary JSON files
    with open(cell_types_to_ensembl_path, 'r') as f:
        cell_types_to_ensembl = json.load(f)
    with open(protein_atlas_ensembl_ids_path, 'r') as f:
        protein_atlas_ensembl_ids = json.load(f)
    
    fisher_test_results = {}
    
    for cell_type, genes in cell_types_to_ensembl.items():
        count_in_both = len(set(ensembl_ids) & set(genes))
        count_in_genelist_not_cell_type = len(ensembl_ids) - count_in_both
        count_in_cell_type_not_genelist = len(genes) - count_in_both
        count_in_neither = len(protein_atlas_ensembl_ids) - count_in_genelist_not_cell_type - count_in_cell_type_not_genelist - count_in_both
        
        table = [[count_in_both, count_in_genelist_not_cell_type], 
                 [count_in_cell_type_not_genelist, count_in_neither]]
        
        odds_ratio, p_value = fisher_exact(table, alternative='two-sided')
        
        fisher_test_results[cell_type] = {
            "p_value": p_value,
            "odds_ratio": odds_ratio,
            "count_in_both": count_in_both,
            "count_in_genelist_not_cell_type": count_in_genelist_not_cell_type,
            "count_in_cell_type_not_genelist": count_in_cell_type_not_genelist,
            "count_in_neither": count_in_neither
        }
    
    p_values = [stats["p_value"] for stats in fisher_test_results.values()]
    reject, pvals_corrected, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')
    
    for cell_type, adj_p_value in zip(fisher_test_results.keys(), pvals_corrected):
        fisher_test_results[cell_type]["adjusted_p_value"] = adj_p_value
    
    # Convert the results to a pandas DataFrame and return
    df = pd.DataFrame.from_dict(fisher_test_results, orient='index')

    # Sort the DataFrame by p-value in ascending order
    df_sorted = df.sort_values(by='p_value', ascending=True)

    return df_sorted

if __name__ == "__main__":
    # Test the function (this part will not be executed when the module is imported)
    test_ensembl_ids = ['ENSG00000182389', 'ENSG00000078081', 'ENSG00000084073', 'ENSG00000119632', 'ENSG00000161267']  # Example Ensembl IDs
    print(celltypefishertest(test_ensembl_ids))
