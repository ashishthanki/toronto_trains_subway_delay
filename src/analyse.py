"File used to analyse processed subway delay data."

import pandas as pd


def calculate_metrics(sub_category: pd.DataFrame) -> pd.Series:
    """Function used to calculate subway delay metrics.

    Args:
        sub_category (pd.DataFrame): Sub category from a given column.

    Returns:
        pd.Series: Series of metrics used for data analysis.
    """
    metrics = {}
    no_delay_count = sub_category[sub_category["Min Delay"] == 0].shape[0]
    total_service_count = sub_category.shape[0]

    # return 0 if there are no on-time services
    if no_delay_count == 0:
        sub_category["on_time_perc_performance"] = 0.0

    metrics["on_time_perc_performance"] = no_delay_count * 100 / total_service_count
    metrics["total_service_count"] = total_service_count
    metrics["total_delay"] = sub_category["Min Delay"].sum()

    return pd.Series(metrics)


def top_5_delays(data: pd.DataFrame) -> dict:
    return
