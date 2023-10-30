"""
The vector database is being created for Dan Jurafsky's Speech and Language Processing. 

The approach that is followed: 
- Use ChatGPT to provide us with simple sentences that can be used to perform similarity search in vector database. 
- Extract the relevant passages from the text and add them as context to the question generation prompt. 
"""

import openai
import os
import re

from datetime import datetime
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Qdrant
from langchain.document_loaders import PDFMinerLoader

from dotenv import load_dotenv
load_dotenv()

CONTEXT_FILE_PATH = "./data/2.pdf"
PROMPT_FILE_PATH = "./prompts/vectordb-prompt.txt"
BREAKDOWN_PROMPT_FILE_PATH = "./prompts/vectordb-breakdown-prompt.txt"
RESPONSE_FILE_PATH = lambda timestamp: f"./responsebuffers/{timestamp} (vectordb).txt"

TOPIC = "Regular Expressions, Text Normalization, Edit Distance"

openai.organization = os.getenv("OPENAI_ORGANIZATON")
openai.api_key = os.getenv("OPENAI_API_KEY")

chunks = list()
prompt = str()
with open(BREAKDOWN_PROMPT_FILE_PATH, "r+") as file:
  prompt = file.read()

prompt = prompt.replace("<SENTENCE>", TOPIC)

response = openai.Completion.create(
  engine="text-davinci-003",
  prompt=prompt,
  temperature=1,
  max_tokens=500
)

raw_chunks = response.choices[0].text.strip().split("\n")
for chunk in raw_chunks:
  sub_chunks = re.split(r'[.,;]', chunk)
  chunks.extend([sub.strip() for sub in sub_chunks if sub.strip() and not sub.strip().isdigit()])

loader = PDFMinerLoader(CONTEXT_FILE_PATH)
pages = loader.load_and_split()
text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
docs = text_splitter.split_documents(pages)

embeddings = OpenAIEmbeddings()
qdrant = Qdrant.from_documents(
  docs,
  embeddings,
  path="./tmp/danjurafsky",
  collection_name="danjurafsky",
)

context = str()
relevance_docs_with_scores = [qdrant.similarity_search_with_score(chunk) for chunk in chunks]
for doc in relevance_docs_with_scores:
  context += doc[0][0].page_content
  context += "\n"

prompt = str()
with open(PROMPT_FILE_PATH, "r+") as file:
  prompt = file.read()

prompt = prompt.replace("<CONTEXT>", context)

completion = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {
      "role": "system",
      "content": "You are a highly skilled subject matter expert in Computer Science and the best question architect.",
    },
    {
      "role": "user", 
      "content": prompt
    },
  ],
  temperature=0,
  max_tokens=5000,
)

response = completion["choices"][0]["message"]["content"]

with open(RESPONSE_FILE_PATH(datetime.now().strftime("%d-%m-%Y %H:%M:%S")), "w+") as file:
  file.write(response)

