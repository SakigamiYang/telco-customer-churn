# coding: utf-8
import pandas as pd
from loguru import logger
from tabulate import tabulate

__all__ = [
    "log_dataframe",
]


def log_dataframe(data, message="Data", max_rows=None, tablefmt='psql'):
    """
    Print DataFrame or Series as a table using loguru

    Parameters:
    -----------
    df : pd.DataFrame or pd.Series
        Data to be logged
    message : str
        Description message
    max_rows : int
        Maximum number of rows to display
    tablefmt : str
        Table format ('psql', 'grid', 'fancy_grid', 'github', 'pretty')
    """
    # Convert Series to DataFrame if needed
    if isinstance(data, pd.Series):
        display_data = data.to_frame()
    else:
        display_data = data

    shape_info = display_data.shape

    # Limit rows if specified
    if max_rows:
        display_data = display_data.head(max_rows)

    table_str = tabulate(display_data, headers='keys', tablefmt=tablefmt, showindex=True)
    logger.info(f"{message} ({shape_info}):\n{table_str}")
