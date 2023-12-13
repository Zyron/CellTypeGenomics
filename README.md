# CellTypeGenomics

## Overview
CellTypeGenomics is an open-source Python package designed to analyze the cell-type origins of genes using Human Protein Atlas data. It helps to identify genes that are potentially over-represented or under-represented in specific cell types, providing insights that are crucial for understanding various biological processes and diseases.

## Key Functionality
- **Gene Analysis:** Analyzes a list of gene Ensembl IDs and returns a sorted pandas DataFrame, highlighting genes that are potentially over- or under-represented in certain cell types.
- **Data Source:** Leverages the comprehensive gene expression data available from the Human Protein Atlas.

## Installation
To install CellTypeGenomics, run the following command in your terminal:
```bash
pip install celltypegenomics
```

## Usage
Here's how to use the CellTypeGenomics package to analyze your gene list:

```python
from celltypegenomics import celltypefishertest

# Optional: Specify a custom significance level with the alpha parameter (default is 0.05)
result = celltypefishertest(list_of_ensembl_ids, alpha=0.05)
print(result)
```
Replace `list_of_ensembl_ids` with your list of gene Ensembl IDs.

## Support
For more information, updates, or to contribute to the project, please visit our [GitHub Repository](https://github.com/Zyron/CellTypeGenomics).

## License
CellTypeGenomics is released under the MIT license. See the LICENSE file for more details.
