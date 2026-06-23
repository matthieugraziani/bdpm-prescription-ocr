import streamlit as st


def render_result_row(result):

    with st.container(border=True):
        st.markdown(f"**Ligne OCR :** {result['ligne_ocr']}")

        if result["matched"]:
            st.markdown(
                f"**Médicament reconnu :** {result['medicament']} "
                f"_(score {result['score_matching']}%)_"
            )
        else:
            st.warning(
                f"Aucun médicament reconnu avec une confiance suffisante "
                f"(score {result['score_matching']}%)."
            )

        if result.get("erreur"):
            st.error(f"Erreur API BDPM : {result['erreur']}")
        elif result.get("resultat_bdpm") is not None:
            st.json(result["resultat_bdpm"])


def render_api_status(is_up):

    if is_up:
        st.sidebar.success("API BDPM : en ligne")
    else:
        st.sidebar.error("API BDPM : hors ligne")