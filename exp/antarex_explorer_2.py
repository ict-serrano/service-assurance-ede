import pandas as pd
import numpy as np
data_dir = '/home/gabriel/Research/Aspide/EDE/data/Antarex/'

csv = 'concat_all.csv'

df = pd.read_csv(csv)

df.head(100).to_csv("concat_partial_head.csv")

df.tail(10).to_csv("concat_partial_tail.csv")