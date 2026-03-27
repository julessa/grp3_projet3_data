import streamlit as st
import json
from config import APP_NAME, APP_DESC, MODELS_CONFIG
from models import FakeNewsModel, predict_news

def set_bg():
    st.set_page_config(page_title=APP_NAME, page_icon="🕵️‍♂️", layout="wide")
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
        }
        </style>
        """,
        unsafe_allow_html=True
    )

@st.cache_resource(show_spinner="Chargement du modèle sélectionné...")
def get_model(model_key: str):
    model = FakeNewsModel(model_key)
    model.load()
    return model

def main():
    set_bg()

    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("""
        <div style='font-size:1.5rem; font-weight:800; color:#dee5ff; font-family:Manrope,Arial,sans-serif; letter-spacing:-0.03em; margin-bottom:2.5rem;'>The Sentinel</div>
        <div style='margin-bottom:2rem;'>
            <div style='display:flex; align-items:center; gap:1rem;'>
                <div style='width:44px; height:44px; border-radius:1.5rem; background:#0f1930; display:flex; align-items:center; justify-content:center; overflow:hidden;'>
                    <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuBVYcJrIlFF_tFC1YDajd7Ou-9j1G48hACVOS0xSprqjAHvcmHrIr8BOV1AGhGvy3Ka8g_2KCum9fBrir89dFaoD61njWnFoNUn73mSVkP6meg169ewL-fUtAEyGJ56gNQnyj9ZyOHNQxFwwMIE_8Hbyq-rw2mIHiEu6Jqc7ypqA1Kxp2IJAv0OeDsoSgXiwOuKQS4G3BqbIKP7e-ubIyRnB8Syb695j1SRB2WqYZOY-3fsUyuX9gK3LwUVfuXnkmkjGclZLj69b2g" width="36" height="36"/>
                </div>
                <div>
                    <div class='label-sm' style='color:#a3a6ff;'>Forensic Lab</div>
                    <div class='label-sm' style='color:#a3aac4;'>AI Engine Active</div>
                </div>
            </div>
            <button style='width:100%; margin-top:1.5rem; background:linear-gradient(90deg,#a3a6ff,#6063ee); color:#0f00a4; padding:0.9rem 0; border-radius:1.5rem; font-weight:700; font-size:0.9rem; text-transform:uppercase; letter-spacing:0.08em; box-shadow:0 0 20px rgba(163,166,255,0.15); border:none;'>Nouvelle Analyse</button>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<hr style='border:1px solid rgba(64,72,93,0.10); margin:1.5rem 0;' />", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#a3aac4; font-size:0.95rem; margin-bottom:1.5rem;'>{APP_DESC}</div>", unsafe_allow_html=True)
        st.markdown("<div style='color:#a3aac4; font-size:0.85rem; margin-bottom:0.5rem;'>Sélection du modèle</div>", unsafe_allow_html=True)
        model_key = st.selectbox("Modèle IA", list(MODELS_CONFIG.keys()), index=0)
        # Affichage dynamique des métriques (exemple simplifié)
        try:
            with open("../data/modeles/baselines_metrics_test.json", "r") as f:
                metrics = json.load(f)
        except Exception:
            metrics = {}
        st.markdown("<div style='color:#a3aac4; font-size:0.85rem; margin-top:1.5rem;'>Métriques du modèle :</div>", unsafe_allow_html=True)
        if model_key and metrics:
            # Mapping simple pour la démo
            if "LogReg" in model_key:
                met = metrics.get("LogisticRegression", {})
            elif "LinearSVC" in model_key:
                met = metrics.get("LinearSVC", {})
            else:
                met = {}
            st.markdown(f"<div style='color:#dee5ff; font-size:1.1rem;'>Accuracy : <b>{met.get('accuracy', 'N/A'):.2%}</b></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='color:#dee5ff; font-size:1.1rem;'>Macro F1 : <b>{met.get('macro_f1', 'N/A'):.2%}</b></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#dee5ff; font-size:1.1rem;'>Aucune métrique disponible</div>", unsafe_allow_html=True)

    # --- MAIN CONTENT ---
    st.markdown("""
    <header style='background:rgba(6,14,32,0.60); backdrop-filter:blur(16px); position:sticky; top:0; z-index:50; box-shadow:0 24px 48px -12px rgba(6,14,32,0.5); display:flex; justify-content:space-between; align-items:center; width:100%; padding:2rem 3rem 1.5rem 3rem;'>
        <div style='display:flex; align-items:center; gap:2.5rem;'>
            <h1 class='headline' style='font-size:1.5rem; color:#dee5ff;'>The Sentinel</h1>
            <nav style='display:flex; align-items:center; gap:2rem;'>
                <a href='#' style='color:#a3a6ff; font-weight:700; border-bottom:2px solid #a3a6ff; font-family:Manrope,sans-serif; font-size:1rem; padding-bottom:0.2rem;'>Dashboard</a>
                <a href='#' style='color:#a3aac4; font-family:Manrope,sans-serif; font-size:1rem; padding:0.2rem 0.8rem; border-radius:0.5rem;'>Investigations</a>
                <a href='#' style='color:#a3aac4; font-family:Manrope,sans-serif; font-size:1rem; padding:0.2rem 0.8rem; border-radius:0.5rem;'>Global Feed</a>
            </nav>
        </div>
        <div style='display:flex; align-items:center; gap:1.5rem;'>
            <div style='position:relative;'>
                <input type='text' placeholder='Recherche globale...' style='background:#000; border:none; border-radius:2rem; padding:0.7rem 2.5rem 0.7rem 2.5rem; color:#dee5ff; font-size:0.95rem; width:220px; outline:none;'/>
                <span style='position:absolute; left:0.9rem; top:50%; transform:translateY(-50%); color:#a3aac4; font-size:1.2rem;'>🔍</span>
            </div>
            <button style='color:#a3aac4; background:none; border:none; border-radius:50%; padding:0.7rem; font-size:1.3rem;'>🔔</button>
            <div style='width:36px; height:36px; border-radius:50%; overflow:hidden; border:1.5px solid #40485d33;'>
                <img src='https://lh3.googleusercontent.com/aida-public/AB6AXuDfK6XSl_Ib2RuOZ6FBfID0JXFmOxdnU5HbBSPUPqOgPk_tGBgxY1GpN7ve3OOGYCK6FsDhfoDRqUO4hy2jsahrTFwSE7izZCzTs7bDyRAAuQhOOGxoAIs2mouzs9rTZN5yMKQHfcMaqBNF-BF5EktCWfW2e1OeqHAZ94SvL39lTXUc8bTKuJjOgiVdAvZeRwxzzRAl7KvqP5iwuhpDqPxmuRN7KJXrXKAqtEPM_GVkay9z9C0Mdd6ziqxgWZkMrMfxsU2qTHdQl4k' width='36' height='36'/>
            </div>
        </div>
    </header>
    """, unsafe_allow_html=True)

    st.markdown("""
    <section style='padding:3rem 0 0 0; max-width:1100px; margin:0 auto;'>
        <div style='margin-bottom:2.5rem;'>
            <h2 class='headline' style='font-size:2.7rem; color:#dee5ff; margin-bottom:0.5rem;'>Initialiser une analyse</h2>
            <p style='color:#a3aac4; font-size:1.15rem;'>Collez un texte ou une URL pour lancer la vérification forensique.</p>
        </div>
    </section>
    """, unsafe_allow_html=True)

    # --- INPUT SECTION ---
    col1, col2 = st.columns([5, 1])
    with col1:
        user_text = st.text_area("Texte ou URL à analyser", "", height=120, key="input_text")
    with col2:
        st.write("")
        st.write("")
        analyze_btn = st.button("Analyser", use_container_width=True)

    # --- ANALYSE ---
    result = None
    if analyze_btn and user_text.strip():
        with st.spinner("Analyse en cours..."):
            model = get_model(model_key)
            label, proba_fake, proba_real = predict_news(user_text, model)
            result = {
                "label": label,
                "proba_fake": proba_fake,
                "proba_real": proba_real,
                "text": user_text
            }

    # --- RESULT SECTION ---
    if result:
        cred = int(result["proba_real"] * 100)
        st.markdown(f"""
        <section style='padding:3rem 0 0 0; max-width:1100px; margin:0 auto;'>
            <div class='glass-card' style='margin-top:2.5rem; padding:2.5rem 2rem; border-radius:2rem;'>
                <div style='display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:2.5rem;'>
                    <div>
                        <span class='label-sm' style='background:rgba(52,181,250,0.10); color:#34b5fa; padding:0.3rem 1rem; border-radius:1rem; margin-bottom:1rem; display:inline-block;'>Analyse terminée</span>
                        <h3 class='headline' style='font-size:2rem; margin:0;'>{result['text'][:60]}{'...' if len(result['text'])>60 else ''}</h3>
                        <p style='color:#a3aac4; font-size:0.95rem; margin-top:0.5rem;'>
                            <span style='font-size:1.1em;'></span> • <span style='font-size:1.1em;'></span>
                        </p>
                    </div>
                    <div style='display:flex; flex-direction:column; align-items:end;'>
                        <div class='headline' style='font-size:3.5rem; color:#a1ffef;'>{cred}<span style='font-size:1.5rem; color:#a3aac4;'>/100</span></div>
                        <div class='label-sm' style='color:#a1ffef; margin-top:0.5rem;'>{'Crédibilité élevée' if cred>70 else 'Crédibilité faible'}</div>
                    </div>
                </div>
                <div style='height:1.2rem; width:100%; background:var(--surface-container-highest,#192540); border-radius:1rem; margin-bottom:2.5rem; overflow:hidden; display:flex;'>
                    <div style='height:100%; width:{cred}%; background:linear-gradient(90deg,#ff6e84,#34b5fa,#a1ffef); border-radius:1rem; box-shadow:0 0 15px rgba(161,255,239,0.4);'></div>
                </div>
                <div style='display:grid; grid-template-columns:repeat(2,1fr); gap:2rem;'>
                    <div style='background:var(--surface-container-low,#091328); padding:1.5rem; border-radius:1.2rem; border-left:4px solid #a1ffef;'>
                        <div class='label-sm' style='margin-bottom:0.5rem;'>Label</div>
                        <div style='font-size:1.3rem; font-weight:700;'>{result['label']}</div>
                        <div style='color:#a3aac4; font-size:0.9rem; margin-top:0.3rem;'>Probabilité Fake : {result['proba_fake']:.2%}</div>
                        <div style='color:#a3aac4; font-size:0.9rem; margin-top:0.3rem;'>Probabilité Real : {result['proba_real']:.2%}</div>
                    </div>
                </div>
            </div>
        </section>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
