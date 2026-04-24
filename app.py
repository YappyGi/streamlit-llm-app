import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
# 環境変数の読み込み
load_dotenv()

# OpenAI APIキーの設定
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Webアプリの概要と操作方法を表示
st.title("専門家AIアシスタント")
st.write("このアプリは、選択した専門家の視点から、あなたの質問に答えます。")

# セッションステートで会話履歴を管理
# ページがリロードされても履歴が保持されるようにする
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 入力フォームの作成
with st.form(key='my_form', clear_on_submit=True):
    # 入力フォーム
    user_input = st.text_area("ここに質問を入力してください")

    # 送信ボタン
    submit_button = st.form_submit_button(label='回答を取得する')

# ラジオボタンの作成
expert_type = st.radio(
    "専門家の種類を選択してください:",
    ("ITコンサルタント", "歴史学者", "栄養士")
)

# 選択された専門家に応じてシステムメッセージを決定
if expert_type == "ITコンサルタント":
    system_message = "あなたは優秀なITコンサルタントです。ユーザーの質問に対し、専門家の視点から、解決策や戦略を提案してください。"
elif expert_type == "歴史学者":
    system_message = "あなたは優秀な歴史学者です。ユーザーの質問に対し、史実に基づいた正確な情報や歴史的な背景を解説してください。"
elif expert_type == "栄養士":
    system_message = "あなたは優秀な栄養士です。ユーザーの質問に対し、科学的根拠に基づいた栄養や健康に関するアドバイスを、分かりやすく提供してください。"
else:
    system_message = "あなたは優秀な専門家です。ユーザーの質問に対し、専門家の視点から、適切な情報やアドバイスを提供してください。" \
    "ただし、専門家の種類が不明な場合は、一般的な知識に基づいて回答してください。"

# LLMからの回答を返す関数
def get_llm_response(prompt, system_message):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# ユーザーがテキストを入力、LLMに質問を送信したときの処理
if submit_button:
    if user_input:
        st.info("AIが回答を生成中です...しばらくお待ちください。")
        with st.spinner("AIが思考中..."):
            response_text = get_llm_response(user_input, system_message)
        
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": response_text})

        st.success("回答が生成されました！会話履歴に表示・追加されます。")

    else:
        st.warning("質問を入力してください。")
    
# 履歴の表示をボタンの外へ
# 回答が生成された後に履歴を更新
st.markdown("---")
st.subheader("会話履歴")
for message in st.session_state["messages"]:
    if message["role"] == "user":
       st.write(f"**ユーザー**: {message['content']}")
    else:
       st.write(f"**AI**: {message['content']}") 
