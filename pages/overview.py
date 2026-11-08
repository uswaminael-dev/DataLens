
import streamlit as st
import plotly.express as px

st.title("Your Data Workspace")
st.caption(
    "Explore your datasets, discover patterns, "
    "and turn raw data into meaningful insights."
)
st.divider()

if st.session_state.dataset is None:
    st.markdown("## Welcome to DataLens")
    st.write(
        "Your workspace is ready. Upload a CSV file from the "
        "sidebar to begin exploring your data."
    )
    st.info("Start by uploading a dataset using the sidebar.")
    st.stop()

# Select the cleaned dataset when available
if (
    st.session_state.get("cleaned_dataset") is not None
    and st.session_state.get("cleaned_filename") == st.session_state.filename
):
    df = st.session_state.cleaned_dataset
    dataset_status = "Cleaned dataset"
else:
    df = st.session_state.dataset
    dataset_status = "Original dataset"

st.markdown(f"### {st.session_state.filename}")
st.caption(f"Workspace view: {dataset_status}")

# Main metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", f"{len(df):,}")
col2.metric("Total Columns", f"{len(df.columns):,}")
col3.metric("Missing Values", f"{int(df.isnull().sum().sum()):,}")
col4.metric("Duplicate Rows", f"{int(df.duplicated().sum()):,}")

st.divider()

# Dataset preview
left, right = st.columns([1.6, 1])

with left:
    st.subheader("Dataset Preview")
    st.dataframe(
        df.head(8),
        use_container_width=True,
        hide_index=True
    )

with right:
    st.subheader("Column Overview")

    column_info = df.dtypes.astype(str).reset_index()
    column_info.columns = ["Column", "Data Type"]

    st.dataframe(
        column_info,
        use_container_width=True,
        hide_index=True,
        height=310
    )

st.divider()

# Missing values visualization
st.subheader("Data Completeness")

missing_counts = df.isnull().sum()
missing_counts = missing_counts[missing_counts > 0]

if missing_counts.empty:
    st.success("Your current dataset has no missing values.")
else:
    missing_chart = missing_counts.reset_index()
    missing_chart.columns = ["Column", "Missing Values"]

    fig = px.bar(
        missing_chart,
        x="Column",
        y="Missing Values",
        title="Missing Values by Column"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Explore Your Workspace")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Data Explorer**")
    st.caption("Inspect records and individual columns.")

with col2:
    st.markdown("**Data Quality**")
    st.caption("Identify and clean data issues.")

with col3:
    st.markdown("**Visual Analytics**")
    st.caption("Discover patterns through interactive charts.")
