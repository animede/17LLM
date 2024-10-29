from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from openai import AsyncOpenAI
import json

app = FastAPI()

client = AsyncOpenAI(
    base_url='http://127.0.0.1:8080/v1',
    api_key="YOUR_OPENAI_API_KEY",)  # このままでOK

@app.get("/", response_class=HTMLResponse)
async def get():
    with open('static/index4B.html', 'r') as f:
        return f.read()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
            data = await websocket.receive_text()
            data_dict = json.loads(data)  # 受信したJSONデータをPython辞書に変換
            message = data_dict.get("message")
            role = data_dict.get("role")
            print(f"Received message: {message} with role: {role}")
            stream = await client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": role, "content": message}],
                stream=True,)
            response_buffer = []
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    response_message=chunk.choices[0].delta.content
                    response_buffer.append(response_message)
                    await  websocket.send_text(response_message) # チャンクをリアルタイムで送信
            response_sum = "".join(response_buffer)
            print("chunk sum  ==>", response_sum)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8004)



