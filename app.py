import streamlit as st

# 1. ページ設定とカスタムCSS
st.set_page_config(page_title="Welfamily", layout="wide")

st.markdown("""
<style>
    /* 全体の背景色 */
    .stApp {
        background-color: #f9faf9;
    }
    
    /* ボタンのカスタム */
    .stButton > button {
        background-color: #4a5d4e;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #38463b;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        color: white;
    }

    /* 結果カードのスタイル */
    .result-card {
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        border-top: 6px solid #4a5d4e;
        margin-top: 24px;
    }

    /* タイプ名のアンダーライン */
    .type-title {
        border-bottom: 2px solid #c5a059;
        padding-bottom: 8px;
        margin-bottom: 16px;
        color: #4a5d4e;
    }

    /* 男性・女性用Tryボックス */
    .try-box-m {
        border-left: 4px solid #4a5d4e;
        background-color: #f0f3f1;
        padding: 16px;
        margin-top: 16px;
        border-radius: 0 8px 8px 0;
    }
    .try-box-f {
        border-left: 4px solid #c5a059;
        background-color: #fbf8f2;
        padding: 16px;
        margin-top: 16px;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("Welfamily コミュニケーションタイプ診断")
st.markdown("💡 1:全く当てはまらない 〜 5:非常に当てはまる の5段階で回答ください")

# 2. ユーザー入力UI
col_m, col_f = st.columns(2)

with col_m:
    st.subheader("🧔 男性セクション")
    m1 = st.slider("悩みにはすぐ具体的なアドバイスをしたくなる", 1, 5, 3, key="m1")
    m2 = st.slider("気まずくなると黙り込んだり逃げたくなる", 1, 5, 3, key="m2")
    m3 = st.slider("稼ぐことや家を建てる等の『形』が一番の責任だと思う", 1, 5, 3, key="m3")
    m4 = st.slider("話し合いでは感情より事実関係の正しさを重視する", 1, 5, 3, key="m4")
    m5 = st.slider("相手の感情に共感し、まずは受け止めることが得意だ", 1, 5, 3, key="m5")

with col_f:
    st.subheader("👩 女性セクション")
    f1 = st.slider("解決策よりも、まずは気持ちを分かってほしい", 1, 5, 3, key="f1")
    f2 = st.slider("夫の不在や無関心に強い不安（セキュリティ不足）を感じる", 1, 5, 3, key="f2")
    f3 = st.slider("喧嘩をすると過去の嫌な記憶を芋づる式に思い出しやすい", 1, 5, 3, key="f3")
    f4 = st.slider("自分ばかりが犠牲になって家庭を守っていると感じる", 1, 5, 3, key="f4")
    f5 = st.slider("自分の感情や状況を、主観だけでなく冷静に言語化できる", 1, 5, 3, key="f5")

# 4. 診断結果マトリックスデータ
results_matrix = {
    "A_X": {
        "title": "A×X (正論の要塞)",
        "desc": "男性の解決策が女性の感情を論破しようとし、女性がさらに爆発する悪循環。",
        "m_try": "結論を言う前に「それはしんどかったね」と5秒間、相手の感情をオウム返しに。",
        "f_try": "話す前に「今は解決策はいらないから、10分だけ聴いてほしい」と宣言して。"
    },
    "A_Y": {
        "title": "A×Y (合理性の壁)",
        "desc": "男性の合理的な行動が女性の不安を直撃。孤独が深まります。",
        "m_try": "予定変更は「事実」だけでなく「寂しい思いをさせて申し訳ない」と一言添えて。",
        "f_try": "「なぜ連絡くれないの？」と問わず「声が聞けなくて不安だった」と伝えて。"
    },
    "A_Z": {
        "title": "A×Z (効率戦争)",
        "desc": "お互いに正しさを競い合い、家庭が職場のような殺伐とした空間に。",
        "m_try": "正論が通っても「二人の仲が悪くなれば負け」だと心得て。あえて折れるのが強さ。",
        "f_try": "彼のやり方が非効率でも、一度感謝を伝え、管理の手を少し緩めて。"
    },
    "A_W": {
        "title": "A×W (進化するバディ)",
        "desc": "男性の分析力と女性の言語化能力が噛み合い、建設的に進歩できる関係。",
        "m_try": "効率を求めすぎず、あえて「無駄な対話の時間」を確保して心の余白を。",
        "f_try": "彼の論理性は「冷たさ」ではなく、関係を整理するための武器だと捉えて。"
    },
    "B_X": {
        "title": "B×X (嵐と避難所)",
        "desc": "女性の感情から男性が逃げ、追いかける女性がさらに激昂する構造。",
        "m_try": "逃げる時は「30分頭を冷やして戻る」と宣言を。黙って去るのが最大のNG。",
        "f_try": "彼の沈黙を「拒絶」ではなく「脳のフリーズ」だと理解し、10分だけ待って。"
    },
    "B_Y": {
        "title": "B×Y (孤独のサイレンス)",
        "desc": "男性の沈黙が女性の不安を最大化させる、冷え込みの強いパターン。",
        "m_try": "言葉が見つからなくても、隣に座る、手を握る等、非言語の安心を届けて。",
        "f_try": "問い詰めすぎると彼はさらに殻に。まずは「私はあなたの味方だよ」と信号を。"
    },
    "B_Z": {
        "title": "B×Z (静かなる独裁)",
        "desc": "女性が全てを決め、男性は従うだけ。男性に不満が溜まりやすい状態。",
        "m_try": "「なんでもいい」は対話の放棄。「僕はAよりBが好きかな」と小さな自己主張を。",
        "f_try": "彼が意見を言った時は、自分の考えと違っても「教えてくれてありがとう」と肯定を。"
    },
    "B_W": {
        "title": "B×W (ゆっくりした開花)",
        "desc": "女性の忍耐強い対話で、男性が少しずつ本音を話し始める成長過程。",
        "m_try": "自分の感情を「快・不快」の2択からで良いので、少しずつシェアを。",
        "f_try": "彼の小さな成長を喜び、変化を急かさない。彼の沈黙を「思考中」と捉えて。"
    },
    "C_X": {
        "title": "C×X (砂漠の古城)",
        "desc": "形は立派ですが情緒的な交流が枯渇。女性は心の渇きを訴えています。",
        "m_try": "高価なプレゼントより、毎日「今日一番嬉しかったことは？」と聞く1分の興味を。",
        "f_try": "彼の仕事への献身を当たり前と思わず、彼なりの不器用な愛情表現だと一度肯定を。"
    },
    "C_Y": {
        "title": "C×Y (遠い城)",
        "desc": "男性は外で戦っていますが、女性は不在の孤独で壊れそうになっています。",
        "m_try": "離れていても「繋がっている」感覚を。風景写真1枚でいいので日常をシェアして。",
        "f_try": "彼の働く姿にリスペクトを。その上で「5分だけ電話したい」と控えめに要求を。"
    },
    "C_Z": {
        "title": "C×Z (共同経営者)",
        "desc": "運営は完璧ですが、夫婦としての甘い空気がなくなっている状態です。",
        "m_try": "効率を度外視して、彼女を一人の女性として扱うデートを月1回プロデュースして。",
        "f_try": "役割を脱ぎ捨てて甘える。隙を見せることが、彼の「守りたい」本能を刺激します。"
    },
    "C_W": {
        "title": "C×W (不揺の基盤)",
        "desc": "男性の安定感と女性の成熟が合致。地に足のついた強い家族になれます。",
        "m_try": "安定に甘んじず、「最近の君の心の状態はどう？」と定期的なアップデートを。",
        "f_try": "彼の安定感を称賛し、彼が安心して「弱音」を吐ける世界で唯一の場所になって。"
    },
    "D_X": {
        "title": "D×X (共鳴の輪)",
        "desc": "男性が女性の感情を包み込み、家庭内が明るいエネルギーで満たされます。",
        "m_try": "彼女の感情に同調しすぎて疲弊しないよう、意識的に自分の一人の時間も確保して。",
        "f_try": "彼の優しさを当然と思わず、「話を聴いてくれて本当に救われる」とフィードバックを。"
    },
    "D_Y": {
        "title": "D×Y (安息の地)",
        "desc": "男性の包容力が女性の不安を溶かす、最強の安心パターンです。",
        "m_try": "ハグや言葉での愛情表現をルーチンに。あなたが提供する安心が彼女を支えます。",
        "f_try": "貰うばかりではなく、彼が疲れている時は「私があなたのセキュリティになるね」と支えて。"
    },
    "D_Z": {
        "title": "D×Z (賢者の鏡)",
        "desc": "お互いを高め合えます。時に真面目すぎて遊びがなくなる点に注意。",
        "m_try": "彼女の完璧主義を和らげるため、あえて「テキトーでいいよ」と笑いを誘う緩さを。",
        "f_try": "彼のコーチングをコントロールと思わず、対等な知恵として楽しんで。たまにはダラダラと。"
    },
    "D_W": {
        "title": "D×W (黄金の調和)",
        "desc": "互いを理解し、常に最新のOSにアップデートし続けるWelfamilyの到達点。",
        "m_try": "今の幸せを維持するために、定期的に二人で「これから作りたい未来」を語り合って。",
        "f_try": "最高のパートナーである彼に感謝を。その余裕を、周囲の悩める方々への光としてお裾分けを。"
    }
}

if st.button("診断する"):
    # 3. 分析ロジック（多次元スコアリング）
    m_scores = {
        "A": m1*2 + m2*-1 + m3*1 + m4*2 + m5*-2,
        "B": m1*-1 + m2*2 + m3*0 + m4*1 + m5*-1,
        "C": m1*1 + m2*0 + m3*2 + m4*1 + m5*0,
        "D": m1*0 + m2*-2 + m3*0 + m4*-1 + m5*3
    }
    
    f_scores = {
        "X": f1*2 + f2*1 + f3*1 + f4*0 + f5*-1,
        "Y": f1*1 + f2*2 + f3*1 + f4*1 + f5*-2,
        "Z": f1*0 + f2*1 + f3*2 + f4*2 + f5*-1,
        "W": f1*1 + f2*-1 + f3*-1 + f4*-2 + f5*3
    }

    # 最大スコアを持つタイプを判定（同点の場合は標準で先のものが選ばれる）
    m_type = max(m_scores, key=m_scores.get)
    f_type = max(f_scores, key=f_scores.get)
    
    combination_key = f"{m_type}_{f_type}"
    result = results_matrix[combination_key]

    # 結果表示
    st.markdown(f"""
    <div class="result-card">
        <h2 class="type-title">{result['title']}</h2>
        <p><strong>[解説]</strong><br>{result['desc']}</p>
        <div class="try-box-m">
            <strong>🧔 [男Try]</strong><br>{result['m_try']}
        </div>
        <div class="try-box-f">
            <strong>👩 [女Try]</strong><br>{result['f_try']}
        </div>
    </div>
    """, unsafe_allow_html=True)
