"File used to process the raw excel file into processed csv"
import logging
import re
from pathlib import Path

import pandas as pd

path = Path().absolute() / "data/"
logger = logging.getLogger(__name__)


def read_excel_subway_data(excel_file: Path) -> pd.DataFrame:
    df = pd.read_excel(excel_file)
    df["DateTime"] = pd.to_datetime(df["Date"].astype("str") + " " + df["Time"])
    df.drop(columns=["Date", "Time"], inplace=True)
    return df


def combine_excel(raw_data_path: Path, processed_data_path: Path) -> pd.DataFrame:
    dfs = []
    for excel_file in raw_data_path.glob("*.xlsx"):
        # check if file name has a year
        match = re.match(".*([1-3][0-9]{3})", excel_file.name)
        if match is None:
            continue
        year = match.group(1)
        logger.info(f"{excel_file} with year {year} found. Appending to DataFrame.")
        df = read_excel_subway_data(excel_file)
        logger.info(f"DataFrame read: {df.shape}.")
        dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)

    combined_df.to_csv(
        processed_data_path / "combined_df.csv",
        index=False,
    )

    logger.info("Saving combined_df to processed.")

    return combined_df


if __name__ == "__main__":
    raw_data_path = path / "raw"
    processed_data_path = path / "processed"

    combine_excel(raw_data_path, processed_data_path)
