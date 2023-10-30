"""
Advanced prompt engineering approach without context. 
"""

import openai
import os

from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

PROMPT_FILE_PATH = "./prompts/vanilla-prompt.txt"
RESPONSE_FILE_PATH = lambda timestamp: f"./responsebuffers/{timestamp} (vanilla).txt"

openai.organization = os.getenv("OPENAI_ORGANIZATON")
openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = str()
with open(PROMPT_FILE_PATH, "r+") as file:
  prompt = file.read()

completion = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {
      "role": "system",
      "content": "You are a highly skilled subject matter expert in Natural Language Processing and a creative question architect.",
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

