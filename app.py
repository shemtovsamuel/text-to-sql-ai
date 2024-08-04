import streamlit as st
import requests
import json

# URL de l'API
API_URL = "https://europe-west2-ai-connection-alpha-crm.cloudfunctions.net/convert_question_to_sql"

# Fonction pour faire l'appel API
def call_api(request, is_list, organization_id):
    payload = {
        "request": request,
        "isList": is_list,
        "organization_id": organization_id
    }
    response = requests.post(API_URL, json=payload)
    return response.json()

# Titre de l'application
st.title("Convertisseur de Question en SQL")

# Input pour la question
question = st.text_input("Entrez votre question :")

# Input pour l'organization_id
organization_id = st.text_input("Entrez l'ID de l'organisation :")

# Checkbox pour isList
is_list = st.checkbox("Afficher sous forme de liste")

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

