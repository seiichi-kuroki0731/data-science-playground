"""
python -m pip install streamlit-tags streamlit-aggrid streamlit-option-menu requests
Hugging Faceに登録してAPIキーを取得 https://huggingface.co/settings/tokens

"""

import streamlit as st
import pandas as pd
import requests

from streamlit_tags import st_tags
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import GridUpdateMode, DataReturnMode

if "widen" not in st.session_state:
    layout = "centered"
else:
    layout = "wide" if st.session_state.widen else "centered"


st.set_page_config(
    layout=layout, page_title="Zero-Shot Text Classifier", page_icon="🤗"
)


if not "valid_inputs_received" in st.session_state:
    st.session_state["valid_inputs_received"] = False


c1, c2 = st.columns([0.4, 2])
with c1:
    st.image(
        "./sample_data/logo.png",
        width=110,
    )
with c2:
    st.caption("")
    st.title("Zero-Shot Text Classifier")


st.markdown(
    """
Classify keyphrases fast and on-the-fly with this mighty app. No ML training needed!  
Create classifying labels (e.g. `Positive`, `Negative` and `Neutral`), paste your keyphrases, and you're off!  
"""
)

st.write("")


with st.form(key="my_form"):
    # hugging faceに登録して以下から取得 https://huggingface.co/settings/tokens
    API_KEY = "XXXXXXXXXXXXXX"

    API_URL = (
        "https://api-inference.huggingface.co/models/valhalla/distilbart-mnli-12-3"
    )

    headers = {"Authorization": f"Bearer {API_KEY}"}

    multiselectComponent = st_tags(
        label="",
        text="Add labels - 3 max",
        value=["Positive", "Negative", "Neutral"],
        suggestions=[
            "Informational",
            "Transactional",
            "Navigational",
            "Positive",
            "Negative",
            "Neutral",
        ],
        maxtags=3,
    )

    new_line = "\n"
    nums = [
        "I want to buy something in this store",
        "How to ask a question about a product",
        "Request a refund through the Google Play store",
        "I have a broken screen, what should I do?",
        "Can I have the link to the product?",
    ]

    sample = f"{new_line.join(map(str, nums))}"

    MAX_LINES_FULL = 50
    text = st.text_area(
        "Enter keyphrases to classify",
        sample,
        height=200,
        key="2",
        help="At least two keyphrases for the classifier to work, one per line, "
        + str(MAX_LINES_FULL)
        + " keyphrases max in 'unlocked mode'. You can tweak 'MAX_LINES_FULL' in the code to change this",
    )

    lines = text.split("\n")
    linesList = []
    for x in lines:
        linesList.append(x)
    linesList = list(dict.fromkeys(linesList))
    linesList = list(filter(None, linesList))

    if len(linesList) > MAX_LINES_FULL:
        st.info(
            "❄️ Note that only the first "
            + str(MAX_LINES_FULL)
            + " keyprases will be reviewed to preserve performance. Fork the repo and tweak 'MAX_LINES_FULL' in the code to increase that limit."
        )

        linesList = linesList[:MAX_LINES_FULL]

    submit_button = st.form_submit_button(label="Submit")

if not submit_button and not st.session_state.valid_inputs_received:
    st.stop()

elif submit_button and not text:
    st.warning("❄️ There is no keyphrases to classify")
    st.session_state.valid_inputs_received = False
    st.stop()

elif submit_button and not multiselectComponent:
    st.warning("❄️ You have not added any labels, please add some! ")
    st.session_state.valid_inputs_received = False
    st.stop()

elif submit_button and len(multiselectComponent) == 1:
    st.warning("❄️ Please make sure to add at least two labels for classification")
    st.session_state.valid_inputs_received = False
    st.stop()

elif submit_button or st.session_state.valid_inputs_received:
    try:
        if submit_button:
            st.session_state.valid_inputs_received = True

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        listToAppend = []

        for row in linesList:
            output2 = query(
                {
                    "inputs": row,
                    "parameters": {"candidate_labels": multiselectComponent},
                    "options": {"wait_for_model": True},
                }
            )

            listToAppend.append(output2)

        st.success("✅ Done!")

        df = pd.DataFrame.from_dict(listToAppend)

        st.caption("")
        st.markdown("### Check classifier results")
        st.caption("")

        st.checkbox(
            "Widen layout",
            key="widen",
            help="Tick this box to toggle the layout to 'Wide' mode",
        )

        f = [[f"{x:.2%}" for x in row] for row in df["scores"]]

        df["classification scores"] = f
        df.drop("scores", inplace=True, axis=1)

        df.rename(columns={"sequence": "keyphrase"}, inplace=True)

        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(
            enablePivot=True, enableValue=True, enableRowGroup=True
        )
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)
        gb.configure_side_bar()
        gridOptions = gb.build()

        response = AgGrid(
            df,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            height=300,
            fit_columns_on_grid_load=False,
            configure_side_bar=True,
        )

        cs, c1 = st.columns([2, 2])
        with cs:

            @st.cache_data
            def convert_df(df):
                return df.to_csv().encode("utf-8")

            csv = convert_df(df)
            st.caption("")
            st.download_button(
                label="Download results as CSV",
                data=csv,
                file_name="results.csv",
                mime="text/csv",
            )
    except ValueError as ve:
        st.warning("❄️ Please confirm that the API key is valid. ☝️")
        st.stop()
