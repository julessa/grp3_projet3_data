import streamlit as st
import time
from config import APP_NAME, APP_DESC, MODELS_CONFIG, DEFAULT_MODEL
from models import FakeNewsModel, predict_news

# Configuration Streamlit
st.set_page_config(page_title=APP_NAME, page_icon="🕵️‍♂️", layout="centered")

@st.cache_resource(show_spinner="Chargement du modèle sélectionné...")
def get_model(model_key: str):
    """Charge l'instance du modèle avec mise en cache."""
    model = FakeNewsModel(model_key)
    model.load()
    return model

def main():
    st.title(f"🕵️‍♂️ {APP_NAME}")
    st.markdown(f"*{APP_DESC}*")
    
    # Sidebar pour le choix du modèle
    with st.sidebar:
        st.header("🎛️ Configuration")
        model_list = list(MODELS_CONFIG.keys())
        selected_key = st.selectbox("Choisissez le modèle d'analyse :", model_list, index=0)
        
        conf = MODELS_CONFIG[selected_key]
        st.info(f"**Description :** {conf['desc']}")
        
        st.markdown("---")
        st.write("📊 **Métriques (Dataset LIAR)**")
        if "TF-IDF" in selected_key:
            st.write("- **Accuracy** : ~0.64")
            st.write("- **F1-Score** : ~0.63")
        else:
            st.write("- **Accuracy** : ~0.60")
            st.write("- **F1-Score** : ~0.60")

    # Chargement du modèle
    try:
        predictor = get_model(selected_key)
    except Exception as e:
        st.error(f"Erreur lors du chargement : {e}")
        st.stop()
        
    st.markdown("### 📝 Soumettez une déclaration")
    user_input = st.text_area(
        label="Saisissez le texte à analyser (déclaration politique, article, etc.) :", 
        height=200, 
        placeholder="Entrez votre texte ici..."
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        submit = st.button("Analyser", type="primary", use_container_width=True)
    
    if submit:
        if not user_input.strip():
            st.warning("Veuillez saisir du texte pour lancer l'analyse.")
        else:
            with st.spinner("Analyse en cours..."):
                label, proba_fake, proba_real = predict_news(user_input, predictor)
                
            confidence = max(proba_fake, proba_real)
            
            st.markdown("---")
            st.subheader("🏁 Résultat de l'Analyse")
            
            # Affichage visuel
            if label == "Fake News":
                st.error(f"### 🚨 {label}")
                st.write("Ce contenu présente des caractéristiques typiques de **désinformation**.")
            else:
                st.success(f"### ✅ {label}")
                st.write("Ce contenu semble être une **information factuelle**.")
            
            # Métriques de confiance
            m1, m2 = st.columns(2)
            m1.metric("Fiabilité estimée", f"{confidence * 100:.1f} %")
            m2.metric("Classe prédite", label)
            
            st.progress(confidence, text=f"Certitude : {confidence*100:.1f}%")
            
            # Message de contexte
            with st.expander("Détails techniques"):
                st.write(f"Modèle utilisé : `{selected_key}`")
                st.write(f"Probabilité Fake : `{proba_fake:.4f}`")
                st.write(f"Probabilité Real : `{proba_real:.4f}`")

if __name__ == "__main__":
    main()
