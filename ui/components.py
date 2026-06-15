import streamlit as st


def render_result_row(result):
    """
    Affiche le résultat d'analyse d'une ligne d'ordonnance.

    Args:
        result: dict tel que renvoyé par
            `services.analyzer.analyze_lines`, avec les clés
            "ligne_ocr", "medicament", "score_matching", "matched",
            "resultat_bdpm", "erreur".
    """
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
    """
    Affiche un indicateur de statut de l'API BDPM dans la barre latérale.

    Args:
        is_up: booléen indiquant si l'API répond, généralement obtenu via
            `api.bdpm_client.check_api_status()`.
    """
    if is_up:
        st.sidebar.success("API BDPM : en ligne")
    else:
        st.sidebar.error("API BDPM : hors ligne")