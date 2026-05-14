from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
DATASET_DIR = ROOT / "dataset"


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def preview_columns(columns: pd.Index) -> tuple[list[str], list[str]]:
    columns_list = list(columns)
    first_ten = columns_list[:10]
    last_five = columns_list[-5:] if len(columns_list) >= 5 else columns_list
    return first_ten, last_five


def find_label_column(columns: pd.Index) -> str | None:
    candidates = ["Label", "label", " Label"]
    for candidate in candidates:
        if candidate in columns:
            return candidate

    for column in columns:
        if str(column).strip().lower() == "label":
            return column

    return None


def print_dataframe_summary(title: str, df: pd.DataFrame) -> None:
    print(f"\n{'=' * 80}")
    print(title)
    print(f"{'=' * 80}")
    print(f"Shape: {df.shape}")

    first_ten, last_five = preview_columns(df.columns)
    print(f"First 10 columns: {first_ten}")
    print(f"Last 5 columns: {last_five}")
    print("Data types:")
    print(df.dtypes)

    label_column = find_label_column(df.columns)
    if label_column is None:
        print("Label column: Not found")
    else:
        print(f"Label column: {label_column}")
        print(f"Unique label values: {df[label_column].dropna().unique()}")


def inspect_cic_ids_2017() -> None:
    folder = DATASET_DIR / "CIC-IDS-2017" / "MachineLearningCVE"
    csv_files = sorted(folder.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {folder}")

    csv_path = csv_files[0]
    print(f"Using CIC-IDS-2017 file: {csv_path.name}")
    df = load_csv(csv_path)
    print_dataframe_summary("CIC-IDS-2017", df)


def inspect_cic_ids_2018() -> None:
    folder = DATASET_DIR / "CIC-IDS-2018"
    csv_files = sorted(folder.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {folder}")

    csv_path = csv_files[0]
    print(f"Using CIC-IDS-2018 file: {csv_path.name}")
    df = load_csv(csv_path)
    print_dataframe_summary("CIC-IDS-2018", df)


def inspect_unsw_nb15() -> None:
    data_path = DATASET_DIR / "UNSW-NB15" / "Data.csv"
    label_path = DATASET_DIR / "UNSW-NB15" / "Label.csv"

    data_df = load_csv(data_path)
    label_df = load_csv(label_path)

    print(f"\n{'=' * 80}")
    print("UNSW-NB15")
    print(f"{'=' * 80}")
    print(f"Data.csv shape: {data_df.shape}")
    print(f"Label.csv shape: {label_df.shape}")

    first_ten, last_five = preview_columns(data_df.columns)
    print(f"Data.csv first 10 columns: {first_ten}")
    print(f"Data.csv last 5 columns: {last_five}")

    label_column = label_df.columns[0]
    print(f"Label.csv unique values in '{label_column}': {label_df[label_column].dropna().unique()}")


def main() -> None:
    inspect_cic_ids_2017()
    inspect_cic_ids_2018()
    inspect_unsw_nb15()


if __name__ == "__main__":
    main()