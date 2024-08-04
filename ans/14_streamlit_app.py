# pip install streamlit_pandas_profiling に加えて以下も必要
# conda install -c conda-forge ydata-profiling
import streamlit as st
import pandas as pd
import ydata_profiling  # df.profile_report()を使うために必要
from streamlit_pandas_profiling import st_profile_report
import matplotlib  # 以下を除くと描画エラーが生じる

matplotlib.use("Agg")  # 以下を除くと描画エラーが生じる

st.header("`streamlit_pandas_profiling`")

df = pd.read_csv(
    "https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv"
)

pr = df.profile_report()
st_profile_report(pr)

