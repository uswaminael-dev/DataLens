
import streamlit as st

from utils.profiling import (
    get_missing_values,
    get_duplicate_rows,
    get_outliers
)

from utils.insights import generate_insights

st.title("Export Studio 📥")
st.caption("Download your datasets and analysis reports.")
st.divider()

original_df = st.session_state.dataset

if original_df is None:
    st.warning("Please upload a CSV dataset first.")
    st.stop()

# Select the current cleaned version, if available
if (
    "cleaned_dataset" in st.session_state
    and st.session_state.get("cleaned_filename") == st.session_state.filename
):
    cleaned_df = st.session_state.cleaned_dataset
    st.caption("Your cleaned dataset is ready to export.")
else:
    cleaned_df = original_df.copy()
    st.caption("No cleaned version found. Using the original dataset.")

filename = st.session_state.filename.rsplit(".", 1)[0]

st.subheader("Dataset Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Original Rows", len(original_df))
col2.metric("Current Rows", len(cleaned_df))
col3.metric(
    "Rows Removed",
    len(original_df) - len(cleaned_df)
)

st.divider()

# 1. DATASET DOWNLOADS
st.subheader("1. Dataset Downloads")

st.write("Download your original or cleaned dataset.")

col1, col2 = st.columns(2)

with col1:
    st.download_button(
        label="Download Original Dataset",
        data=original_df.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"{filename}_original.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    st.download_button(
        label="Download Cleaned Dataset",
        data=cleaned_df.to_csv(index=False).encode("utf-8-sig"),
        file_name=f"{filename}_cleaned.csv",
        mime="text/csv",
        use_container_width=True
    )

st.divider()

# 2. MISSING VALUES REPORT
st.subheader("2. Missing Values Report")

missing_report = get_missing_values(cleaned_df)

if missing_report.empty:
    st.success("No missing values found in the current dataset.")
else:
    st.dataframe(
        missing_report,
        use_container_width=True,
        hide_index=True
    )

st.download_button(
    label="Download Missing Values Report",
    data=missing_report.to_csv(index=False).encode("utf-8-sig"),
    file_name=f"{filename}_missing_values.csv",
    mime="text/csv"
)

st.divider()

# 3. OUTLIER REPORT
st.subheader("3. Outlier Report")

outlier_report = get_outliers(cleaned_df)

if outlier_report.empty:
    st.info("No numerical columns available for outlier analysis.")
else:
    st.dataframe(
        outlier_report,
        use_container_width=True,
        hide_index=True
    )

st.download_button(
    label="Download Outlier Report",
    data=outlier_report.to_csv(index=False).encode("utf-8-sig"),
    file_name=f"{filename}_outliers.csv",
    mime="text/csv"
)

st.divider()

# 4. AUTOMATED INSIGHTS REPORT
st.subheader("4. Automated Insights Report")

if cleaned_df.empty:
    st.warning("The cleaned dataset is empty. Insights cannot be generated.")
else:
    insights = generate_insights(cleaned_df)

    report_text = "DATALENS - DATASET INTELLIGENCE REPORT\n"
    report_text += "=" * 45 + "\n\n"

    report_text += "GENERAL OBSERVATIONS\n"
    report_text += "-" * 25 + "\n"

    for item in insights["overview"]:
        report_text += f"- {item}\n"

    report_text += "\nNUMERICAL INSIGHTS\n"
    report_text += "-" * 25 + "\n"

    for item in insights["numerical"]:
        report_text += f"- {item}\n"

    report_text += "\nCATEGORICAL INSIGHTS\n"
    report_text += "-" * 25 + "\n"

    for item in insights["categorical"]:
        report_text += f"- {item}\n"

    report_text += "\nRELATIONSHIP INSIGHTS\n"
    report_text += "-" * 25 + "\n"

    for item in insights["relationships"]:
        report_text += f"- {item}\n"

    st.download_button(
        label="Download Insights Report",
        data=report_text.encode("utf-8"),
        file_name=f"{filename}_insights.txt",
        mime="text/plain"
    )

st.divider()

st.caption(
    "DataLens | Dataset Intelligence Studio"
)
