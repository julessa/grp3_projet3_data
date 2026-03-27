import json
import os

NOTEBOOK_DIR = r"C:\Users\Franck\Documents\grp3_projet3_data\Franck\notebook"

load_data_code = [
    "columns = ['id', 'label', 'statement', 'subject', 'speaker', 'job_title', 'state_info', 'party', \n",
    "           'barely_true_counts', 'false_counts', 'half_true_counts', 'mostly_true_counts', \n",
    "           'pants_on_fire_counts', 'context']\n",
    "df_train = pd.read_csv('../data/brutes/liar_dataset/train.tsv', sep='\\t', names=columns).fillna('')\n",
    "df_val = pd.read_csv('../data/brutes/liar_dataset/valid.tsv', sep='\\t', names=columns).fillna('')\n",
    "df_test = pd.read_csv('../data/brutes/liar_dataset/test.tsv', sep='\\t', names=columns).fillna('')\n",
    "\n",
    "label_map = {'pants-fire': 0, 'false': 1, 'mostly-false': 2, 'half-true': 3, 'mostly-true': 4, 'true': 5}\n",
    "df_train['label'] = df_train['label'].map(label_map).fillna(-1).astype(int)\n",
    "df_val['label'] = df_val['label'].map(label_map).fillna(-1).astype(int)\n",
    "df_test['label'] = df_test['label'].map(label_map).fillna(-1).astype(int)\n"
]

def update_nb(filename, advanced=False):
    path = os.path.join(NOTEBOOK_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            if "load_dataset('liar')" in source:
                new_source = [
                    "import pandas as pd\n",
                    "import plotly.express as px\n",
                ] if not advanced else [
                    "import pandas as pd\n",
                    "import torch\n",
                    "import numpy as np\n",
                    "from datasets import Dataset, DatasetDict\n",
                    "from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments\n",
                    "from sklearn.metrics import accuracy_score, f1_score\n"
                ]
                
                new_source.extend(["\n# 1. Chargement des données locales depuis les TSV\n"])
                new_source.extend(load_data_code)
                
                if not advanced:
                    if filename == "Modeles_de_Base.ipynb":
                        new_source = [
                            "import pandas as pd\n",
                            "import plotly.express as px\n",
                            "from sklearn.feature_extraction.text import TfidfVectorizer\n",
                            "from sklearn.linear_model import LogisticRegression\n",
                            "from sklearn.svm import LinearSVC\n",
                            "from sklearn.metrics import classification_report, accuracy_score, confusion_matrix\n",
                            "import plotly.figure_factory as ff\n",
                            "\n# 1. Chargement des données locales depuis les TSV\n"
                        ] + load_data_code + [
                            "\nX_train, y_train = df_train['statement'], df_train['label']\n",
                            "X_val, y_val = df_val['statement'], df_val['label']\n",
                            "X_test, y_test = df_test['statement'], df_test['label']\n",
                            "\nprint(\"Données LIAR chargées localement.\")\n"
                        ]
                    elif filename == "EDA_LIAR.ipynb":
                        new_source = new_source + [
                            "\nprint(\"Train size:\", len(df_train))\n",
                            "print(\"Validation size:\", len(df_val))\n",
                            "print(\"Test size:\", len(df_test))\n",
                            "\ndisplay(df_train.head())\n"
                        ]
                    elif filename == "Interpretabilite_Biais.ipynb":
                         new_source = [
                            "import pandas as pd\n",
                            "import numpy as np\n",
                            "from sklearn.feature_extraction.text import TfidfVectorizer\n",
                            "from sklearn.linear_model import LogisticRegression\n",
                            "from sklearn.metrics import accuracy_score\n",
                            "import plotly.express as px\n",
                            "import lime.lime_text\n",
                            "\n# 1. Chargement des données locales depuis les TSV\n"
                        ] + load_data_code + [
                             "\ntfidf = TfidfVectorizer(stop_words='english', max_features=5000)\n",
                             "X_train_tfidf = tfidf.fit_transform(df_train['statement'])\n",
                             "\nlr_model = LogisticRegression(class_weight='balanced', max_iter=1000)\n",
                             "lr_model.fit(X_train_tfidf, df_train['label'])\n"
                        ]
                else:
                    new_source.extend([
                        "\n# Transformation en format HuggingFace Dataset\n",
                        "dataset = DatasetDict({\n",
                        "    'train': Dataset.from_pandas(df_train),\n",
                        "    'validation': Dataset.from_pandas(df_val),\n",
                        "    'test': Dataset.from_pandas(df_test)\n",
                        "})\n",
                        "\nprint(\"Données LIAR transformées en Dataset HF.\")\n"
                    ])

                cell['source'] = new_source
                break 

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

for nb in ["EDA_LIAR.ipynb", "Modeles_de_Base.ipynb", "Interpretabilite_Biais.ipynb"]:
    update_nb(nb, advanced=False)
update_nb("Modeles_Avances.ipynb", advanced=True)

print("Notebooks updated successfully!")
