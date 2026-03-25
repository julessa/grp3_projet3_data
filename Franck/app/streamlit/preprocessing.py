import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Initialisation et téléchargement des ressources NLTK nécessaires
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')
    nltk.download('wordnet')

def preprocess_text(text: str) -> str:
    """
    Nettoie et prétraite le texte d'entrée. Exécute :
    1. Mise en minuscules
    2. Suppression de la ponctuation, URLs, chiffres
    3. Tokenisation
    4. Suppression des stopwords
    5. Lemmatisation
    """
    if not isinstance(text, str):
        return ""
        
    # 1. Minuscules
    text = text.lower()
    
    # 2. Nettoyage de base (URL, nombres, ponctuation)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # 3. Tokenisation
    try:
        tokens = word_tokenize(text)
    except Exception:
        # Fallback au cas où NLTK ne trouve pas punkt
        tokens = text.split()
    
    # 4 & 5. Stopwords et Lemmatisation
    lemmatizer = WordNetLemmatizer()
    try:
        stop_words = set(stopwords.words('english'))
    except Exception:
        stop_words = set()
        
    clean_tokens = [
        lemmatizer.lemmatize(word) 
        for word in tokens 
        if word not in stop_words
    ]
    
    return " ".join(clean_tokens)
