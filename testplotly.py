import json
import pandas as pd
import plotly.express as px
from supabase import create_client, Client
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Connexion à Supabase (à remplacer par vos propres informations)
url: str = os.getenv('SUPABASE_URL')
key: str = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)

# Votre input
input_data = json.loads('''{
  "query": "SELECT users_meta_data.first_name FROM users_meta_data INNER JOIN teams ON users_meta_data.team_id = teams.id WHERE teams.name = 'Commerciaux'",
  "plot_type": "bar",
  "x_legend": "Users",
  "y_legend": "Count",
  "plot_title": "Number of Users in Commerciaux Team"
}''')

# Exécution de la requête SQL
result = supabase.table("users_meta_data").select("first_name").execute()

# Conversion des résultats en DataFrame pandas
df = pd.DataFrame(result.data)

# Comptage des occurrences de chaque prénom
df_count = df['first_name'].value_counts().reset_index()
df_count.columns = ['first_name', 'count']

# Création du graphique en barre avec Plotly
fig = px.bar(df_count, x='first_name', y='count', 
             title=input_data['plot_title'],
             labels={'first_name': input_data['x_legend'], 'count': input_data['y_legend']})

# Affichage du graphique
fig.show()