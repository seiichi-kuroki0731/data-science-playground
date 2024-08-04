import streamlit as st

st.header("st.multiselect")

options = st.multiselect(
    "What are your favorite colors",
    ["Green", "Yellow", "Red", "Blue"],  # 選択肢
    ["Yellow", "Red"],  # デフォルトで選択されているもの
)

st.write("You selected:", options)
