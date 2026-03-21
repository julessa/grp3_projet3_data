import streamlit as st
import time
from config import APP_NAME, APP_DESC, MODEL_PATH
from models import FakeNewsModel, predict_news

# Configuration Streamlit
st.set_page_config(page_title=APP_NAME, page_icon="🕵️‍♂️", layout="centered")

@st.cache_resource(show_spinner="Chargement initial du modèle NLP...")
def load_trained_model():
    """Charge l'instance du modèle une seule fois grâce au cache."""
    model = FakeNewsModel(MODEL_PATH)
    model.load()
    return model

def main():
    st.title(f"🕵️‍♂️ {APP_NAME}")
    st.write(APP_DESC)
    
    # Optionnel: Selectbox des modèles dans la sidebar
    with st.sidebar:
        st.header("Paramètres")
        modele_choisi = st.selectbox("Sélection des modèles prêts :", ["Baseline (LogReg)", "LSTM", "BERT"])
        st.markdown("---")
        if modele_choisi == "Baseline (LogReg)":
            st.write("📊 **Performances Globales**")
            st.write("- **Accuracy** : ~61 %")
            st.write("- **F1-Score** : ~59 %")
            st.info("C'est le modèle TF-IDF entraîné sur le jeu LIAR par défaut.")
        else:
            st.warning("⚠️ Les modèles avancés (LSTM / BERT) nécessiteraient d'être entraînés et interfacés dans models.py.")

    # Tentative d'instanciation
    try:
        predictor = load_trained_model()
    except Exception as e:
        st.error(str(e))
        st.stop()
        
    st.markdown("### Soumettez une déclaration")
    user_input = st.text_area(
        label="Collez un paragraphe complet ou un article pour fournir un contexte approprié :", 
        height=200, 
        placeholder="Un haut représentant de la banque mondiale affirme que..."
    )
    
    if st.button("Analyze News", type="primary"):
        if not user_input.strip():
            st.error("Veuillez saisir du texte avant de lancer l'inférence.")
        else:
            with st.spinner("Prétraitement & Inférence..."):
                time.sleep(0.2) # Esthétique "temps réel"
                # Appel de la fonction définie dans la spec
                label, proba_fake, proba_real = predict_news(user_input, predictor)
                
            confidence = max(proba_fake, proba_real)
            
            st.markdown("---")
            st.markdown("### Résultat de l'analyse")
            
            if label == "Fake News":
                st.error(f"🚨 **{label}**")
                st.write("Ce texte est très probablement trompeur selon le modèle entraîné.")
                st.metric(label="Score de Confiance", value=f"{confidence * 100:.1f} %")
                st.progress(confidence)
            else:
                st.success(f"✅ **{label}**")
                st.write("Ce texte est vraisemblablement authentique / factuel.")
                st.metric(label="Score de Confiance", value=f"{confidence * 100:.1f} %")
                st.progress(confidence)

if __name__ == "__main__":
    main()
