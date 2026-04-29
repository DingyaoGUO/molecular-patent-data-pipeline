# Example Files

These files are synthetic and are only used to demonstrate the pipeline.

- `sample_data.csv`: fake compound-level input table
- `sample_structures.sdf`: fake SDF file with `Coreference` fields
- `sample_output.csv`: expected output after SMILES matching

Run the example:

```bash
python src/extract_smiles.py examples/sample_data.csv examples/sample_structures.sdf -o examples/sample_output.csv --compound-col Compound
```
