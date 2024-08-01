import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_KEY')
MODEL = "gpt-4o"

model = ChatOpenAI(openai_api_key=OPENAI_KEY, model=MODEL, temperature=0.5)

prompt = ChatPromptTemplate.from_template("""
Répondez à la question suivante en utilisant un langage formel et professionnel:
question: {question}
""")

output_parser = StrOutputParser()

chain = prompt | model | output_parser

result = chain.invoke({"question": "Quelle est la capitale de la France ?"})
print(result)