import streamlit as st

st.title('Membuat Sidebar')
st.button('Tombol pada halaman')

st.sidebar.write('Ini adalah sidebar')
st.sidebar.button('Tombol dalam sidebar')

btn1 = st.sidebar.button('Tombol untuk diklik')
if btn1:
    st.write('Tombol diklik')

select1 = st.sidebar.selectbox('Pilih opsi', ['A', 'B', 'C'])
if select1 == 'A':
    st.write('Anda memilih opsi A')

multiselect1 = st.sidebar.multiselect('Pilih beberapa opsi', ['D', 'E', 'F', 'G', 'H'])

date1 = st.sidebar.date_input('Pilih tanggal')

date2 = st.sidebar.date_input('Pilih tanggal dengan format', format='DD-MM-YYYY')