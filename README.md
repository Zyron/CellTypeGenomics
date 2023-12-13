# CellTypeGenomics

## Overview
CellTypeGenomics is an open-source Python package designed to analyze the cell-type origins of genes using Human Protein Atlas data. It aims to provide insights into the potential over-representation of genes in specific cell types.

## Key Functionality
- **Gene Analysis:** Takes a list of gene Ensembl IDs and returns a prioritized list highlighting genes potentially over-represented in certain cell types.
- **Data Source:** Utilizes data from the Human Protein Atlas for analysis.

## Installation
```bash
pip install celltypegenomics
```

## Usage
```python
from celltypegenomics import celltypefishertest

# Optional alpha parameter (default is 0.05)
result = celltypefishertest(list_of_ensembl_ids, alpha=0.05)
print(result)
```

Replace `list_of_ensembl_ids` with your gene Ensembl IDs.

For more information and updates, visit our [GitHub Repository](https://github.com/Zyron/CellTypeGenomics).
