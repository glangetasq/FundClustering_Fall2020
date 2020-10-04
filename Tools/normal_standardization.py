# Normalize each columns of a panda data frame as (X-mu)/sigma

import numpy as np
import pandas as pd


def normal_standardization(df : pd.DataFrame) -> pd.DataFrame:

    for column in df.columns:

        df[column] = (df[column] - df[column].mean()) / np.std(df[column])

    return df
