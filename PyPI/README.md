# CellTypeGenomics

## Overview
CellTypeGenomics is an open-source Python package designed to analyze the cell-type origins of genes using Human Protein Atlas (HPA) data. It helps to identify genes that are potentially over-represented or under-represented in specific cell types, providing insights that are crucial for understanding various biological processes and diseases.

The recent update made it possible to replace our numerical Human Protein Atlas (HPA) marker genes (proteinatlas.tsv) with qualitative marker genes from the human Ensemble Cell Atlas (hECA) or the Human Protein Atlas (HPA). In addition, there is an option to return tissue origins of genes using Human Protein Atlas (HPA) data.

## Key Functionality
- **Gene Analysis:** Analyzes a list of gene Ensembl IDs and returns a sorted pandas DataFrame, highlighting genes that are potentially over- or under-represented in certain cell types.
- **Data Source:** Leverages the comprehensive gene expression data available from the Human Protein Atlas (HPA) and the human Ensemble Cell Atlas (hECA).

## Installation
To install CellTypeGenomics, run the following command in your terminal:
```bash
pip install celltypegenomics
```

## Usage
Here's how to use the CellTypeGenomics package to analyze your gene list with numerical Human Protein Atlas (HPA) marker genes:

```python
from celltypegenomics import celltypefishertest

# Specify an optional alpha for significance (default: 0.05)
result = celltypefishertest(list_of_ensembl_ids, alpha=0.05)
print(result)
```
Replace `list_of_ensembl_ids` with your list of gene Ensembl IDs.

Use CellTypeGenomics package to analyze your gene list with qualitative marker genes from the human Ensemble Cell Atlas (hECA):

```python
result = celltypefishertest(list_of_ensembl_ids, heca=True)
print(result)
```

Use CellTypeGenomics package to analyze your gene list with qualitative marker genes from the Human Protein Atlas (HPA):

```python
result = celltypefishertest(list_of_ensembl_ids, hpa_marker_genes=True)
print(result)
```

Use CellTypeGenomics package to analyze your gene list with tissue origins of genes using Human Protein Atlas (HPA):

```python
result = celltypefishertest(list_of_ensembl_ids, tissue=True)
print(result)
```

## Support
For more information, updates, or to contribute to the project, please visit our [GitHub Repository](https://github.com/Zyron/CellTypeGenomics).

## License
CellTypeGenomics is released under the MIT license. See the LICENSE file for more details.
