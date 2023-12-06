import pytest
import pandas as pd
from celltypegenomics import celltypefishertest

def test_celltypefishertest_integration():
    # Example Ensembl IDs for testing
    test_ensembl_ids = ['ENSG00000182389', 'ENSG00000078081', 'ENSG00000084073', 'ENSG00000119632', 'ENSG00000161267']

    # Call the function
    result = celltypefishertest(test_ensembl_ids)

    # Assertions to check integration
    # Check if the result is a DataFrame
    assert isinstance(result, pd.DataFrame)

    # Check if the DataFrame is not empty
    assert not result.empty

    # Check if the DataFrame is sorted by p-value
    assert result['p_value'].is_monotonic_increasing
