"Main file for Toronto dataset"
import logging
from pathlib import Path

import pandas as pd

from src.data_loader import combine_excel
from src.feature_engineering import add_time_columns
from src.ingest_data import get_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger()

data_folder_path = Path().absolute() / "data/"
raw_data_path = data_folder_path / "raw/"
processed_data_path = data_folder_path / "processed"


def main():
    "Main function to load Toronto data end to end."
    logger.info("Running logger function.")
    # get subway data from url
    get_data(raw_data_path)

    logger.info(f"Downloaded subway data successfully, saved in {raw_data_path}.")

    combine_excel(raw_data_path, processed_data_path)

    logger.info(f"Processed subway data successfully, saved in {processed_data_path}.")

    data = pd.read_csv(
        processed_data_path / "combined_df.csv", parse_dates=["DateTime"]
    )

    data = add_time_columns(data)
