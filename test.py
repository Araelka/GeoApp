import pandas as pd
import numpy as np
import random

df = {'Дата'}
df = pd.DataFrame(df)
print(df)
new = [1]

for i in range(10):
    i = [random.random()]
    df.loc[len(df.index)] = i
print(df)