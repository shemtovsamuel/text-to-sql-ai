import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import pg8000
from urllib.parse import urlparse
import pandas as pd

load_dotenv()


API_URL = st.secrets["QUESTION_TO_SQL_API_URL"]
URL_DB = st.secrets["URL_DB"]
PASSWORD = st.secrets["PASSWORD"]

def call_api(request, is_list, organization_id):
    payload = {
        "request": request,
        "isList": is_list,
        "organization_id": organization_id
    }
    response = requests.post(API_URL, json=payload)
    return response.json()

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
    st.title("Convertisseur de Question en SQL")
    question = st.text_input("Entrez votre question :")
    organization_id = st.text_input("Entrez l'ID de l'organisation :")
    is_list = st.checkbox("Afficher sous forme de liste", value=True)

    if st.button("Convertir"):
        if question and organization_id:
            result = call_api(question, is_list, organization_id)

            st.subheader("Résultat :")
            st.json(result)

            url = urlparse(URL_DB)

            conn = pg8000.connect(
                host=url.hostname,
                database=url.path[1:],
                user=url.username,
                password=url.password,
                port=url.port
            )

            cursor = conn.cursor()
            cursor.execute(result["query"])
            results = cursor.fetchall()
            columns = [column[0] for column in cursor.description]

            st.subheader("Execution de la requête SQL :")
            df = pd.DataFrame(results, columns=columns)
            st.table(df)

            conn.close()
        else:
            st.warning("Veuillez entrer une question et un ID d'organisation.")