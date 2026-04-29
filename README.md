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

---

## Project Structure

```
src/
    organize_pdfs.py
    move_excels.py
    extract_smiles.py

examples/
    sample_data.csv
    sample_structures.sdf
    sample_output.csv
    
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Single File Processing

```bash
python extract_smiles.py input.xlsx input.sdf -o output.xlsx
```

### Batch Processing

```bash
python extract_smiles.py --folder ./data
```

---

## Example

Input:

* Excel with compound identifiers
* SDF with molecular structures

Output:

* Excel file with SMILES column populated

---

## Key Technologies

* Python
* pandas
* RDKit
* OpenPyXL

---

## Applications

* Drug discovery data curation
* Molecular database construction
* Bioinformatics preprocessing
* AI-ready dataset generation

---

## Author

Dingyao Guo

---
