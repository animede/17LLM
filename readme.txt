llama.cppによるOpenAI互換サーバと様々なクライアントを動かします。

事前にCUDA-Toolkitをインストールしてください

https://developer.nvidia.com/cuda-downloads
環境を選ぶとインストールコマンドが表示されるのでそのままコピペします。networkインストールが楽だと思います

パスを通しておきましょう（よく忘れます）
export PATH=/usr/local/cuda:/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/lib:/usr/local/cuda/lib64:$LD_LIBRARY_PATH
source ~/.bashrc

確認
NVCC -V


1,　llama.cppのインストール
   仮想環境作成の準備
　 sudo apt install python3.11-venv

  仮想環境作成
   git clone https://github.com/ggerganov/llama.cpp.git
   python3.11 -m venv llama
   source llama/bin/activate
  
  構築 (cmakeが無いというエラーが出るときはメッセージに従いcmakeをインストール）
   cmake -B build -DGGML_CUDA=ON
   cmake --build build --config Release
    すごく時間がかかります
   cd llama.cpp
　
  build/binフォルダのbinファイルへパスを通すか生成された全てのbinファイルをリポジトリのルートにコピー
　
　モジュールのインストール
   pip install openai
   pip install fastapi
   pip install gradio

このリポジトリのクローン
  git clone https://github.com/animede/17LLM.git

2,　モデルのダウンロード
  gemma-2シリーズ
  https://huggingface.co/bartowski/gemma-2-9b-it-GGUF
  から
  gemma-2-9b-it-Q4_K_M.gguf

　https://huggingface.co/bartowski/gemma-2-27b-it-GGUF　
　から
  gemma-2-27b-it-IQ2_M.gguf

  https://huggingface.co/bartowski/gemma-2-2b-jpn-it-GGUF
  から
  gemma-2-2B-jpn-it-Q4_K_M.gguf

  をダウンロード どちらも16GbyteのGPUメモリー又はCPUで動きます。

  lama3-2シリーズ
  https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF
  から
  Llama-3.2-1B-Instruct-Q4_K_M.gguf
  をダウンロード。2Gbyteで動きます。


3,　CLIで会話
  ./llama-cli -m models/gemma-2-2B-jpn-it-Q4_K_M.gguf -p "あなたは賢いaiですUserの質問に答えなさい" -cnv  --n-gpu-layers 27
  
  コマンドラインで対話が出来ます。

4,　サーバを動かす
   以下のコマンドを入力。それぞれ動かして性能を比べてください。gemma-2-2BやLlama-3.2-1BはCPUでも十分な速度です。
  --n-gpu-layersをコマンドから外すとCPUで動きます。これらのサーバはクライアントからOpenAI互換API接続で動きます。
  

  ./llama-server -m models/gemma-2-2B-jpn-it-Q4_K_M.gguf --n-gpu-layers 27 --port 8080 

  ./llama-server -m models/gemma-2-9b-it-Q4_K_M.gguf --n-gpu-layers 43 --port 8080

  ./llama-server -m models/gemma-2-27b-it-IQ2_M.gguf --n-gpu-layers 47 --port 8080

  ./llama-server -m models/Llama-3.2-1B-Instruct-Q4_K_M.gguf --n-gpu-layers 43 --port 8080

5,　クライアント側コマンドラインテスト
　1）単純なテスト
　　ユーザーニュー力がコードに埋め込まれて、回答だけが出力されます。
　　
　　python openai_test.py

　2）会話テスト
　   会話が出来ます。
　   
　  python python openai_conv_test.py
　
　3)シンプルなGUI
　
　  python openai_gradio.py
　  
    Gradioベースの最もシンプルなGUIです。
　   ブラウザからhttp://127.0.0.1:8009にアクセスします。
　  LLMへのRoleにはLLMに振る舞ってほしいことを書きます
　    単純な回答：userの質問に答えなさい
　    翻訳の場合：userの入力した日本語を英語に翻訳しなさい
　    キャラ付け：あなたは大阪出身の女子高生です、大阪弁で回答しなさい

　4）チャットができるGUIアプリ
　
　　python openai_gui_simple.py
　　
　 FastAPIとHTML、CSSで構成されるシンプル化されたフロント+バックエンドシステムです。
　 ブラウザからhttp://127.0.0.1:8002にアクセスします。
 　python openai_gui_simple.py
　 LLMへのRoleには3)シンプルなGUIと同様な記述が出来ます。
　 会話記憶ができます。
　 LLM側の名前が指定出来ます。
　
　5）Line風のGUIによるチャットアプリ
　
　 python openai_gui_multiai.py

   FastAPIとHTML、CSSで構成されるシンプル化されたフロント+バックエンドシステムです。
     ブラウザからhttp://127.0.0.1:8004にアクセスします。
　 LLMへのRoleには3)シンプルなGUIと同様な記述が出来ます。
　 二人のキャラクタ別にRoleが指定できます。
　二人のLLM側の名前とユーザーの名前の指定出来ます。
　どちらかを選んで会話できます。
　 会話記憶ができます。
　 二人のAI同士が会話することが出来ます。ユーザーのトリガワードで会話が始まります。
　 二人のAI同士が会話中にユーザーが割り込むことも出来ます。
　  
　  


おおよその処理速度　4060TI-16G
gemma-2-2B-jpn-it-Q4_K_M.gguf 

llama_perf_context_print: prompt eval time =      70.20 ms /     6 tokens (   11.70 ms per token,    85.47 tokens per second)
llama_perf_context_print:        eval time =    6706.19 ms /   127 runs   (   52.80 ms per token,    18.94 tokens per second)
llama_perf_context_print:       total time =    6825.94 ms /   133 tokens

llama_perf_context_print: prompt eval time =      10.97 ms /     6 tokens (    1.83 ms per token,   546.95 tokens per second)
llama_perf_context_print:        eval time =     701.91 ms /    98 runs   (    7.16 ms per token,   139.62 tokens per second)
llama_perf_context_print:       total time =     743.97 ms /   104 tokens


gemma-2-9b-it-Q4_K_M.gguf

llama_perf_context_print: prompt eval time =     232.40 ms /     6 tokens (   38.73 ms per token,    25.82 tokens per second)
llama_perf_context_print:        eval time =   18232.73 ms /   109 runs   (  167.27 ms per token,     5.98 tokens per second)
llama_perf_context_print:       total time =   18508.49 ms /   115 tokens

llama_perf_context_print: prompt eval time =      35.34 ms /     6 tokens (    5.89 ms per token,   169.79 tokens per second)
llama_perf_context_print:        eval time =    1116.44 ms /    58 runs   (   19.25 ms per token,    51.95 tokens per second)
llama_perf_context_print:       total time =    1172.46 ms /    64 tok

参考URL
https://blog.google/technology/developers/google-gemma-2/
https://github.com/ggerganov/llama.cpp
https://blog.google/intl/ja-jp/company-news/technology/gemma-2-2b/
https://huggingface.co/collections/google/gemma-2-jpn-release-66f5d3337fdf061dff76a4f1
https://www.llama.com/


