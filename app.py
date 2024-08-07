import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

# URL de l'API
API_URL = "https://europe-west2-ai-connection-alpha-crm.cloudfunctions.net/convert_question_to_sql"

# Fonction pour obtenir le mot de passe
def get_password():
    try:
        # Essayer d'obtenir le mot de passe depuis les secrets Streamlit
        return st.secrets["PASSWORD"]
    except FileNotFoundError:
        # Si le fichier secrets.toml n'est pas trouvé, utiliser une variable d'environnement
        return os.environ.get("PASSWORD")

# Obtenir le mot de passe
try:
    PASSWORD = get_password()
except:
    st.error("Erreur: Le mot de passe n'a pas pu être récupéré. Assurez-vous d'avoir configuré correctement vos secrets ou variables d'environnement.")
    st.stop()

# Le reste du code reste inchangé...

# Fonction pour faire l'appel API
def call_api(request, is_list, organization_id):
    payload = {
        "request": request,
        "isList": is_list,
        "organization_id": organization_id
    }
    response = requests.post(API_URL, json=payload)
    return response.json()

# Fonction pour vérifier le mot de passe
def check_password():
    def password_entered():
        if st.session_state["password"] == PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Entrez le mot de passe", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Entrez le mot de passe", type="password", on_change=password_entered, key="password")
        st.error("Mot de passe incorrect")
        return False
    else:
        return True

if check_password():
    # Titre de l'application
    st.title("Convertisseur de Question en SQL")

    # Input pour la question
    question = st.text_input("Entrez votre question :")

    # Input pour l'organization_id
    organization_id = st.text_input("Entrez l'ID de l'organisation :")

    # Checkbox pour isList, par défaut à True
    is_list = st.checkbox("Afficher sous forme de liste", value=True)

    # Bouton pour lancer la requête
    if st.button("Convertir"):
        if question and organization_id:
            # Appel de l'API
            result = call_api(question, is_list, organization_id)

            # Affichage du résultat
            st.subheader("Résultat :")
            st.json(result)
        else:
            st.warning("Veuillez entrer une question et un ID d'organisation.")