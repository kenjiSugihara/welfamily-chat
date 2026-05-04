import streamlit as st
import google.generativeai as genai

# ページとUIの設定
st.set_page_config(page_title="Welfamily - 心の伴走者", page_icon="🍀", layout="centered")

st.title("Welfamily - パートナー関係の心の伴走者 🍀")
st.write("夫婦関係やパートナーとの関係で悩んでいること、日々のちょっとした心配事から大きなお悩みまで、何でもお話しください。Welfamilyが優しく寄り添い、ワンポイントでアドバイスをお届けします。")

# サイドバーでAPIキーを取得
st.sidebar.title("設定")
st.sidebar.write("Google GeminiのAPIキーを入力してチャットを開始してください。")
api_key = st.sidebar.text_input("Gemini APIキー", type="password")

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 過去のメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーからの入力
if prompt := st.chat_input("今の気持ちや悩みを教えてください..."):
    # ユーザーの入力を画面に表示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # APIキーが設定されている場合のみAIが応答
    if api_key:
        genai.configure(api_key=api_key)
        
        # 心理学と男女コミュニケーションの専門家としてのシステムプロンプト
        system_instruction = """
        あなたは心理学と男女のコミュニケーションの専門家であり、「Welfamily」というブランド名でユーザーに優しく寄り添う心の伴走者です。
        以下の知識をベースに、相談者に対してまずは深く共感し、その後にワンポイントのアドバイスを提供してください。
        
        【ベースとする知識と方針】
        * 女性脳は共感欲求が非常に高く、「わかる、わかる」と共感されることで過剰なストレス信号が沈静化します。[cite: 1]
        * 女性の会話の目的は共感であり、男性の会話の目的は問題解決です。[cite: 1]
        * 女性脳は体験記憶に感情の見出しをつけて収納しているため、一つの出来事をトリガーに何十年分もの関連記憶を一気に引き出す特性があります。[cite: 1]
        * 事実の通信線よりも前に、まず相手の「心」を肯定する「心の通信線」を繋ぐことが重要であり、正論を突きつける必要はありません。[cite: 1]
        * 夫一筋、家庭一筋の妻ほど、期待の裏返しとして「怒り」を抱えやすい傾向があります。[cite: 1]
        * パートナーへの不満はコップに1滴ずつ水が落ちるように蓄積されるため、「セキュリティ問題」として捉え、日々の気遣いや感謝を伝えることが重要です。[cite: 1]
        * 夫婦間の会話がない場合は、何らかの不満を抱えているサインであるため、普段とは違う気遣いや、少しの褒め言葉をかけることで関係改善に繋がります。[cite: 1]
        * 「こうしてほしい」という要求と、それを避ける回避の悪循環（接近―回避のコミュニケーションパターン）に陥った場合は、自分自身の内面を知り、カウンセリング等で第三者の冷静な意見を参考にすることが有効です。[cite: 1]
        
        【応答のルール】
        1. ユーザーの感情（不安、怒り、悲しみなど）を絶対に否定せず、まずは深く受け止めて共感してください。
        2. 問題解決を急ぐのではなく、「心の通信線」を繋ぐことを最優先にしてください。[cite: 1]
        3. 専門用語を多用しすぎず、温かく優しいトーンで語りかけてください。
        4. 長すぎない構成にし、今日から少しだけ実践できる「ワンポイントアドバイス」を添えてください。
        5. 自身の名前を名乗る際は「Welfamily」としてください。
        """
        
        # モデルの初期化
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=system_instruction
        )
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # 履歴のフォーマットをGemini用に変換
            history = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
            chat = model.start_chat(history=history)
            
            try:
                # AIからの応答を取得してストリーミング表示
                response = chat.send_message(prompt, stream=True)
                full_response = ""
                for chunk in response:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                
                # 履歴に保存
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("サイドバーからAPIキーを設定してください。")