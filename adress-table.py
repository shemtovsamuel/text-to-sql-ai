import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY')
MODEL = "gpt-4o"

model = ChatOpenAI(openai_api_key=OPENAI_KEY, model=MODEL, temperature=0.5)

prompt = ChatPromptTemplate.from_template("""
Act as an SQL and plotly expert.
I need you to translate this request into SQL for a PostgreSQL database.
Don't assume any additional information on the structure of the db.
If the request is impossible to satisfy, write a clear error message for the user.
If the request is not precise enough, ask me a refinement question and I will give you details.
I am not a developer and I don't know anything about SQL or the structure of the database.
If I don't ask you to select specific columns of a table select them all.
The database is PostgreSQL.
Here is the description of the relevant table:

Table name: address
Columns:
- id (uuid): Unique identifier of the address, primary key
- created_at (timestamptz): Date and time when the record was created
- city (varchar): Name of the city
- street (varchar): Street name
- number (varchar): Street number
- lat (float8): Latitude of the address
- lng (float8): Longitude of the address
- zip_code (varchar): Postal code
- address_line (varchar): Full address line
- type (varchar): Type of address (e.g., residential, business)
- client_id (uuid): Identifier of the client associated with this address

Table name: client
Columns:
- client_id (uuid): Unique identifier of the client, primary key, default value gen_random_uuid()
- civility (varchar): Civility, default value 'M'
- first_name (varchar): First name, default value NULL
- last_name (varchar): Last name, default value NULL
- tel (varchar): Telephone number, default value NULL
- email (varchar): Email address, default value NULL
- statut_id (int4): Status ID, default value 15
- processed_by_ (uuid): Processed by user ID, default value NULL
- created_by (uuid): Created by user ID, default value NULL
- created_at (timestamptz): Date and time when the record was created, default value now()
- updated_at (timestamptz): Date and time when the record was last updated, default value now()
- deleted_at (timestamptz): Date and time when the record was deleted, default value NULL
- updated_by (uuid): Updated by user ID, default value NULL
- id_address_fac (uuid): Address ID for facility, default value NULL
- id_address_ins (uuid): Address ID for installation, default value NULL
- supplier_id (uuid): Supplier ID, default value NULL
- source (text): Source of the information, default value NULL
- assigned_at (timestamptz): Date and time when the client was assigned, default value NULL
- dynamic_fields (jsonb): Dynamic fields, default value '[]'::jsonb
- source_id (int8): Source ID, default value NULL
- organization_id (int8): Organization ID, default value 2

Generate the SQL query that matches this request: "{request}"
The goal is to be able to execute SQL scripts to interact with the database.
Do not include any explanations, only provide a RFC8259 compliant JSON response following one of these 2 formats without deviation.
{{"query": <insert query>, "columns": [<list of columns names returned>]}}
OR
{{"error": <insert error>}}
""")

output_parser = StrOutputParser()

chain = prompt | model | output_parser

result = chain.invoke({"request": "combien il y a de clients dans la base de données ?"})
print(result)