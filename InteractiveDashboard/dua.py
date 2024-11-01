import pandas as pd
import streamlit as st
from fpdf import FPDF
import base64

st.title("Sekolah Sabtu Auditor Data dari Internet")

export_as_pdf = st.button("Export Report")

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

if export_as_pdf:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Halo dunia')
    
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")

    st.markdown(html, unsafe_allow_html=True)

df = pd.read_csv('https://raw.githubusercontent.com/aansubarkah/ssa/refs/heads/main/MembukaPDF/SalesOrderHeaderMinimized.csv', sep='\t')

df_kolom = df[['RevisionNumber', 'SalesOrderID']]

st.write(df_kolom)

st.write(df)