
import streamlit as st

from utils.insights import generate_insights

st.title("Automated Insights 💡")
st.caption("Let DataLens explain what your dataset is telling you.")
st.divider()

# Use cleaned data if it belongs to the current uploaded file
if (
    "cleaned_dataset" in st.session_state
    and st.session_state.get("cleaned_filename") == st.session_state.filename
):
    df = st.session_state.cleaned_dataset
    st.caption("Analyzing: Cleaned Dataset")
else:
    df = st.session_state.dataset
    st.caption("Analyzing: Original Dataset")

if df is None:
    st.warning("Please upload a CSV dataset first.")
    st.stop()

if df.empty:
    st.warning("Your dataset has no rows to analyze.")
    st.stop()

# Generate insights
insights = generate_insights(df)

# Summary metrics
st.subheader("Dataset at a Glance")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", f"{df.shape[0]:,}")
col2.metric("Columns", f"{df.shape[1]:,}")
col3.metric(
    "Missing Values",
    f"{int(df.isnull().sum().sum()):,}"
)
col4.metric(
    "Duplicate Rows",
    f"{int(df.duplicated().sum()):,}"
)

st.divider()

# Overview insights
st.subheader("📌 General Observations")

for insight in insights["overview"]:
    st.markdown(f"- {insight}")

st.divider()

# Numerical insights
st.subheader("🔢 Numerical Insights")

if insights["numerical"]:
    for insight in insights["numerical"]:
        st.markdown(f"- {insight}")
else:
    st.info("No numerical columns found in this dataset.")

st.divider()

# Categorical insights
st.subheader("🏷️ Categorical Insights")

if insights["categorical"]:
    for insight in insights["categorical"]:
        st.markdown(f"- {insight}")
else:
    st.info("No categorical columns found in this dataset.")

st.divider()

# Relationship insights
st.subheader("🔗 Relationships")

for insight in insights["relationships"]:
    st.markdown(f"- {insight}")

st.divider()

st.caption(
    "Insights are generated from statistical patterns in your data. "
    "They are observations, not proof of cause and effect."
)
