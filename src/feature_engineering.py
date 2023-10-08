"File for adding features to the dataset."
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def add_time_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Function to add time, month, year etc to the dataset.

    Args:
        data (pd.DataFrame): Dataset that contains DateTime column.

    Returns:
        pd.DataFrame: Return dataset with datetime column categories.
    """
    data["Year"] = data.DateTime.dt.year
    data["Month"] = data.DateTime.dt.month
    data["Hour"] = data.DateTime.dt.hour
    data["meridian"] = data.dt.strftime("%p")
    return data
