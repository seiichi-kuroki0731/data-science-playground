"""
Bored APIは利用できなくなっているので、代わりにJokeAPIを使用
"""

import streamlit as st
import requests

st.title("🎭 Random Joke Generator")

st.sidebar.header("選択肢")
joke_type = st.sidebar.selectbox(
    "ジョークのタイプ",
    ["Any", "Programming", "Misc", "Dark", "Pun", "Spooky", "Christmas"],
)

# Random Joke APIのエンドポイント
api_url = "https://v2.jokeapi.dev/joke/" + joke_type
# if joke_type != "Any":
#    api_url += joke_type

# APIリクエストを送信
response = requests.get(api_url)

# レスポンスのステータスコードを確認
if response.status_code == 200:
    joke_data = response.json()
else:
    st.error(f"Error: Unable to fetch joke. Status code: {response.status_code}")
    st.stop()


c1, c2 = st.columns(2)
with c1:
    with st.expander("About this app"):
        st.write(
            "Need a laugh? The **Random Joke Generator** provides jokes based on the category you choose. This app is powered by the JokeAPI."
        )
with c2:
    with st.expander("JSON data"):
        st.write(joke_data)

st.header("Here's your joke:")
if joke_data["type"] == "single":
    st.info(joke_data["joke"])
else:
    st.info(joke_data["setup"])
    st.success(joke_data["delivery"])

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="Category",
        value=joke_data["category"],
        delta="",
    )
with col2:
    st.metric(
        label="Type",
        value=joke_data["type"].capitalize(),
        delta="",
    )
with col3:
    st.metric(
        label="ID",
        value=joke_data["id"],
        delta="",
    )

if st.button("Get Another Joke"):
    st.rerun()
