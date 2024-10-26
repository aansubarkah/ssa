import streamlit as st
import pandas as pd
from datetime import datetime

st.title('Membuat Line Chart')

df = pd.read_csv('SalesOrderHeaderMinimized.csv', sep='\t')
df['OrderDate'] = pd.to_datetime(df['OrderDate']).dt.date
df['No'] = range(1, len(df) + 1)
first_column = df.pop('No')
df.insert(0, 'No', first_column)

st.header('Data dari CSV')
#st.dataframe(df.style.hide(axis='index'))
st.dataframe(df, hide_index=True)

st.sidebar.header('Filter data dan Line Chart')

df_min_date = df['OrderDate'].min()
df_max_date = df['OrderDate'].max()

first_date = st.sidebar.date_input('Pilih tanggal Awal Data', min_value=df_min_date, max_value=df_max_date, key='first_date')
last_date = st.sidebar.date_input('Pilih tanggal Akhir Data', min_value=df_min_date, max_value=df_max_date, key='last_date')

if isinstance(first_date, str):
    first_date = datetime.strptime(first_date, '%Y-%m-%d').date()
if isinstance(last_date, str):
    last_date = datetime.strptime(last_date, '%Y-%m-%d').date()

df_filtered_date = df[(df['OrderDate'] >= first_date) & (df['OrderDate'] <= last_date)]
df_filtered_date = df_filtered_date.drop(columns=['No'])
df_filtered_date['No'] = range(1, len(df_filtered_date) + 1)
first_column = df_filtered_date.pop('No')
df_filtered_date.insert(0, 'No', first_column)

df_grouped = df_filtered_date.groupby('OrderDate')['TotalDue'].agg(['sum', 'count']).reset_index()
df_grouped['No'] = range(1, len(df_grouped) + 1)
first_column = df_grouped.pop('No')
df_grouped.insert(0, 'No', first_column)

st.header('Data yang difilter OrderDate')
st.dataframe(df_grouped, hide_index=True)

st.line_chart(df_grouped, x='OrderDate', y=['sum', 'count'], x_label='Tanggal', y_label='Total Penjualan')
