import streamlit as st
import pandas as pd

st.title("Sekolah Sabtu Auditor Membuat Line Chart")

df = pd.read_csv('SalesOrderHeaderMinimized.csv', sep='\t')
df['OrderDate'] = pd.to_datetime(df['OrderDate']).dt.date

#st.write(df)

st.sidebar.header('Filter Data')
#teritory_ids = df['TerritoryID'].unique().tolist()
#st.write(teritory_ids)
#ids = [i for i in range(1, 11)]
#id_wilayah = st.sidebar.multiselect('Pilih Territory ID', sorted(teritory_ids))
#st.write(id_wilayah)
#if len(id_wilayah) > 0:
#    filtered_df = df[df['TerritoryID'].isin(id_wilayah)]

#filtered_df = df[df['TerritoryID'] == id_wilayah]
#st.write(filtered_df)

df_min_date = df['OrderDate'].min()
df_max_date = df['OrderDate'].max()

#st.write(df_min_date, df_max_date)

date1 = st.sidebar.date_input('Pilih tanggal awal', min_value=df_min_date, max_value=df_max_date)
date2 = st.sidebar.date_input('Pilih tanggal akhir', min_value=df_min_date, max_value=df_max_date)

filtered_df = df[(df['OrderDate'] >= date1) & (df['OrderDate'] <= date2)]

#filtered_group = filtered_df.groupby('OrderDate')['TotalDue'].sum().reset_index()
filtered_group = filtered_df.groupby('OrderDate')['TotalDue'].agg(['sum', 'count']).reset_index()


#filtered_group = filtered_group.sort_values('TotalDue', ascending=False)
filtered_group['Nomor'] = range(1, len(filtered_group) + 1)
filtered_group.set_index('Nomor', inplace=True)

st.write(filtered_group)

#st.line_chart(filtered_df, x='OrderDate', y='TotalDue')
st.line_chart(filtered_group, x='OrderDate', y=['sum', 'count'])

st.bar_chart(filtered_group, x='OrderDate', y=['sum', 'count'])
#st.write(filtered_df[['TerritoryID', 'OrderDate', 'SalesOrderID']])