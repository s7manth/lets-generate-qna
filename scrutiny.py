"""
An attempt towards LLM based scrutiny to evaluate the effectiveness of generated MCQs. 
"""

import openai
import os

from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

SCRUTINY_PROMPT_FILE_PATH = "./prompts/scrutiny-prompt.txt"
TO_SCRUTINY = "./responsebuffers/vectordb-response.txt"
RESPONSE_FILE_PATH = lambda timestamp: f"./responsebuffers/{timestamp} (scrutiny).txt"

openai.organization = os.getenv("OPENAI_ORGANIZATON")
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = str()
with open(SCRUTINY_PROMPT_FILE_PATH, "r+") as file:
  prompt = file.read()

with open(TO_SCRUTINY, "r+") as file:
  prompt = prompt.replace("<ATTEMPT>", file.read())

completion = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {
      "role": "system",
      "content": "You are a highly skilled subject matter expert in Natural Language Processing and a creative question architect. You think critically before answering any question.",
    },
    {
      "role": "user", 
      "content": prompt
    },
  ],
  temperature=1,
  max_tokens=5000,
)

response = completion["choices"][0]["message"]["content"]

with open(RESPONSE_FILE_PATH(datetime.now().strftime("%d-%m-%Y %H:%M:%S")), "w+") as file:
  file.write(response)

