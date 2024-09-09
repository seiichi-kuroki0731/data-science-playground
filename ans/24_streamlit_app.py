import streamlit as st
import numpy as np
import pandas as pd
from time import time

st.title(
    "st.cache_data、初回は遅いがリロードすると2回目以降はcacheを利用したほうが速い"
)

# Using cache
# st.subheader("Using st.cache")
# st.cacheは非推奨となり、st.cache_dataに変更された
a0 = time()
st.subheader("Using st.cache_data")


@st.cache_data
def load_data_a():
    df = pd.DataFrame(np.random.rand(1000000, 5), columns=["a", "b", "c", "d", "e"])
    return df


st.write(load_data_a())
a1 = time()
st.info(a1 - a0)


# Not using cache
b0 = time()
st.subheader("Not using st.cache_data")


def load_data_b():
    df = pd.DataFrame(np.random.rand(1000000, 5), columns=["a", "b", "c", "d", "e"])
    return df


st.write(load_data_b())
b1 = time()
st.info(b1 - b0)
