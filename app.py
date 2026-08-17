import streamlit as st
import google.generativeai as genai

# APIキーの設定
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def generate_article(asin_a, obs_a, unconf_a, asin_b, obs_b, unconf_b):
    official_info_a = f"商品A（ASIN: {asin_a}）の公式情報"
    official_info_b = f"商品B（ASIN: {asin_b}）の公式情報"

    prompt = f"""
    あなたは商品比較記事の編集者です。
    以下の資料だけを使い、商品Aと商品Bの比較記事を作ってください。
    
    【目的】
    2商品で迷っている読者が、自分の使い方に合う方を選べる状態にする。
    
    【絶対ルール】
    資料にない仕様や使用感を補わない
    書き手が体験していないことを体験談にしない
    未確認の内容は「未確認」と表示する
    Amazonのカスタマーレビューを根拠にしない
    公式情報と書き手の観察を区別する
    優劣を決めつけず、利用場面ごとに向く商品を分ける
    価格は固定せず、購入時の確認を促す
    「必ず」「絶対」「最強」など根拠のない表現を使わない
    
    【商品A】
    商品名と公式情報：{official_info_a}
    実際に観察したこと：{obs_a}
    未確認のこと：{unconf_a}
    
    【商品B】
    商品名と公式情報：{official_info_b}
    実際に観察したこと：{obs_b}
    未確認のこと：{unconf_b}
    
    【記事構成】
    30秒で分かる結論
    2商品の大きな違い
    商品Aが向く人
    商品Bが向く人
    実際に確認した注意点
    購入前の最終チェック
    最後に、事実確認が必要な文章と、記事に書かなかった未確認情報を一覧にしてください。
    """

    # モデルの呼び出し（安定版）
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text

# --- UI構築 ---
st.set_page_config(page_title="商品比較記事ジェネレーター", layout="wide")
st.title("🛍️ 商品比較記事ジェネレーター")

col1, col2 = st.columns(2)

with col1:
    st.subheader("商品A")
    asin_a = st.text_input("ASIN (商品A)")
    obs_a = st.text_area("実際に観察したこと", key="obs_a")
    unconf_a = st.text_area("未確認のこと", key="unconf_a")

with col2:
    st.subheader("商品B")
    asin_b = st.text_input("ASIN (商品B)")
    obs_b = st.text_area("実際に観察したこと", key="obs_b")
    unconf_b = st.text_area("未確認のこと", key="unconf_b")

st.divider()

if st.button("記事を生成する", type="primary", use_container_width=True):
    if not asin_a or not asin_b:
        st.error("ASINを入力してください。")
    else:
        with st.spinner("Geminiが記事を執筆しています..."):
            try:
                result_markdown = generate_article(
                    asin_a, obs_a, unconf_a, 
                    asin_b, obs_b, unconf_b
                )
                st.success("生成完了！右上のアイコンからコピーできます。")
                st.code(result_markdown, language="markdown")
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
