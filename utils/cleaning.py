
import pandas as pd


def remove_duplicates(df):
    return df.drop_duplicates().copy()


def handle_missing_values(df, strategy):
    cleaned_df = df.copy()

    if strategy == "Drop rows":
        cleaned_df = cleaned_df.dropna()

    elif strategy == "Fill missing values":
        for column in cleaned_df.columns:

            if pd.api.types.is_numeric_dtype(cleaned_df[column]):
                median_value = cleaned_df[column].median()

                if pd.notna(median_value):
                    cleaned_df[column] = cleaned_df[column].fillna(
                        median_value
                    )

            else:
                mode_values = cleaned_df[column].mode()

                if not mode_values.empty:
                    cleaned_df[column] = cleaned_df[column].fillna(
                        mode_values[0]
                    )

    return cleaned_df



def remove_outliers(df, column):
    cleaned_df = df.copy()

    q1 = cleaned_df[column].quantile(0.25)
    q3 = cleaned_df[column].quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Keep missing values; remove only actual outliers
    valid_rows = (
        cleaned_df[column].isna() |
        (
            (cleaned_df[column] >= lower_bound) &
            (cleaned_df[column] <= upper_bound)
        )
    )

    return cleaned_df[valid_rows].copy()
