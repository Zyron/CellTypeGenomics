import unittest
import pandas as pd
from celltypegenomics import celltypefishertest

class TestCellTypeFisherTest(unittest.TestCase):

    def test_valid_input(self):
        """ Test the function with valid input """
        test_ensembl_ids = ['ENSG00000182389', 'ENSG00000078081', 'ENSG00000084073', 'ENSG00000119632', 'ENSG00000161267']
        result = celltypefishertest(test_ensembl_ids)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertNotEqual(len(result), 0)

    def test_empty_input(self):
        """ Test the function with an empty list """
        test_ensembl_ids = []
        result = celltypefishertest(test_ensembl_ids)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 135)  # Update this to the expected number

    def test_invalid_input(self):
        """ Test the function with invalid Ensembl IDs """
        test_ensembl_ids = ['INVALID_ID1', 'INVALID_ID2']
        result = celltypefishertest(test_ensembl_ids)
        self.assertIsInstance(result, pd.DataFrame)
        # Depending on function's handling of invalid IDs, adjust the assertion
        self.assertEqual(len(result), 135) # Update this to the expected number

    def test_output_structure(self):
        """ Test if the output DataFrame has the correct structure """
        test_ensembl_ids = ['ENSG00000182389', 'ENSG00000078081', 'ENSG00000084073', 'ENSG00000119632', 'ENSG00000161267']
        result = celltypefishertest(test_ensembl_ids)
        expected_columns = ['p_value', 'odds_ratio', 'count_in_both', 'count_in_genelist_not_cell_type', 
                            'count_in_cell_type_not_genelist', 'count_in_neither', 'adjusted_p_value']
        self.assertListEqual(list(result.columns), expected_columns)

if __name__ == '__main__':
    unittest.main()
