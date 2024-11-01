import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv('SalesOrderHeaderMinimized.csv', sep='\t')
df['OrderDate'] = pd.to_datetime(df['OrderDate']).dt.date
df['No'] = range(1, len(df) + 1)
first_column = df.pop('No')
df.insert(0, 'No', first_column)

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
df_grouped['Nilai'] = np.log10(df_grouped['sum'])
df_grouped['Banyak'] = np.log10(df_grouped['count'])
first_column = df_grouped.pop('No')
df_grouped.insert(0, 'No', first_column)

df_filtered_date['DayName'] = pd.to_datetime(df_filtered_date['OrderDate']).dt.day_name()
df_grouped_day = df_filtered_date.groupby('DayName')['TotalDue'].agg(['sum']).reset_index()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df_grouped_day['DayName'] = pd.Categorical(df_grouped_day['DayName'], categories=day_order, ordered=True)

df_grouped_day['No'] = range(1, len(df_grouped_day) + 1)
df_grouped_day['Nilai'] = df_grouped_day['sum']
first_column = df_grouped_day.pop('No')
df_grouped_day.insert(0, 'No', first_column)

# Main Page
st.title('Membuat Line Chart dengan Log10')

st.header('Line Chart dengan Log10')
st.line_chart(df_grouped, x='OrderDate', y=['Nilai', 'Banyak'], x_label='Tanggal', y_label='Penjualan')

st.header('Hari Terlaris')
st.bar_chart(df_grouped_day, x='DayName', y=['Nilai'], x_label='Hari', y_label='Penjualan')

st.header('Data yang difilter OrderDate')
st.dataframe(df_grouped, hide_index=True)

st.header('Semua Data')
st.dataframe(df, hide_index=True)

# Sidebar
st.sidebar.header('Filter data dan Line Chart')
