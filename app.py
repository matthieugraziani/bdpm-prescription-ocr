import easyocr
import numpy as np
import streamlit as st
from PIL import Image

from api.bdpm_client import check_api_status
from ocr.extractor import extract
from services.analyzer import analyze_lines, to_dataframe
from ui.components import render_api_status, render_result_row

@st.cache_resource
def get_reader(lang_list=None, gpu=False):
    return easyocr.Reader(lang_list or ["fr"], gpu=gpu)

st.set_page_config(page_title="BDPM Prescription OCR", layout="wide")
st.title("💊 BDPM Prescription OCR")

render_api_status(check_api_status())

st.markdown(
    "Importez une photo ou un PDF d'ordonnance, ou collez directement le "
    "texte, pour identifier les médicaments via la base BDPM."
)

uploaded_file = st.file_uploader(
    "Image ou PDF d'ordonnance", type=["png", "jpg", "jpeg", "pdf"]
)

manual_text = st.text_area("...ou collez le texte de l'ordonnance")

threshold = st.slider(
    "Seuil de confiance du fuzzy matching (%)", min_value=50, max_value=100, value=80
)


def load_images_from_upload(uploaded):
    """
    Convertit un fichier importé (image ou PDF) en liste d'images numpy RGB,
    une par page pour un PDF, ou une seule image pour un fichier image.
    """
    images = []

    if uploaded.type == "application/pdf":
        import fitz  # PyMuPDF

        pdf_document = fitz.open(stream=uploaded.read(), filetype="pdf")
        for page in pdf_document:
            pixmap = page.get_pixmap(dpi=200)
            page_image = Image.frombytes(
                "RGB", (pixmap.width, pixmap.height), pixmap.samples
            )
            images.append(np.array(page_image))
    else:
        images.append(np.array(Image.open(uploaded).convert("RGB")))

    return images


if st.button("Analyser"):
    lines = []

    if uploaded_file is not None:
        st.info(f"Fichier reçu : {uploaded_file.name}")

        with st.spinner("Extraction du texte (OCR) en cours..."):
            for i, page_image in enumerate(load_images_from_upload(uploaded_file), start=1):
                st.write(f"Traitement page {i}")

                text = extract(page_image)

                print("OCR RESULT:", text[:500])
                st.write(f"OCR page {i} terminée")

                lines.extend(text.splitlines())

    if manual_text:
        lines.extend(manual_text.splitlines())

    if not lines:
        st.warning("Importez un fichier ou saisissez du texte avant d'analyser.")
    else:
        with st.spinner("Recherche dans la base BDPM..."):
            results = analyze_lines(lines, threshold=threshold)

        for result in results:
            render_result_row(result)

        results_df = to_dataframe(results)
        st.dataframe(results_df, width="stretch")

        csv_bytes = results_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Télécharger les résultats (CSV)",
            data=csv_bytes,
            file_name="resultats_ordonnance.csv",
            mime="text/csv",
        )