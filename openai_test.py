from openai import OpenAI

client = OpenAI(
    base_url ='http://127.0.0.1:8080/v1',
    api_key="YOUR_OPENAI_API_KEY", #このままでOK,
)
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "こんにちは"}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
