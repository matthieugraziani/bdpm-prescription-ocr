import streamlit as st
from api.bdpm_client import search_medicine
from matcher.fuzzy_match import normalize

st.set_page_config(page_title="BDPM Prescription OCR",layout="wide")
st.title("💊 BDPM Prescription OCR")

text=st.text_area("Texte OCR ou ordonnance")
if st.button("Analyser"):
    for line in text.splitlines():
        if line.strip():
            q=normalize(line)
            st.write(search_medicine(q))
