import pytest
import pandas as pd
from celltypegenomics import celltypefishertest

def test_celltypefishertest_integration():
    # Example Ensembl IDs for testing
    test_ensembl_ids = ['ENSG00000182389', 'ENSG00000078081', 'ENSG00000084073', 'ENSG00000119632', 'ENSG00000161267']

    # Define alpha value
    alpha = 0.05
        
    # Call the function
    result = celltypefishertest(test_ensembl_ids, alpha)

    # Assertions to check integration
    # Check if the result is a DataFrame
    assert isinstance(result, pd.DataFrame)

    # Check if the DataFrame is not empty
    assert not result.empty

    # Check if the DataFrame is sorted by p-value
    assert result['p_value'].is_monotonic_increasing

    # Check if the DataFrame has the correct columns
    assert result.columns.tolist() == ['p_value', 'odds_ratio', 'count_in_both', 'count_in_genelist_not_cell_type', 'count_in_cell_type_not_genelist', 'count_in_neither', 'adjusted_p_value']
