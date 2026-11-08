
import pandas as pd
import streamlit as st
from io import BytesIO


@st.cache_data
def load_csv(file_bytes):

    df = pd.read_csv(BytesIO(file_bytes))

    return df
