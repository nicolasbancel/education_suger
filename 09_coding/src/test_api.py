from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);
