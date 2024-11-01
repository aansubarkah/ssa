import streamlit as st
import pandas as pd

st.title("Sekolah Sabtu Auditor Memfilter Data")

df = pd.read_csv('SalesOrderHeaderMinimized.csv', sep='\t')
df['OrderDate'] = pd.to_datetime(df['OrderDate']).dt.date

#st.write(df)

st.sidebar.header('Filter Data')
teritory_ids = df['TerritoryID'].unique().tolist()
#st.write(teritory_ids)
#ids = [i for i in range(1, 11)]
id_wilayah = st.sidebar.multiselect('Pilih Territory ID', sorted(teritory_ids))
#st.write(id_wilayah)
if len(id_wilayah) > 0:
    filtered_df = df[df['TerritoryID'].isin(id_wilayah)]

#filtered_df = df[df['TerritoryID'] == id_wilayah]
#st.write(filtered_df)

df_min_date = filtered_df['OrderDate'].min()
df_max_date = filtered_df['OrderDate'].max()

#st.write(df_min_date, df_max_date)

date1 = st.sidebar.date_input('Pilih tanggal awal', min_value=df_min_date, max_value=df_max_date)
date2 = st.sidebar.date_input('Pilih tanggal akhir', min_value=df_min_date, max_value=df_max_date)

filtered_df = filtered_df[(filtered_df['OrderDate'] >= date1) & (filtered_df['OrderDate'] <= date2)]
st.write(filtered_df[['TerritoryID', 'OrderDate', 'SalesOrderID']])