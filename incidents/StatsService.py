from streamlit import cache_data

import numpy as np
import pandas as pd
import scipy.stats as stats

def compute_confidence_interval(mean_series, std_series, n_series, confidence=0.95) -> tuple:
    lower_bound = mean_series - stats.norm.ppf((1 + confidence) / 2) * std_series / np.sqrt(n_series)
    upper_bound = mean_series + stats.norm.ppf((1 + confidence) / 2) * std_series / np.sqrt(n_series)

    for i in range(len(mean_series)):
        if n_series[i] < 30:
            lower_bound[i] = mean_series[i]
            upper_bound[i] = mean_series[i]

    return lower_bound, upper_bound