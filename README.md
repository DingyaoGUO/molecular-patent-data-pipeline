# Molecular Patent Data Processing Pipeline

## Overview

This project presents a data processing pipeline for extracting and structuring experimental and molecular information from pharmaceutical patents. The workflow integrates manual curation, large language models, and cheminformatics tools to build a structured molecular dataset.

The pipeline is designed to:

* Extract experimental data from patent documents
* Organize and structure compound-level information
* Convert molecular structures into canonical SMILES
* Automate data integration into Excel-based datasets

---

## Workflow

### 1. Experimental Data Extraction

Patent PDFs are manually screened for key experimental metrics:

* IC50, EC50, DC50, Dmax
* Binding constants (Kd, Ki)
* Degradation data

Relevant tables and descriptions are:

* Extracted as images
* Converted into structured CSV using LLMs
* Parsed into Excel format

---

### 2. Molecular Structure Extraction

* Patent PDFs are processed using structure extraction tools (e.g., αExtractor)
* Molecular structures are exported as `.sdf` files
* Each molecule includes a reference label (Coreference)

---

### 3. Data Integration

* Excel tables are constructed with:

  * Patent ID
  * Compound / Example identifiers
  * Experimental data
* Data is cleaned, deduplicated, and standardized

---

### 4. Automated SMILES Extraction

Using RDKit:

* Parse `.sdf` files
* Convert structures into canonical SMILES
* Match SMILES with compound identifiers
* Append results to Excel datasets

---

### 5. File Organization

Python scripts automate:

* Organizing PDFs into folders
* Matching Excel files to patent directories
* Batch processing datasets

---

## Project Structure

```bash
src/
    organize_pdfs.py      # organize PDF files into folders
    move_excels.py        # match Excel files to patent folders
    extract_smiles.py     # extract SMILES from SDF
    batch_pipeline.py     # batch processing pipeline

examples/
    sample_data.xlsx
    sample_structures.sdf
    sample_output.xlsx
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

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
