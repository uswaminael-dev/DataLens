
import streamlit as st
import plotly.express as px

st.title("Visual Analytics 📊")
st.caption("Discover patterns, distributions and relationships in your data.")
st.divider()

# Use cleaned data if it belongs to the currently uploaded file
if (
    "cleaned_dataset" in st.session_state
    and st.session_state.get("cleaned_filename") == st.session_state.filename
):
    df = st.session_state.cleaned_dataset
    st.caption("Currently visualizing: Cleaned Dataset")
else:
    df = st.session_state.dataset
    st.caption("Currently visualizing: Original Dataset")

if df is None:
    st.warning("Please upload a CSV dataset first.")
    st.stop()

if df.empty:
    st.warning("Your dataset has no rows to visualize.")
    st.stop()

chart_type = st.selectbox(
    "Choose a visualization",
    [
        "Histogram",
        "Box Plot",
        "Bar Chart",
        "Scatter Plot",
        "Correlation Heatmap"
    ]
)

numeric_columns = df.select_dtypes(include="number").columns.tolist()

categorical_columns = df.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()


# 1. HISTOGRAM
if chart_type == "Histogram":
    st.subheader("Distribution of a Numerical Column")

    if numeric_columns:
        selected_column = st.selectbox(
            "Choose a numerical column",
            numeric_columns
        )

        fig = px.histogram(
            df,
            x=selected_column,
            nbins=30,
            title=f"Distribution of {selected_column}"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write(
            "A histogram shows how frequently values fall into "
            "different numerical ranges."
        )
    else:
        st.info("No numerical columns available.")


# 2. BOX PLOT
elif chart_type == "Box Plot":
    st.subheader("Numerical Spread and Potential Outliers")

    if numeric_columns:
        selected_column = st.selectbox(
            "Choose a numerical column",
            numeric_columns
        )

        fig = px.box(
            df,
            y=selected_column,
            title=f"Box Plot of {selected_column}",
            points="outliers"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write(
            "A box plot displays the median, quartiles, spread "
            "and potential outliers."
        )
    else:
        st.info("No numerical columns available.")


# 3. BAR CHART
elif chart_type == "Bar Chart":
    st.subheader("Frequency of Categories")

    if categorical_columns:
        selected_column = st.selectbox(
            "Choose a categorical column",
            categorical_columns
        )

        value_counts = (
            df[selected_column]
            .fillna("Missing")
            .astype(str)
            .value_counts()
            .head(15)
            .reset_index()
        )

        value_counts.columns = ["Category", "Count"]

        fig = px.bar(
            value_counts,
            x="Category",
            y="Count",
            title=f"Category Counts in {selected_column}"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write(
            "A bar chart compares how frequently different "
            "categories appear."
        )
    else:
        st.info("No categorical columns available.")


# 4. SCATTER PLOT
elif chart_type == "Scatter Plot":
    st.subheader("Relationship Between Two Numerical Columns")

    if len(numeric_columns) >= 2:
        col1, col2 = st.columns(2)

        with col1:
            x_column = st.selectbox(
                "Choose X-axis",
                numeric_columns,
                index=0
            )

        with col2:
            y_column = st.selectbox(
                "Choose Y-axis",
                numeric_columns,
                index=1
            )

        fig = px.scatter(
            df,
            x=x_column,
            y=y_column,
            title=f"{x_column} vs {y_column}"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write(
            "A scatter plot helps identify relationships, "
            "clusters and unusual observations."
        )
    else:
        st.info("You need at least two numerical columns.")


# 5. CORRELATION HEATMAP
elif chart_type == "Correlation Heatmap":
    st.subheader("Correlation Between Numerical Columns")

    if len(numeric_columns) >= 2:
        correlation = df[numeric_columns].corr()

        fig = px.imshow(
            correlation,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu",
            zmin=-1,
            zmax=1,
            title="Correlation Heatmap"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write(
            "Correlation ranges from -1 to +1. Positive values "
            "indicate variables tend to move together, while "
            "negative values indicate they tend to move in "
            "opposite directions. Correlation does not prove causation."
        )
    else:
        st.info("You need at least two numerical columns.")
