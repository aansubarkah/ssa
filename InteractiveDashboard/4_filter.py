import streamlit as st
import pandas as pd
from datetime import datetime

st.title('Membuat Filter')

df = pd.read_csv('SalesOrderHeaderMinimized.csv', sep='\t')
df['OrderDate'] = pd.to_datetime(df['OrderDate']).dt.date

st.header('Data dari CSV')
st.write(df)

st.sidebar.header('Filter data')

teritoryids = df['TerritoryID'].unique().tolist()

teritoryid = st.sidebar.selectbox('Pilih TerritoryID', teritoryids)

filtered_df = df[df['TerritoryID'] == teritoryid]
st.header('Data yang difilter')
st.dataframe(filtered_df)

df_min_date = df['OrderDate'].min()
df_max_date = df['OrderDate'].max()

first_date = st.sidebar.date_input('Pilih tanggal Awal Data', min_value=df_min_date, max_value=df_max_date, key='first_date')
last_date = st.sidebar.date_input('Pilih tanggal Akhir Data', min_value=df_min_date, max_value=df_max_date, key='last_date')

if isinstance(first_date, str):
    first_date = datetime.strptime(first_date, '%Y-%m-%d').date()
if isinstance(last_date, str):
    last_date = datetime.strptime(last_date, '%Y-%m-%d').date()

df_filtered_date = df[(df['OrderDate'] >= first_date) & (df['OrderDate'] <= last_date)]

st.header('Data yang difilter OrderDate')
st.dataframe(df_filtered_date)
