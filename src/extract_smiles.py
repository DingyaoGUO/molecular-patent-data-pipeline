import os
import pandas as pd
from rdkit import Chem
import argparse


def sdf_molecules(sdf_path: str):
    """从 SDF 中读取 (Coreference, SMILES)"""
    suppl = Chem.SDMolSupplier(sdf_path)

    for mol in suppl:
        if mol is None:
            continue

        coref = mol.GetProp("Coreference") if mol.HasProp("Coreference") else ""
        smiles = Chem.MolToSmiles(mol, isomericSmiles=True, canonical=True)

        yield coref, smiles


def main(xlsx_path, sdf_path, out_path=None, column_name="Compound"):
    """单个文件处理"""
    if out_path is None:
        out_path = xlsx_path

    df = pd.read_excel(xlsx_path)

    if column_name not in df.columns:
        raise ValueError(f" xlsx 中缺少 '{column_name}' 列")

    if "SMILES" not in df.columns:
        df["SMILES"] = None

    # 建立编号 → 行号映射
    no2idx = {str(v): idx for idx, v in df[column_name].dropna().items()}

    for coref, smiles in sdf_molecules(sdf_path):
        if coref is None:
            continue

        if str(coref) in no2idx:
            row_idx = no2idx[str(coref)]
            df.at[row_idx, "SMILES"] = smiles

    df.to_excel(out_path, index=False)
    print(f" 完成：{out_path}")


def batch_process(folder_path, column_name="Compound"):
    """批量处理"""
    success = []
    failed = []

    for name in os.listdir(folder_path):
        sub_path = os.path.join(folder_path, name)

        if not os.path.isdir(sub_path):
            continue

        xlsx_path = os.path.join(sub_path, f"{name}.xlsx")
        sdf_path = os.path.join(sub_path, f"{name}.sdf")
        out_path = os.path.join(sub_path, f"{name}_final.xlsx")

        if os.path.exists(out_path):
            print(f" 已存在，跳过：{name}")
            continue

        if not os.path.exists(xlsx_path) or not os.path.exists(sdf_path):
            print(f" 缺文件：{name}")
            failed.append(name)
            continue

        try:
            print(f" 处理：{name}")
            main(xlsx_path, sdf_path, out_path, column_name)
            success.append(name)
        except Exception as e:
            print(f" 失败：{name}，错误：{e}")
            failed.append(name)

    print("\n 成功：")
    for s in success:
        print("  -", s)

    print("\n 失败：")
    for f in failed:
        print("  -", f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("xlsx", nargs="?", help="xlsx路径")
    parser.add_argument("sdf", nargs="?", help="sdf路径")
    parser.add_argument("-o", "--out", help="输出路径")
    parser.add_argument("--folder", help="批量处理文件夹")
    parser.add_argument(
        "--col",
        default="Compound",
        help="列名：Compound / Example / 化合物",
    )

    args = parser.parse_args()

    if args.folder:
        batch_process(args.folder, args.col)
    elif args.xlsx and args.sdf:
        main(args.xlsx, args.sdf, args.out, args.col)
    else:
        print("请提供参数")
