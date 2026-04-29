# Example Data

This folder contains synthetic example files only.

- `sample_data.xlsx`: a fake patent compound table
- `sample_structures.sdf`: fake molecular structures with Coreference fields
- `sample_output.xlsx`: expected output after running the pipeline

Run:

```bash
python ../src/extract_smiles.py sample_data.xlsx sample_structures.sdf -o sample_output.xlsx --compound-col Compound
```
