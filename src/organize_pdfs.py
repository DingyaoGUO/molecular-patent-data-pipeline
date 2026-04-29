"""Organize patent PDF files into folders with matching names."""

import argparse
import shutil
from pathlib import Path


def organize_pdfs(source_dir: str) -> None:
    """Move each PDF file into a folder with the same base name.

    Example:
        PATENT001.pdf -> PATENT001/PATENT001.pdf
    """
    source_path = Path(source_dir)

    if not source_path.exists():
        raise FileNotFoundError(f"Directory not found: {source_dir}")

    pdf_files = list(source_path.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {source_dir}")
        return

    for pdf_path in pdf_files:
        folder_name = pdf_path.stem
        target_folder = source_path / folder_name
        target_folder.mkdir(exist_ok=True)

        target_path = target_folder / pdf_path.name
        shutil.move(str(pdf_path), str(target_path))

        print(f"Moved: {pdf_path.name} -> {target_folder.name}/")

    print("PDF organization completed.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Organize PDF files into matching folders."
    )
    parser.add_argument("source_dir", help="Directory containing PDF files")
    args = parser.parse_args()

    organize_pdfs(args.source_dir)


if __name__ == "__main__":
    main()
