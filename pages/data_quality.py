
import streamlit as st

from utils.profiling import (
    get_missing_values,
    get_duplicate_rows,
    get_outliers,
    get_data_types
)


from utils.cleaning import (
    remove_duplicates,
    handle_missing_values,
    remove_outliers
)


st.title("Data Quality Intelligence 🛡️")
st.caption("Discover missing values, duplicates, outliers and data types.")
st.divider()

df = st.session_state.dataset

if df is None:
    st.warning("Please upload a CSV dataset first.")
    st.stop()
    

# Maintain a separate cleaned copy of the original dataset
if st.session_state.get("cleaned_filename") != st.session_state.filename:
    st.session_state.cleaned_dataset = df.copy()
    st.session_state.cleaned_filename = st.session_state.filename


# Generate data quality reports
missing_report = get_missing_values(df)
duplicate_count, duplicate_rows = get_duplicate_rows(df)
outlier_report = get_outliers(df)
data_type_report = get_data_types(df)

# Summary metrics
col1, col2, col3 = st.columns(3)

col1.metric(
    "Missing Values",
    int(df.isnull().sum().sum())
)

col2.metric(
    "Duplicate Rows",
    duplicate_count
)

col3.metric(
    "Columns with Outliers",
    int((outlier_report["Outlier Count"] > 0).sum())
    if not outlier_report.empty else 0
)

st.divider()

# Analysis sections
missing_tab, duplicate_tab, outlier_tab, datatype_tab = st.tabs([
    "Missing Values",
    "Duplicates",
    "Outliers",
    "Data Types"
])

with missing_tab:
    st.subheader("Missing Values Analysis")

    if missing_report.empty:
        st.success("Great! No missing values found.")
    else:
        st.dataframe(
            missing_report,
            use_container_width=True,
            hide_index=True
        )

with duplicate_tab:
    st.subheader("Duplicate Records")

    if duplicate_count == 0:
        st.success("No duplicate rows found.")
    else:
        st.warning(f"Found {duplicate_count} duplicate row(s).")

        st.dataframe(
            duplicate_rows,
            use_container_width=True,
            hide_index=True
        )

with outlier_tab:
    st.subheader("Outlier Detection")

    if outlier_report.empty:
        st.info("No numerical columns available for outlier analysis.")
    else:
        st.dataframe(
            outlier_report,
            use_container_width=True,
            hide_index=True
        )

with datatype_tab:
    st.subheader("Column Data Types")

    st.dataframe(
        data_type_report,
        use_container_width=True,
        hide_index=True
    )


st.divider()

st.header("Data Cleaning Workspace 🧹")
st.caption("Apply cleaning operations to a separate copy of your dataset.")

cleaned_df = st.session_state.cleaned_dataset

# Current cleaning status
col1, col2, col3 = st.columns(3)

col1.metric("Original Rows", len(df))
col2.metric("Cleaned Rows", len(cleaned_df))
col3.metric(
    "Rows Removed",
    len(df) - len(cleaned_df)
)

st.subheader("1. Remove Duplicate Rows")

st.write(
    f"Current duplicate rows: {int(cleaned_df.duplicated().sum())}"
)

if st.button("Remove Duplicates"):
    st.session_state.cleaned_dataset = remove_duplicates(cleaned_df)
    st.success("Duplicate rows removed!")
    st.rerun()


st.divider()

st.subheader("2. Handle Missing Values")

missing_count = int(cleaned_df.isnull().sum().sum())

st.write(f"Current missing values: {missing_count}")

missing_strategy = st.selectbox(
    "Choose a cleaning strategy",
    ["Drop rows", "Fill missing values"]
)

if st.button("Apply Missing Value Strategy"):
    st.session_state.cleaned_dataset = handle_missing_values(
        cleaned_df,
        missing_strategy
    )

    st.success("Missing value strategy applied!")
    st.rerun()


st.divider()

st.subheader("3. Remove Outliers")

numeric_columns = cleaned_df.select_dtypes(
    include="number"
).columns.tolist()

if numeric_columns:
    selected_outlier_column = st.selectbox(
        "Choose a numerical column",
        numeric_columns,
        key="cleaning_outlier_column"
    )

    if st.button("Remove Outliers"):
        st.session_state.cleaned_dataset = remove_outliers(
            cleaned_df,
            selected_outlier_column
        )

        st.success(
            f"Outliers removed from {selected_outlier_column}!"
        )
        st.rerun()

else:
    st.info("No numerical columns available for outlier removal.")


st.divider()

st.subheader("4. Cleaned Dataset Preview")

cleaned_df = st.session_state.cleaned_dataset

st.write("Current cleaned dataset:")
st.dataframe(
    cleaned_df,
    use_container_width=True,
    hide_index=True
)

if st.button("Reset to Original Dataset"):
    st.session_state.cleaned_dataset = df.copy()
    st.success("Dataset restored to its original state.")
    st.rerun()
