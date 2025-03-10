import argparse
import os
from pathlib import Path

import pandas as pd

def get_project_root() -> Path:
    """Returns the project root directory."""
    return Path(__file__).parent.parent

def clean_data(country: str = "PT") -> None:
    """Cleans data and saves to csv.
    args:
        country: Country code.
    """
    data_path = Path(os.getcwd()) / "data"
    df = pd.read_csv(data_path / "eu_life_expectancy_raw.tsv", sep="\t")

    # Split columns
    df[["unit", "sex", "age", "region"]] = df["unit,sex,age,geo\\time"].str.split(
        ",", expand=True
    )

    # Drop
    df.drop(columns=["unit,sex,age,geo\\time"], inplace=True)

    # Strip any trailing spaces in the year columns
    df.columns = df.columns.str.strip()

    # Unpivot the data (convert from wide to long format)
    df_long = df.melt(
        id_vars=["unit", "sex", "age", "region"], var_name="year", value_name="value"
    )
    del df

    # Enforce data types
    df_long["year"] = df_long["year"].astype(int)

    df_long["value"] = (
        df_long["value"].str.extract(r"(\d+\.\d+)").astype(float)
    )  # remove non numeric

    # Filter
    df_long = df_long.loc[df_long["region"] == country]

    df_long.to_csv(data_path / "pt_life_expectancy.csv", index=False)


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description="Clean life expectancy data")
    parser.add_argument(
        "--county",
        type=str,
        default="PT",
        help="Specify the country code to filter by (default: PT).",
    )
    args = parser.parse_args()
    clean_data()
