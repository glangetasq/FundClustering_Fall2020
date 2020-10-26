# Normalize each columns of a panda data frame as (X-mu)/sigma

import numpy as np
import pandas as pd


def normal_standardization(df_ : pd.DataFrame) -> pd.DataFrame:

    df = df_.copy()
    for column in df.columns:

        if not np.std(df[column]) == 0:
            df[column] = (df[column] - df[column].mean()) / np.std(df[column])
        else:
            df[column] = 0

    return df
