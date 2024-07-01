from openai import OpenAI
from os import getenv

from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=getenv("OPENROUTER_API_KEY"),
)

completion = client.chat.completions.create(
  model="anthropic/claude-3.5-sonnet",
  messages=[
    {
      "role": "user",
      "content": "Say this is a test",
    },
  ],
)
print(completion.choices[0].message.content)