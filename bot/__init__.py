import os
from mistralai import Mistral

api_key = "QRAdCvnRGJaLRXHwEiy3wSRojN0wHCLY"
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

chat = client.chat.complete(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "How are you!"
        },
    ]
)

response_text = chat.choices[0].message.content
print(response_text)