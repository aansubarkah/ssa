import pandas as pd
import streamlit as st

st.title('Interactive Dashboard Keduaku')

df = pd.read_csv('https://raw.githubusercontent.com/aansubarkah/ssa/refs/heads/main/MembukaPDF/SalesOrderHeaderMinimized.csv', sep='\t')

st.header('Data dari internet')

st.write(df)

st.header('Data dalam bentuk tabel')
st.table(df)