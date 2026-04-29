"""Extract canonical SMILES from SDF files and match them to compound tables.

This script supports both single-file processing and batch processing.
The compound identifier in the SDF file is expected to be stored in the
"Coreference" property, which is commonly produced by molecular structure
extraction tools.
"""

import argparse
import os
from typing import Dict, Iterable, Optional, Tuple

import pandas as pd
from rdkit import Chem


def read_sdf_molecules(sdf_path: str) -> Iterable[Tuple[str, str]]:
    """Read molecules from an SDF file and return compound references and SMILES.

    Args:
        sdf_path: Path to the input SDF file.

    Yields:
        A tuple of (compound_reference, canonical_smiles).
    """
    supplier = Chem.SDMolSupplier(sdf_path)

    for molecule in supplier:
        if molecule is None:
            continue

        compound_ref = molecule.GetProp("Coreference") if molecule.HasProp("Coreference") else ""
        compound_ref = str(compound_ref).strip()

        if not compound_ref:
            continue

        smiles = Chem.MolToSmiles(
            molecule,
            isomericSmiles=True,
            canonical=True,
        )

        yield compound_ref, smiles


def build_smiles_mapping(sdf_path: str) -> Dict[str, str]:
    """Build a dictionary mapping compound references to canonical SMILES."""
    mapping = {}

    for compound_ref, smiles in read_sdf_molecules(sdf_path):
        mapping[compound_ref] = smiles

    return mapping


def read_table(table_path: str) -> pd.DataFrame:
    """Read a CSV or Excel table into a pandas DataFrame."""
    if table_path.endswith(".csv"):
        return pd.read_csv(table_path)
    if table_path.endswith((".xlsx", ".xls")):
        return pd.read_excel(table_path)

    raise ValueError("Input table must be a CSV or Excel file.")


def write_table(df: pd.DataFrame, output_path: str) -> None:
    """Write a pandas DataFrame to CSV or Excel."""
    if output_path.endswith(".csv"):
        df.to_csv(output_path, index=False)
    elif output_path.endswith((".xlsx", ".xls")):
        df.to_excel(output_path, index=False)
    else:
        raise ValueError("Output file must be a CSV or Excel file.")


def add_smiles_to_table(
    table_path: str,
    sdf_path: str,
    output_path: Optional[str] = None,
    compound_col: str = "Compound",
    smiles_col: str = "SMILES",
) -> None:
    """Add SMILES to a compound-level table using an SDF file.

    Args:
        table_path: Path to the input CSV or Excel file.
        sdf_path: Path to the input SDF file.
        output_path: Path to save the output file. If not provided, overwrite input.
        compound_col: Column name containing compound identifiers.
        smiles_col: Output column name for SMILES strings.
    """
    if output_path is None:
        output_path = table_path

    if not os.path.exists(table_path):
        raise FileNotFoundError(f"Table file not found: {table_path}")

    if not os.path.exists(sdf_path):
        raise FileNotFoundError(f"SDF file not found: {sdf_path}")

    df = read_table(table_path)

    if compound_col not in df.columns:
        raise ValueError(f"Missing required column: {compound_col}")

    smiles_mapping = build_smiles_mapping(sdf_path)

    df[smiles_col] = (
        df[compound_col]
        .astype(str)
        .str.strip()
        .map(smiles_mapping)
    )

    matched_count = int(df[smiles_col].notna().sum())
    total_count = len(df)

    write_table(df, output_path)

    print(f"Processed: {table_path}")
    print(f"Output saved to: {output_path}")
    print(f"Matched SMILES: {matched_count}/{total_count}")


def batch_process(folder_path: str, compound_col: str = "Compound") -> None:
    """Batch process patent folders.

    Each patent folder should contain files named as:
    - <folder_name>.csv or <folder_name>.xlsx
    - <folder_name>.sdf
    """
    success = []
    failed = []

    for folder_name in os.listdir(folder_path):
        subfolder = os.path.join(folder_path, folder_name)

        if not os.path.isdir(subfolder):
            continue

        csv_path = os.path.join(subfolder, f"{folder_name}.csv")
        xlsx_path = os.path.join(subfolder, f"{folder_name}.xlsx")
        sdf_path = os.path.join(subfolder, f"{folder_name}.sdf")

        if os.path.exists(csv_path):
            table_path = csv_path
            output_path = os.path.join(subfolder, f"{folder_name}_final.csv")
        elif os.path.exists(xlsx_path):
            table_path = xlsx_path
            output_path = os.path.join(subfolder, f"{folder_name}_final.xlsx")
        else:
            print(f"Skipped {folder_name}: missing CSV or Excel file")
            failed.append(folder_name)
            continue

        if not os.path.exists(sdf_path):
            print(f"Skipped {folder_name}: missing SDF file")
            failed.append(folder_name)
            continue

        try:
            add_smiles_to_table(
                table_path=table_path,
                sdf_path=sdf_path,
                output_path=output_path,
                compound_col=compound_col,
            )
            success.append(folder_name)

        except Exception as error:
            print(f"Failed {folder_name}: {error}")
            failed.append(folder_name)

    print("\nBatch processing summary")
    print(f"Successful folders: {len(success)}")
    print(f"Failed folders: {len(failed)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract SMILES from SDF files and match them to compound identifiers."
    )

    parser.add_argument("table", nargs="?", help="Input CSV or Excel file")
    parser.add_argument("sdf", nargs="?", help="Input SDF file")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("--folder", help="Folder path for batch processing")
    parser.add_argument(
        "--compound-col",
        default="Compound",
        help="Column name for compound identifiers, e.g. Compound, Example, 化合物",
    )
    parser.add_argument(
        "--smiles-col",
        default="SMILES",
        help="Output column name for SMILES",
    )

    args = parser.parse_args()

    if args.folder:
        batch_process(args.folder, compound_col=args.compound_col)

    elif args.table and args.sdf:
        add_smiles_to_table(
            table_path=args.table,
            sdf_path=args.sdf,
            output_path=args.output,
            compound_col=args.compound_col,
            smiles_col=args.smiles_col,
        )

    else:
        raise SystemExit("Please provide either --folder or both table and sdf paths.")


if __name__ == "__main__":
    main()
