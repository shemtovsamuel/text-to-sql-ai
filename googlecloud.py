import os
import functions_framework
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY')
MODEL = "gpt-4"
DESCRIPTION_TABLES = """
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

Table name: client_invoices
Columns:
- id (int8): Unique identifier of the invoice, primary key
- client_id (uuid): Identifier of the client associated with this invoice
- facturation_ad (text): Billing address, default value NULL
- selected_products (json): Selected products, default value NULL
- selected_annexes (json): Selected years, default value NULL
- created_at (timestamptz): Date and time when the record was created, default value now()
- updated_at (timetz): Date and time when the record was last updated, default value now()
- file_url (text): URL of the invoice file, default value NULL
- deleted_at (timestamptz): Date and time when the record was deleted, default value NULL
- organization_id (int8): Organization ID, default value '2'::bigint

Table name: events
Columns:
- id (uuid): Unique identifier of the event, primary key, default value gen_random_uuid()
- user_id (uuid): Identifier of the user associated with this event, primary key
- title (varchar): Title of the event, default value NULL
- description (varchar): Description of the event, default value NULL
- start_time (timestamptz): Start time of the event, default value NULL
- end_time (timestamptz): End time of the event, default value NULL
- event_type_id (int4): Type of the event, default value NULL
- created_at (timestamptz): Date and time when the record was created, default value now()
- updated_at (timestamptz): Date and time when the record was last updated, default value now()
- deleted_at (timestamptz): Date and time when the record was deleted, default value NULL
- client_id (uuid): Identifier of the client associated with this event, default value NULL
- organization_id (int8): Organization ID, default value '2'::bigint
- owners (uuid): Owners of the event, default value NULL

Table name: files
Columns:
- id (uuid): Unique identifier of the file, primary key, default value gen_random_uuid()
- created_at (timestamptz): Date and time when the record was created, default value now()
- updated_at (timestamptz): Date and time when the record was last updated, default value now()
- type (varchar): Type of the file, default value NULL
- file_name (varchar): Name of the file, default value NULL
- file_size (varchar): Size of the file, default value NULL
- deleted_at (timestamptz): Date and time when the record was deleted, default value NULL
- created_by (uuid): Identifier of the user who created the file, default value auth.uid()
- file_url (varchar): URL of the file, default value NULL
- owner_id (uuid): Identifier of the owner of the file, default value NULL

Table name: onglets_dynamique
Columns:
- id (int8): Unique identifier of the dynamic tab, primary key, default value nextval('onglets_dynamique_id_seq'::regclass)
- created_at (timestamptz): Date and time when the record was created, default value now()
- updated_at (timestamptz): Date and time when the record was last updated, default value now()
- slug (varchar): Slug of the dynamic tab, default value NULL
- fields (jsonb): Fields of the dynamic tab, default value NULL
- organization_id (int8): Organization ID, default value '2'::bigint

Table name: order_cart
Columns:
- id (uuid): Unique identifier of the cart item, primary key, default value gen_random_uuid()
- created_at (timestamptz): Date and time when the record was created, default value now()
- updated_at (timestamptz): Date and time when the record was last updated, default value now()
- order_id (uuid): Identifier of the order associated with this cart item, default value NULL
- product_id (uuid): Identifier of the product in the cart, default value NULL
- quantity (int4): Quantity of the product, default value 1
- price_ht (numeric): Price before tax, default value NULL
- tva (numeric): Tax amount, default value NULL

Table name: orders
Columns:
- id (uuid): Unique identifier of the order, primary key, default value gen_random_uuid()
- client_id (uuid): Identifier of the client associated with this order
- reduction_rate (numeric): Reduction rate applied to the order
- reduction_amount (numeric): Reduction amount applied to the order
- note (varchar): Additional notes for the order
- created_by (uuid): Identifier of the user who created the order
- updated_by (uuid): Identifier of the user who last updated the order
- deleted_at (timestamptz): Date and time when the order was deleted, default value NULL
- created_at (timestamptz): Date and time when the order was created, default value now()
- updated_at (timestamptz): Date and time when the order was last updated, default value now()
- payment_method (varchar): Method of payment, default value 'Virement'
- ref (int4): Reference number for the order
- custom_installation_power (float4): Custom installation value
- custom_prime (int4): Custom prime value

Table name: packs
Columns:
- id (uuid): Unique identifier of the pack, primary key, default value gen_random_uuid()
- name (varchar): Name of the pack, default value 'price_ht'
- description (varchar): Description of the pack
- price_ht (float8): Price excluding tax
- created_at (timestamptz): Date and time when the pack was created, default value now()
- deleted_at (timestamptz): Date and time when the pack was deleted, default value NULL
- updated_at (timestamptz): Date and time when the pack was last updated, default value now()
- created_by (uuid): Identifier of the user who created the pack, default value auth.uid()
- updated_by (uuid): Identifier of the user who last updated the pack, default value auth.uid()
- tva (int4): Tax rate, default value 8
- pack_image (text): Image associated with the pack
- price_ttc (float8): Price including tax
- published (bool): Whether the pack is published, default value false
- isTTc (bool): Whether the price is including tax, default value false
- organization_id (int8): Organization ID, default value '2'::bigint

Table name: packs_products
Columns:
- pack_id (uuid): Identifier of the pack, part of composite primary key
- product_id (uuid): Identifier of the product, part of composite primary key
- created_at (timestamptz): Date and time when the association was created, default value now()
- deleted_at (timestamptz): Date and time when the association was deleted, default value NULL
- quantity (int4): Quantity of the product in the pack, default value 1

Table name: product
Columns:
- id (uuid): Unique identifier, primary key, default value gen_random_uuid()
- created_at (timestamptz): Date and time when the record was created, default value now()
- updated_at (timestamptz): Date and time when the record was last updated, default value now()
- name (varchar): Name of the product, default value NULL
- description (varchar): Description of the product, default value NULL
- category_id (int4): Category ID of the product, default value NULL
- price_ht (float8): Price excluding tax, default value NULL
- created_by (uuid): Identifier of the user who created the product, default value NULL
- updated_by (uuid): Identifier of the user who last updated the product, default value NULL
- deleted_at (timestamptz): Date and time when the record was deleted, default value NULL
- published (bool): Whether the product is published, default value false
- product_image (text): Image associated with the product, default value NULL
- technical_specs (json): Technical specifications of the product, default value NULL
- technical_file (text): Technical file associated with the product, default value NULL
- power (numeric): Power of the product, default value NULL
- type_installation (varchar): Type of installation for the product, default value NULL
- tva (float4): Tax rate for the product, default value NULL
- isTTc (bool): Whether the price includes tax, default value false
- organization_id (int8): Organization ID, default value '2'::bigint

Table name: product_categories
Columns:
- id (int4): Unique identifier, primary key, default value nextval('product_categories_id_seq'::regclass)
- name (varchar): Name of the category, default value NULL
- description (varchar): Description of the category, default value NULL
- created_by (uuid): Identifier of the user who created the category, default value NULL
- created_at (timestamptz): Date and time when the record was created, default value now()
- updated_at (timestamptz): Date and time when the record was last updated, default value now()
- updated_by (uuid): Identifier of the user who last updated the category, default value NULL
- deleted_at (timestamptz): Date and time when the record was deleted, default value NULL
- parent_category (int4): ID of the parent category, default value NULL
- is_dynamic (bool): Whether the category is dynamic, default value false
- organization_id (int8): Organization ID, default value '2'::bigint

Table name: roles
Columns:
- id (uuid): Unique identifier of the role, primary key, default value gen_random_uuid()
- description (varchar): Description of the role, default value NULL
- created_at (timestamptz): Date and time when the record was created, default value now()
- updated_at (timestamptz): Date and time when the record was last updated, default value NULL
- deleted_at (timetz): Date and time when the record was deleted, default value NULL
- permission_level (int2): Permission level, default value 3
- organization_id (int8): Organization ID, default value '2'::bigint

Table name: roles_permissions
Columns:
- id (uuid): Unique identifier of the role permission, primary key, default value gen_random_uuid()
- permission_id (uuid): ID of the permission, default value NULL
- role_id (uuid): ID of the role, default value NULL
- created_at (timestamptz): Date and time when the record was created, default value now()
- create (bool): Create permission flag, default value false
- update (bool): Update permission flag, default value false
- delete (bool): Delete permission flag, default value false
- read (bool): Read permission flag, default value false
- team_id (uuid): ID of the team, default value NULL

Table name: sources
Columns:
- id (int8): Unique identifier of the source, primary key, default value nextval('sources_id_seq'::regclass)
- name (text): Name of the source, default value NULL
- created_at (timestamptz): Date and time when the record was created, default value now()
- deleted_at (timestamptz): Date and time when the record was deleted, default value NULL
- created_by (uuid): ID of the user who created the record, default value NULL

Table name: statut
Columns:
- id (int4): Unique identifier of the status, primary key
- name (varchar): Name of the status, default value NULL
- description (varchar): Description of the status, default value NULL
- category (varchar): Category of the status, default value ''::character varying
- created_at (timestamptz): Date and time when the record was created, default value now()
- updated_at (timestamptz): Date and time when the record was last updated, default value now()
- created_by (uuid): ID of the user who created the record, default value NULL
- deleted_at (timestamptz): Date and time when the record was deleted, default value NULL
- updated_by (uuid): ID of the user who last updated the record, default value NULL
- sub_category (varchar): Sub-category of the status, default value ''::character varying
- event_id (int4): Event ID associated with the status, default value NULL
- parent_category (varchar): Parent category of the status, default value NULL
- color (varchar): Color associated with the status, default value NULL
- organization_id (int8): Organization ID, default value '2'::bigint

Table name: suppliers
Columns:
- id (uuid): Unique identifier of the supplier, primary key, default value gen_random_uuid()
- supplier_name (varchar): Name of the supplier, default value NULL
- supplier_email (varchar): Email of the supplier, default value NULL
- company_domicile (varchar): Company domain of the supplier, default value NULL
- company_director (varchar): Company directory of the supplier, default value NULL
- created_at (timestamptz): Date and time when the record was created, default value now()
- updated_at (timestamptz): Date and time when the record was last updated, default value now()
- deleted_at (timestamptz): Date and time when the record was deleted, default value NULL
- organization_id (int8): Organization ID, default value '2'::bigint

Table name: teams
Columns:
- id (uuid): Unique identifier of the team, primary key, default value gen_random_uuid()
- name (varchar): Name of the team, default value NULL
- description (varchar): Description of the team, default value NULL
- created_at (timestamptz): Date and time when the record was created, default value now()
- updated_at (timestamptz): Date and time when the record was last updated, default value now()
- updated_by (uuid): ID of the user who last updated the record, default value NULL
- deleted_at (timestamptz): Date and time when the record was deleted, default value NULL
- created_by (uuid): ID of the user who created the record, default value NULL
- organization_id (int8): Organization ID, default value '2'::bigint

Table name: tiers
Columns:
- id (int8): Unique identifier of the tier, primary key
- name (text): Name of the tier, default value NULL
- description (text): Description of the tier, default value NULL
- features (jsonb): Features of the tier, default value '[]'::jsonb
- created_at (timestamptz): Date and time when the record was created, default value now()
- updated_at (timestamptz): Date and time when the record was last updated, default value NULL

Table name: users_meta_data
Columns:
- id (uuid): Unique identifier of the user metadata, primary key, default value gen_random_uuid()
- created_at (timestamptz): Date and time when the record was created, default value now()
- updated_at (timestamptz): Date and time when the record was last updated, default value now()
- first_name (varchar): First name of the user, default value NULL
- last_name (varchar): Last name of the user, default value NULL
- civility (civilite): Civility of the user, default value NULL
- email (varchar): Email of the user, default value NULL
- team_id (uuid): ID of the team the user belongs to, default value NULL
- tel (varchar): Telephone number of the user, default value NULL
- deleted_at (timestamptz): Date and time when the record was deleted, default value NULL
- role_id (uuid): ID of the user's role, default value NULL
- auth_id (uuid): Authentication ID of the user, default value NULL
- address (text): Address of the user, default value NULL
- organization_id (int8): Organization ID, default value '2'::bigint
"""
TABLES_RELATIONSHIPS = """
1. client
   - created_by -> users_meta_data.id
   - id_address_facturation -> address.id
   - id_address_installation -> address.id
   - organization_id -> organizations.id
   - processed_by_id -> users_meta_data.id
   - source_id -> sources.id
   - statut_id -> statut.id
   - updated_by -> users_meta_data.id
   - supplier_id -> suppliers.id

2. client_invoices
   - client_id -> client.client_id
   - organization_id -> organizations.id

3. client_notes
   - client_id -> client.client_id
   - created_by -> users_meta_data.id
   - note_type -> statut.id

4. etude
   - client_id -> client.client_id
   - created_by -> users_meta_data.id

5. events
   - event_type_id -> statut.id
   - organization_id -> organizations.id
   - user_id -> users_meta_data.id
   - client_id -> client.client_id

6. files
   - created_by -> users_meta_data.id
   - owner_id -> client.client_id

7. onglets_dynamique
   - organization_id -> organizations.id

8. orders
   - client_id -> client.client_id
   - created_by -> users_meta_data.id
   - updated_by -> users_meta_data.id

9. organizations
    - tier_id -> tiers.id

10. packs
    - created_by -> users_meta_data.id
    - organization_id -> organizations.id
    - updated_by -> users_meta_data.id

11. product_categories
    - organization_id -> organizations.id

12. product
    - organization_id -> organizations.id

13. address
    - client_id -> client.client_id

14. payments
    - organization_id -> organizations.id
    - client_id -> client.client_id
    - order_id -> orders.id

15. users_meta_data
    - auth_id -> users.id
    - organization_id -> organizations.id
    - role_id -> roles.id
    - team_id -> teams.id

16. roles
    - organization_id -> organizations.id

17. roles_permissions
    - permission_id -> permissions.id
    - role_id -> roles.id
    - team_id -> teams.id

18. sources
    - created_by -> users_meta_data.id

19. statut
    - created_by -> users_meta_data.id
    - event_id -> statut.id
    - organization_id -> organizations.id
    - updated_by -> users_meta_data.id

20. suppliers
    - organization_id -> organizations.id

21. teams
    - created_by -> users_meta_data.id
    - organization_id -> organizations.id
    - updated_by -> users_meta_data.id
"""


model = ChatOpenAI(openai_api_key=OPENAI_KEY, model=MODEL, temperature=0.5)

list_prompt = ChatPromptTemplate.from_template("""
Act as an SQL and plotly expert.
I need you to translate this request into SQL for a PostgreSQL database.
Don't assume any additional information on the structure of the db.
If the request is impossible to satisfy, write a clear error message for the user.
If the request is not precise enough, ask me a refinement question and I will give you details.
I am not a developer and I don't know anything about SQL or the structure of the database.
If I don't ask you to select specific columns of a table select them all.
The database is PostgreSQL.

Important: Always filter the results to include only information related to the specified organization_id or clients associated with that organization_id. Follow these steps:
1. If the main table has an organization_id column, use it directly: WHERE organization_id = {organization_id}
2. If the main table has a client_id column but no organization_id, join with the client table:
   JOIN client ON main_table.client_id = client.client_id WHERE client.organization_id = {organization_id}
3. If the main table has neither organization_id nor client_id, use the table relationships to join with tables that do have these columns.
   Chain multiple JOINs if necessary to reach a table with organization_id or client_id.

Use {organization_id} as the parameter for the organization ID in your query.

Here is the list of table relationships:
{tables_relationships}

Here is the description of the tables:
{description_tables}

Generate the SQL query that matches this request: "{request}"
The goal is to be able to execute SQL scripts to interact with the database.
Do not include any explanations, only provide a RFC8259 compliant JSON response following one of these 2 formats without deviation.
{{"query": <insert query>, "columns": [<list of columns names returned>]}}
OR
{{"error": <insert error>}}
""")

plotly_prompt = ChatPromptTemplate.from_template("""
Act as an SQL and plotly expert.
I need you to translate this request into SQL for a PostgreSQL database so that I can plot it with plotly.
I want to plot the data, make sure the SQL query returns two columns, the first one is the X axis and the second one is the Y axis.
Choose the best plot type for my data and insert it in "plot_type".
Don't assume any additional information on the structure of the db.
If the request is impossible to satisfy, write a clear error message for the user.
If the request is not precise enough, ask me a refinement question and I will give you details.
I am not a developer and I don't know anything about SQL or the structure of the database.
If I don't ask you to select specific columns of a table select them all.
The database is PostgreSQL.

Important: Always filter the results to include only information related to the specified organization_id or clients associated with that organization_id. Follow these steps:
1. If the main table has an organization_id column, use it directly: WHERE organization_id = {organization_id}
2. If the main table has a client_id column but no organization_id, join with the client table:
   JOIN client ON main_table.client_id = client.client_id WHERE client.organization_id = {organization_id}
3. If the main table has neither organization_id nor client_id, use the table relationships to join with tables that do have these columns.
   Chain multiple JOINs if necessary to reach a table with organization_id or client_id.

Use {organization_id} as the parameter for the organization ID in your query.

Here is the list of table relationships:
{tables_relationships}

Here is the description of the tables:
{description_tables}

Generate the SQL query that matches this request: "{request}"

Do not include any explanations, only provide a RFC8259 compliant JSON response following one of these 3 formats without deviation.
{{ "need_more_tables": [write the names of the tables and i will provide their full description] }}
OR
{{"query": <insert query>, "plot_type": <can be hist/line/bar/pie>, "x_legend": <>, "y_legend": <>, "plot_title": <>}}
OR
{{ "error": <insert error if any>, "refine": <insert refinment question if any >" }}
""")

output_parser = StrOutputParser()

@functions_framework.http
def sql_query_generator(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'request' in request_json:
        user_request = request_json['request']
        is_list = request_json.get('isList', False)
        organization_id = request_json.get('organization_id')
    elif request_args and 'request' in request_args:
        user_request = request_args['request']
        is_list = request_args.get('isList', 'false').lower() == 'true'
        organization_id = request_args.get('organization_id')
    else:
        return json.dumps({"error": "No 'request' parameter provided"}), 400, {'Content-Type': 'application/json'}

    if not organization_id:
        return json.dumps({"error": "No 'organization_id' parameter provided"}), 400, {'Content-Type': 'application/json'}

    try:
        prompt = list_prompt if is_list else plotly_prompt
        chain = prompt | model | output_parser
        result = chain.invoke({"request": user_request, "description_tables": DESCRIPTION_TABLES, "tables_relationships": TABLES_RELATIONSHIPS, "organization_id": organization_id})
        return result, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return json.dumps({"error": str(e)}), 500, {'Content-Type': 'application/json'}