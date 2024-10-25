import pandas as pd
import streamlit as st
import json

st.title('Interactive Dashboard Keduaku, data offline')

df = pd.read_csv('SalesOrderHeaderMinimized.csv', sep='\t')

st.header('Data dari CSV')

st.write(df)

st.header('Data dalam bentuk tabel')
st.table(df.iloc[:10])

with open('page_30.json', 'r') as f:
    json_data = json.load(f)
    st.json(json_data)