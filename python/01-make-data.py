import os
os.chdir("/home/evan/Documents/columbia/jtc/w10/d1/python")
## https://www.ncdc.noaa.gov/cdo-web/datasets
import pandas as pd


dfx = pd.read_csv("1-1-2017_12-31-2019.csv")
dfx.shape
dfx.columns
dfx.info()
dfx.tail()
station_counts = dfx['STATION'].value_counts()
station_counts[station_counts == 1095]
# df.query('STATION == USW00054787', inplace=False) = GO BACK TO LATER
dfx['DATE'] = pd.to_datetime(dfx['DATE'])

dfx.info()
df1 = dfx[dfx['STATION'] == 'USW00094728'].copy()
df1.info()
df1.sort_values('DATE', ascending=True)
df1.head()
df1 = df1.dropna(axis=1, how='any')
df1.info()
def clean_data(original):
    clean_df = original[original['STATION'] == 'USW00094728'].copy()
    clean_df = clean_df.dropna(axis=1, how='any')
    clean_df['DATE'] = pd.to_datetime(clean_df['DATE'])
    return clean_df

original_df2 = pd.read_csv("1-1-2020_12-31-2022.csv")
original_df3 = pd.read_csv("1-1-2023_today.csv")


df2 = clean_data(original_df2)
df3 = clean_data(original_df3)

df2.info()
df3.info()


df = pd.concat([df1, df2, df3], ignore_index=True)
df = pd.concat([df2, df3], ignore_index=True)
df.info()


# In[21]:


df = df.drop(columns=['NAME'])
### Create weather_history.csv

df_renamed = df.rename(columns={"TMAX": "temperature",
                                "DATE": "date"})

df_renamed.to_csv("weather_history.csv", index=False)
