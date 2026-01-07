# coding: utf-8
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split


def stratified_split(
        df: pd.DataFrame,
        target: str,
        test_size: float = 0.2,
        random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train_df, val_df = train_test_split(
        df,
        test_size=test_size,
        stratify=df[target],
        random_state=random_state,
    )
    return train_df, val_df
