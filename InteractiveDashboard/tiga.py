import streamlit as st
import pandas as pd

st.title("Sekolah Sabtu Auditor Data dari Internet")

#df = pd.read_csv('https://raw.githubusercontent.com/aansubarkah/ssa/refs/heads/main/MembukaPDF/SalesOrderHeaderMinimized.csv', sep='\t')
#st.write(df)

btn_1 = st.button('Tombol untuk diklik')

if btn_1:
    st.write("Tombol ini sudah diklik")
    st.write("Klik tombol ini sekali lagi untuk melihat perubahan")
    #df = df.head(10)    
    #st.write(df)

btn_2 = st.button('Tombol untuk diklik 2')

select1 = st.sidebar.selectbox('Pilih angka', [1, 2, 3, 4, 5])

if select1 == 1:
    st.write("Anda memilih angka 1")
elif select1 == 2:
    st.write("Anda memilih angka 2")

date1 = st.sidebar.date_input('Pilih tanggal')

st.write(date1, format='DD-MM-YYYY')