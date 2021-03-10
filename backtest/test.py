import pandas as pd
import quandl as q
import matplotlib.pyplot as plt
import numpy as np

q.ApiConfig.api_key = 'Ms91AzsAsj7GyZx25Ns6'

aapl = q.get("WIKI/AAPL", start_date="2006-10-01", end_date="2012-01-01")

print(aapl.head())