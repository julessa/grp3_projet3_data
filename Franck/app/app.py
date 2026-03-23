
import streamlit as st
import json
from config import APP_NAME, APP_DESC, MODELS_CONFIG
from models import FakeNewsModel, predict_news


# Configuration Streamlit
st.set_page_config(page_title=APP_NAME, page_icon="🕵️‍♂️", layout="wide")

# Ajout d'un fond personnalisé via CSS




def set_bg():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;700;800&family=Inter:wght@400;600;700&display=swap');
        :root {
            --surface: #060e20;
            --surface-container-low: #091328;
            --surface-container: #0f1930;
            --surface-bright: #1f2b49;
            --surface-variant: #192540;
            --primary: #a3a6ff;
            --primary-dim: #6063ee;
            --secondary: #34b5fa;
            --tertiary: #a1ffef;
            --error: #ff6e84;
            --on-surface: #dee5ff;
            --on-surface-variant: #a3aac4;
            --outline-variant: #40485d;
            --gradient-main: linear-gradient(135deg, #a3a6ff 0%, #6063ee 100%);
        }
        html, body, .stApp {
            background: var(--surface) !important;
            color: var(--on-surface) !important;
            font-family: 'Inter', 'Manrope', Arial, sans-serif !important;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stSidebar {
            background: rgba(25, 37, 64, 0.6) !important;
            backdrop-filter: blur(20px) !important;
            border-radius: 1.5rem !important;
        }
        .stButton>button {
            background: var(--gradient-main);
            color: var(--on-surface);
            border-radius: 1.5rem;
            font-family: 'Manrope', 'Inter', Arial, sans-serif;
            font-weight: 700;
            border: none;
            box-shadow: 0 0 20px rgba(163,166,255,0.15);
            transition: 0.2s;
            font-size: 1rem;
            padding: 0.7rem 2.2rem;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #6063ee 0%, #a3a6ff 100%);
            color: var(--on-surface);
            transform: scale(1.04);
        }
        .stProgress>div>div>div>div {
            background-image: var(--gradient-main);
        }
        /* Glassmorphism for cards */
        .glass-card {
            background: rgba(25, 37, 64, 0.6);
            backdrop-filter: blur(20px);
            border-radius: 2rem;
            box-shadow: 0 24px 48px -12px rgba(6, 14, 32, 0.5);
        }
        /* Headline font */
        .headline {
            font-family: 'Manrope', Arial, sans-serif;
            font-weight: 800;
            letter-spacing: -0.03em;
        }
        /* Label font */
        .label-sm {
            font-family: 'Inter', Arial, sans-serif;
            font-size: 0.75rem;
            color: var(--on-surface-variant);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        /* No hard borders, only ghost borders for inputs */
        .ghost-border {
            outline: 1.5px solid rgba(64,72,93,0.15);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


set_bg()

@st.cache_resource(show_spinner="Chargement du modèle sélectionné...")
def get_model(model_key: str):
    """Charge l'instance du modèle avec mise en cache."""
    model = FakeNewsModel(model_key)
    model.load()
    return model

def main():
    # En-tête avec icône et description
    st.markdown(
        """
        <div style='display: flex; align-items: center; gap: 1rem;'>
            <span style='font-size:2.5rem;'>🕵️‍♂️</span>
            <span style='font-size:2.2rem; font-weight:700;'>{}</span>
        </div>
        <div style='margin-top:0.5rem; color:#555; font-size:1.1rem;'>
            {}
        </div>
        """.format(APP_NAME, APP_DESC),
        unsafe_allow_html=True
    )

    # Sidebar modernisée

    with st.sidebar:
        st.markdown(
            """
            <div style='text-align:center;'>
                <span style='font-size:2rem;'>⚙️</span>
                <h2 style='margin-bottom:0.2em;'>Configuration</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        model_list = list(MODELS_CONFIG.keys())
        selected_key = st.selectbox(
            "<b>Choisissez le modèle d'analyse :</b>",
            model_list,
            index=0,
            format_func=lambda x: f"🧠 {x}",
            help="Sélectionnez le modèle de détection de fake news à utiliser."
        )
        conf = MODELS_CONFIG[selected_key]
        st.info(f"**Description :** {conf['desc']}")
        st.markdown("---")
        st.write("📊 <b>Métriques (Dataset LIAR)</b>", unsafe_allow_html=True)

        # Mapping modèle -> clé métrique
        metrics_map = {
            "TF-IDF + LogReg (SMOTE)": "LogisticRegression",
            "TF-IDF + LinearSVC (SMOTE)": "LinearSVC",
            "GloVe + LogReg (300d)": "LogisticRegression"  # fallback, à adapter si métriques spécifiques
        }
        metrics_key = metrics_map.get(selected_key)
        metrics = None
        try:
            with open("data/modeles/baselines_metrics_test.json", "r", encoding="utf-8") as f:
                all_metrics = json.load(f)
                if metrics_key in all_metrics:
                    metrics = all_metrics[metrics_key]
        except Exception:
            metrics = None

        if metrics:
            st.write(f"- <b>Accuracy</b> : {metrics['accuracy']:.2f}", unsafe_allow_html=True)
            st.write(f"- <b>F1-Score</b> : {metrics['macro_f1']:.2f}", unsafe_allow_html=True)
        else:
            st.write("- <b>Métriques non disponibles pour ce modèle.</b>", unsafe_allow_html=True)

        st.markdown(
            """
            <hr style='margin:1em 0;'>
            <div style='font-size:0.95em; color:#888;'>
                <b>Astuce :</b> Essayez différents modèles pour comparer les résultats !
            </div>
            """,
            unsafe_allow_html=True
        )

    # Chargement du modèle
    try:
        predictor = get_model(selected_key)
    except Exception as e:
        st.error(f"Erreur lors du chargement : {e}")
        st.stop()

    st.markdown(
        """
        <div style='margin-top:2em; margin-bottom:0.5em;'>
            <span style='font-size:1.3rem;'>📝 Soumettez une déclaration</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    user_input = st.text_area(
        label=(
            "Saisissez le texte à analyser "
            "(déclaration politique, article, etc.) :"
        ),
        height=180,
        placeholder="Entrez votre texte ici...",
        help="Collez ici la déclaration, l'article ou le texte à vérifier."
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        submit = st.button(
            "Analyser",
            type="primary",
            use_container_width=True,
            help="Lancer l'analyse du texte saisi."
        )

    if submit:
        if not user_input.strip():
            st.warning("⚠️ Veuillez saisir du texte pour lancer l'analyse.")
        else:
            with st.spinner("Analyse en cours... "):
                label, proba_fake, proba_real = predict_news(user_input, predictor)

            confidence = max(proba_fake, proba_real)

            st.markdown("---")
            st.markdown(
                """
                <div style='display:flex; align-items:center; gap:1rem;'>
                    <span style='font-size:1.7rem;'>🏁</span>
                    <span style='font-size:1.3rem; font-weight:600;'>Résultat de l'Analyse</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Affichage visuel modernisé
            if label == "Fake News":
                st.error(
                    f"🚨 <b>{label}</b>", icon="🚨"
                )
                st.markdown(
                    "<span style='color:#c0392b; font-size:1.1rem;>"
                    "Ce contenu présente des caractéristiques typiques de "
                    "<b>désinformation</b>."
                    "</span>",
                    unsafe_allow_html=True
                )
            else:
                st.success(
                    f"✅ <b>{label}</b>", icon="✅"
                )
                st.markdown(
                    "<span style='color:#27ae60; font-size:1.1rem;>"
                    "Ce contenu semble être une <b>information factuelle</b>."
                    "</span>",
                    unsafe_allow_html=True
                )

            # Métriques de confiance
            m1, m2 = st.columns(2)
            m1.metric(
                "Fiabilité estimée",
                f"{confidence * 100:.1f} %",
                help="Plus ce score est élevé, plus le modèle est confiant dans sa prédiction."
            )
            m2.metric(
                "Classe prédite",
                label,
                help="Catégorie attribuée par le modèle."
            )

            st.progress(confidence, text=f"Certitude : {confidence*100:.1f}%")

            # Message de contexte
            with st.expander("🛠️ Détails techniques"):
                st.write(f"Modèle utilisé : `{selected_key}`")
                st.write(f"Probabilité Fake : `{proba_fake:.4f}`")
                st.write(f"Probabilité Real : `{proba_real:.4f}`")


if __name__ == "__main__":
    main()
