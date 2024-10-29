import gradio as gr
import openai
from   openai import AsyncOpenAI
import asyncio

# OpenAI APIの設定
client = AsyncOpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="YOUR_OPENAI_API_KEY",  # このままでOK
    )

# OpenAI APIから応答を取得する非同期ジェネレーター関数
async def chat_with_openai(role, user_message, conversation_logs, max_logs=5):
    try:
        # 会話履歴にroleとユーザーメッセージを追加
        messages = [{"role": "system", "content": role}] + conversation_logs + [{"role": "user", "content": user_message}]
        # デバッグ用のメッセージ出力
        print(f"Sending to API: {messages}")
        # ストリーミングリクエストを実行
        stream = await client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            stream=True,
        )
        response_sum = ""
        # ストリーミングで応答を処理
        async for chunk in stream:
            response_chunk = chunk.choices[0].delta.content or ""
            response_sum += response_chunk
            print(response_sum)
            yield response_chunk  # 部分的な応答をストリーミング
        # 全体の応答を保存
        conversation_logs.append({"role": "assistant", "content": response_sum})
        # 会話ログが最大数を超えた場合、古いログを削除
        if len(conversation_logs) > max_logs:
            conversation_logs = conversation_logs[-max_logs:]
    except Exception as e:
        yield f"Error: {str(e)}"

# ユーザーのメッセージを送信し、応答を処理する関数
async def submit_message(role, message, logs):
    role = role or "You are a helpful assistant."  # デフォルトのrole設定
    response_chunks = ""
    # OpenAI APIとストリーミングでやり取り
    async for response_chunk in chat_with_openai(role, message, logs):
        response_chunks += response_chunk
        yield response_chunks, logs  # 応答を順次表示

# Gradio UIの定義
def create_ui():
    with gr.Blocks() as demo:
        with gr.Row():
            role_input = gr.Textbox(label="LLMへのRole", value="You are a helpful assistant.")
            conversation_logs = gr.State(value=[])
            response_output = gr.Textbox(label="応答", interactive=False)
        with gr.Row():
            message_input = gr.Textbox(label="メッセージを入力")
        # エンターキーでメッセージを送信できるようにする
        message_input.submit(
            fn=submit_message,
            inputs=[role_input, message_input, conversation_logs],
            outputs=[response_output, conversation_logs],
            concurrency_limit=2  # 並行処理の制限
           )
    return demo

# サーバーを起動
if __name__ == "__main__":
    demo = create_ui()
    demo.launch(server_name="127.0.0.1", server_port=8009)







