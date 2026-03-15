import pandas as pd

nav_df = pd.read_csv('data/nav_120542.csv')
nav_df['nav'] = nav_df['nav'].ffill()
nav_df.to_csv('data/nav_120542.csv', index=False)
print('Corrected missing NAVs in nav_120542.csv')
