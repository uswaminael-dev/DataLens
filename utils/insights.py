
def generate_insights(df):
    insights = {
        "overview": [],
        "numerical": [],
        "categorical": [],
        "relationships": []
    }

    rows, columns = df.shape

    # 1. GENERAL DATASET INSIGHTS
    insights["overview"].append(
        f"Your dataset contains {rows:,} rows and {columns:,} columns."
    )

    total_missing = int(df.isnull().sum().sum())
    total_cells = rows * columns

    if total_cells > 0:
        missing_percentage = (total_missing / total_cells) * 100
    else:
        missing_percentage = 0

    insights["overview"].append(
        f"There are {total_missing:,} missing values "
        f"({missing_percentage:.2f}% of all cells)."
    )

    duplicate_count = int(df.duplicated().sum())

    insights["overview"].append(
        f"Your dataset contains {duplicate_count:,} duplicate rows."
    )

    # 2. NUMERICAL INSIGHTS
    numeric_columns = df.select_dtypes(include="number").columns

    for column in numeric_columns:
        values = df[column].dropna()

        if values.empty:
            insights["numerical"].append(
                f"{column} has no available numerical values."
            )
            continue

        mean_value = values.mean()
        median_value = values.median()
        minimum = values.min()
        maximum = values.max()

        insights["numerical"].append(
            f"{column}: Average = {mean_value:.2f}, "
            f"Median = {median_value:.2f}, "
            f"Minimum = {minimum:.2f}, "
            f"Maximum = {maximum:.2f}."
        )

        # Potential outlier count using IQR
        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outlier_count = int(
            ((values < lower_bound) | (values > upper_bound)).sum()
        )

        insights["numerical"].append(
            f"{column}: {outlier_count} potential outlier(s) "
            f"detected using the IQR method."
        )

    # 3. CATEGORICAL INSIGHTS
    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns

    for column in categorical_columns:
        values = df[column].dropna()

        if values.empty:
            insights["categorical"].append(
                f"{column} has no available category values."
            )
            continue

        unique_count = values.nunique()
        most_common = values.mode().iloc[0]
        most_common_count = int((values == most_common).sum())

        insights["categorical"].append(
            f"{column}: Contains {unique_count} unique categories. "
            f"The most frequent value is '{most_common}', "
            f"appearing {most_common_count} time(s)."
        )

    # 4. CORRELATION INSIGHTS
    if len(numeric_columns) >= 2:
        correlation = df[numeric_columns].corr()

        strongest_pair = None
        strongest_value = 0

        for i in range(len(numeric_columns)):
            for j in range(i + 1, len(numeric_columns)):
                value = correlation.iloc[i, j]

                if value == value and abs(value) > abs(strongest_value):
                    strongest_value = value
                    strongest_pair = (
                        numeric_columns[i],
                        numeric_columns[j]
                    )

        if strongest_pair is not None:
            first_column, second_column = strongest_pair

            insights["relationships"].append(
                f"The strongest linear correlation among numerical "
                f"columns is between {first_column} and {second_column}: "
                f"{strongest_value:.2f}."
            )
        else:
            insights["relationships"].append(
                "No usable numerical correlations could be calculated."
            )
    else:
        insights["relationships"].append(
            "At least two numerical columns are needed to analyze correlations."
        )

    return insights
