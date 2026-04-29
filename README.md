# Molecular Patent Data Processing Pipeline

## Overview

This project is a Python-based pipeline for organizing pharmaceutical patent files and extracting compound-level molecular information into structured datasets.

The pipeline supports:

- organizing patent PDF files into individual folders
- matching Excel files to patent folders using patent IDs
- extracting molecular structures from SDF files
- converting SDF structures into canonical SMILES using RDKit
- matching SMILES with compound identifiers
- generating structured compound-level datasets for downstream analysis

No confidential patent data is included in this repository. All example files are synthetic.

---

## Workflow

```text
Patent PDF
   ↓
Manual screening for experimental data
   ↓
Experimental table extraction
   ↓
SDF molecular structure extraction
   ↓
RDKit-based SMILES conversion
   ↓
Final structured dataset
```

---

## Project Structure

```text
molecular-patent-data-pipeline/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── extract_smiles.py
│   ├── organize_pdfs.py
│   └── move_excels.py
└── examples/
    ├── sample_data.csv
    ├── sample_structures.sdf
    └── sample_output.csv
```

---

## Installation

```bash
pip install -r requirements.txt
```

RDKit installation may depend on your Python environment. If `pip install rdkit` does not work, install it with conda:

```bash
conda install -c conda-forge rdkit
```

---

## Usage

### Extract SMILES for one file

```bash
python src/extract_smiles.py examples/sample_data.csv examples/sample_structures.sdf -o examples/sample_output.csv --compound-col Compound
```

### Batch process multiple patent folders

Expected folder structure:

```text
data/
├── PATENT001/
│   ├── PATENT001.csv
│   └── PATENT001.sdf
└── PATENT002/
    ├── PATENT002.csv
    └── PATENT002.sdf
```

Run:

```bash
python src/extract_smiles.py --folder data --compound-col Compound
```

### Organize PDF files

```bash
python src/organize_pdfs.py ./data
```

This moves each PDF file into a folder with the same name.

### Move Excel files into patent folders

```bash
python src/move_excels.py ./data
```

This reads patent IDs from the first column of each Excel file and moves the file into the matching patent folder.

---

## Example Input

| Patent ID | Compound | Target | Assay | IC50_nM | Cell Line |
|---|---|---|---|---|---|
| PATENT001 | 1 | BRD4 | Binding assay | 50 | HEK293 |
| PATENT001 | 2 | BRD4 | Binding assay | 120 | HEK293 |
| PATENT001 | 3 | CRBN | Degradation assay | 35 | MM.1S |

---

## Example Output

| Patent ID | Compound | Target | Assay | IC50_nM | Cell Line | SMILES |
|---|---|---|---|---|---|---|
| PATENT001 | 1 | BRD4 | Binding assay | 50 | HEK293 | CCO |
| PATENT001 | 2 | BRD4 | Binding assay | 120 | HEK293 | c1ccccc1 |
| PATENT001 | 3 | CRBN | Degradation assay | 35 | MM.1S | CC(=O)O |

---

## Key Technologies

- Python
- pandas
- RDKit
- openpyxl

---

## Applications

This pipeline can be used for:

- drug discovery data curation
- molecular patent data mining
- chemical database construction
- AI-ready molecular dataset preparation
- cheminformatics preprocessing

---

## Notes on Data Privacy

This repository does not include real patent data, confidential laboratory records, or internal molecular databases. The example files are synthetic and are only used to demonstrate the pipeline.

---

## Author

Dingyao Guo
