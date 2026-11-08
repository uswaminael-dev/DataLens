
import pandas as pd


def get_missing_values(df):
    missing_count = df.isnull().sum()

    missing_percentage = (
        missing_count / len(df) * 100
        if len(df) > 0
        else missing_count * 0
    )

    summary = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": missing_count.values,
        "Missing Percentage": missing_percentage.values
    })

    summary = summary[summary["Missing Values"] > 0]

    return summary.sort_values(
        by="Missing Values",
        ascending=False
    )


def get_duplicate_rows(df):
    duplicates = df[df.duplicated(keep=False)]

    duplicate_count = int(df.duplicated().sum())

    return duplicate_count, duplicates


def get_outliers(df):
    numeric_columns = df.select_dtypes(include="number").columns

    results = []

    for column in numeric_columns:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outlier_count = (
            (df[column] < lower_bound) |
            (df[column] > upper_bound)
        ).sum()

        results.append({
            "Column": column,
            "Outlier Count": int(outlier_count),
            "Lower Bound": round(lower_bound, 2),
            "Upper Bound": round(upper_bound, 2)
        })

    return pd.DataFrame(results)


def get_data_types(df):
    results = []

    for column in df.columns:
        dtype = str(df[column].dtype)

        if pd.api.types.is_numeric_dtype(df[column]):
            category = "Numerical"
        elif pd.api.types.is_string_dtype(df[column]) or df[column].dtype == "object":
            category = "Categorical / Text"
        else:
            category = "Other"

        results.append({
            "Column": column,
            "Data Type": dtype,
            "Category": category
        })

    return pd.DataFrame(results)
