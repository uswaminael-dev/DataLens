# DataLens — Dataset Intelligence Studio

**Explore. Understand. Improve.**

DataLens is an interactive dataset analysis application built with Python and Streamlit. It helps users upload CSV files, explore data, identify quality issues, visualize patterns, generate automated insights, and export analysis results.

## Features

### Dataset Exploration
- Upload CSV datasets.
- View dataset dimensions and previews.
- Inspect column names and data types.
- Explore numerical and categorical summaries.

### Data Quality & Cleaning
- Detect missing values.
- Identify duplicate records.
- Detect potential numerical outliers using the IQR method.
- Handle missing values using median or mode imputation.
- Remove duplicate rows and selected outliers.
- Preserve the original uploaded dataset.

### Visual Analytics
- Interactive histograms.
- Box plots.
- Categorical bar charts.
- Numerical scatter plots.
- Correlation heatmaps.

### Automated Insights
- Dataset overview and completeness statistics.
- Numerical summaries.
- Categorical observations.
- Potential outlier counts.
- Numerical correlation observations.

### Export Studio
- Download original and cleaned CSV datasets.
- Export missing-value reports.
- Export outlier reports.
- Download automated insights as a text report.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| Pandas | Data processing and analysis |
| NumPy | Numerical computing |
| Plotly | Interactive visualizations |
| Git & GitHub | Version control and source hosting |

## Project Structure

```text
DataLens/
├── app.py
├── pages/
│   ├── overview.py
│   ├── data_explorer.py
│   ├── data_quality.py
│   ├── visual_analytics.py
│   ├── insights.py
│   └── export.py
├── utils/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── profiling.py
│   ├── cleaning.py
│   ├── visualizations.py
│   └── insights.py
├── assets/
├── data/
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/DataLens.git
cd DataLens
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## Live Demo

Add your deployed Streamlit Community Cloud URL here once deployment is complete.

## Future Improvements

- Advanced data cleaning recommendations.
- More visualization options.
- Downloadable PDF analysis reports.
- More advanced statistical insights.
- Support for additional file formats.

## Learning Outcomes

This project explores practical applications of Python, data manipulation, exploratory data analysis, data visualization, Streamlit development, modular programming, and version control.

---

**Built as a hands-on Data Science project.**