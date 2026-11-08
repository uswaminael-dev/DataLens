
import streamlit as st
import hashlib
from utils.data_loader import load_csv


# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="DataLens | Dataset Intelligence",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)



st.markdown("""
<style>

/* ---------- BRAND IDENTITY ---------- */

.brand-lockup {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 2px 22px 2px;
}

.brand-icon {
    width: 43px;
    height: 43px;
    border-radius: 12px;
    background: #72C7B8;
    color: #0B1220;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 23px;
    font-weight: 800;
}

.brand-name {
    color: #F0F4F8;
    font-size: 22px;
    font-weight: 750;
    letter-spacing: -0.8px;
}

.brand-subtitle {
    color: #8FA3B8;
    font-size: 9px;
    letter-spacing: 1.5px;
    margin-top: 3px;
}

<style>

/* ---------- GLOBAL APP ---------- */

.stApp {
    background: #0B1220;
}

.block-container {
    max-width: 1450px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
}

/* ---------- TYPOGRAPHY ---------- */

html, body, [class*="css"] {
    font-family: "Segoe UI", sans-serif;
}

h1 {
    font-size: 2.15rem !important;
    font-weight: 700 !important;
    letter-spacing: -1px;
    color: #F0F4F8;
}

h2 {
    font-size: 1.45rem !important;
    font-weight: 650 !important;
    color: #E8EDF3;
}

h3 {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: #DCE5EE;
}

p, label {
    color: #B6C3D2;
}

/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background: #101A2A;
    border-right: 1px solid #253348;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #AAB8C8;
}

/* ---------- METRIC CARDS ---------- */

div[data-testid="stMetric"] {
    background: #121C2D;
    border: 1px solid #25364B;
    padding: 19px;
    border-radius: 14px;
    transition: border-color 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    border-color: #72C7B8;
}

div[data-testid="stMetricLabel"] {
    color: #AAB8C8;
    font-size: 0.88rem;
}

div[data-testid="stMetricValue"] {
    color: #F0F4F8;
    font-weight: 700;
}

/* ---------- BUTTONS ---------- */

.stButton > button,
.stDownloadButton > button {
    border-radius: 9px;
    min-height: 42px;
    font-weight: 600;
    border: 1px solid #345064;
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #72C7B8;
    color: #72C7B8;
}

/* ---------- INPUTS ---------- */

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #121C2D;
    border-color: #304157;
    border-radius: 9px;
}

.stTextInput input,
.stNumberInput input {
    background: #121C2D;
}

/* ---------- TABS ---------- */

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid #25364B;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    padding: 10px 17px;
    color: #AAB8C8;
}

.stTabs [aria-selected="true"] {
    color: #72C7B8 !important;
}

/* ---------- DATAFRAMES ---------- */

div[data-testid="stDataFrame"] {
    border: 1px solid #25364B;
    border-radius: 12px;
    overflow: hidden;
}

/* ---------- FILE UPLOADER ---------- */

div[data-testid="stFileUploader"] {
    background: #121C2D;
    border: 1px dashed #3B5268;
    border-radius: 12px;
    padding: 10px;
}

/* ---------- DIVIDERS ---------- */

hr {
    border-color: #253348;
}

/* ---------- ALERTS ---------- */

div[data-testid="stAlert"] {
    border-radius: 11px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------

if "dataset" not in st.session_state:
    st.session_state.dataset = None

if "filename" not in st.session_state:
    st.session_state.filename = None


# ---------------------------------
# SIDEBAR BRANDING
# ---------------------------------

with st.sidebar:

    
    st.markdown("""
    <div class="brand-lockup">
        <div class="brand-icon">D</div>
        <div>
            <div class="brand-name">DataLens</div>
            <div class="brand-subtitle">DATA INTELLIGENCE STUDIO</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


    st.divider()

    st.write("Explore. Understand. Improve.")

    st.divider()

    st.subheader("Dataset Upload")

    uploaded_file = st.file_uploader(
        "Upload your CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            
            file_bytes = uploaded_file.getvalue()

            # Create a unique fingerprint for the uploaded file
            file_signature = hashlib.sha256(file_bytes).hexdigest()

            # Reset cleaning state only when the uploaded content changes
            if st.session_state.get("dataset_signature") != file_signature:
                st.session_state.cleaned_dataset = None
                st.session_state.cleaned_filename = None
                st.session_state.dataset_signature = file_signature

            df = load_csv(file_bytes)


            if df.empty:

                st.error("The dataset is empty.")

                st.session_state.dataset = None
                st.session_state.filename = None

            else:

                st.session_state.dataset = df
                st.session_state.filename = uploaded_file.name
                st.session_state.dataset_signature = None
                st.success("Dataset loaded!")

        except Exception as e:

            st.error(f"CSV loading error: {e}")

            st.session_state.dataset = None
            st.session_state.filename = None
            st.session_state.dataset_signature = None

    else:

        st.session_state.dataset = None
        st.session_state.filename = None
        

    st.divider()

    st.caption("Built with Python and Streamlit")


# ---------------------------------
# PAGE NAVIGATION
# ---------------------------------

pages = {

    "WORKSPACE": [

        st.Page(
            "pages/overview.py",
            title="Overview",
            icon="🏠",
            default=True
        ),

        st.Page(
            "pages/data_explorer.py",
            title="Data Explorer",
            icon="🔎"
        ),

        st.Page(
            "pages/data_quality.py",
            title="Data Quality",
            icon="🛡️"
        ),

    ],

    "ANALYSIS": [

        st.Page(
            "pages/visual_analytics.py",
            title="Visual Analytics",
            icon="📊"
        ),

        st.Page(
            "pages/insights.py",
            title="Insights",
            icon="💡"
        ),

    ],

    "EXPORT": [

        st.Page(
            "pages/export.py",
            title="Export",
            icon="📥"
        ),

    ]

}


pg = st.navigation(pages)

pg.run()
