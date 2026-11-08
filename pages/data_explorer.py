
import streamlit as st


st.title("Data Explorer 🔎")

st.caption("Explore your dataset and inspect individual records.")

st.divider()


df = st.session_state.dataset


if df is None:

    st.warning("Please upload a CSV dataset first.")

    st.stop()


# ---------------------------------
# DATASET INFORMATION
# ---------------------------------

st.subheader("Dataset Information")

st.write("File:", st.session_state.filename)

st.write("Dimensions:", df.shape)


# ---------------------------------
# ROW SELECTION
# ---------------------------------

st.subheader("Explore Records")

number_of_rows = st.slider(
    "Number of rows to display",
    min_value=1,
    max_value=max(1, len(df)),
    value=min(10, len(df))
)

st.dataframe(
    df.head(number_of_rows),
    use_container_width=True
)


# ---------------------------------
# COLUMN SELECTION
# ---------------------------------

st.subheader("Inspect a Column")

selected_column = st.selectbox(
    "Choose a column",
    df.columns.tolist()
)

st.write("Column Name:", selected_column)

st.write("Data Type:", str(df[selected_column].dtype))

st.write("Missing Values:", int(df[selected_column].isnull().sum()))

st.write("Unique Values:", int(df[selected_column].nunique()))

st.subheader("Column Statistics")

st.write(df[selected_column].describe())
