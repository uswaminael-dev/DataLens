
import streamlit as st
import hashlib

from utils.data_loader import load_csv


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="DataLens | Dataset Intelligence",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. DESIGN SYSTEM
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --background: #0A1020;
    --surface: #111B2D;
    --surface-light: #172438;
    --border: #25364D;
    --text: #F1F5F9;
    --muted: #9AAABD;
    --accent: #75D5C2;
    --accent-dark: #173E3B;
}

/* =====================================================
   GLOBAL APP
===================================================== */

.stApp {
    background:
        radial-gradient(
            ellipse at 80% 0%,
            rgba(48, 104, 111, 0.12),
            transparent 38%
        ),
        var(--background);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1500px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* =====================================================
   TYPOGRAPHY
===================================================== */

h1, h2, h3, h4 {
    font-family: 'Manrope', sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -0.7px;
}

h1 {
    font-size: 2.25rem !important;
    font-weight: 800 !important;
}

h2 {
    font-size: 1.55rem !important;
    font-weight: 700 !important;
}

h3 {
    font-size: 1.15rem !important;
    font-weight: 700 !important;
}

p, label, li {
    color: var(--muted);
}

/* =====================================================
   SIDEBAR
===================================================== */

section[data-testid="stSidebar"] {
    background: #0D1728;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: var(--muted);
}

/* =====================================================
   BRANDING
===================================================== */

.brand-lockup {
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 10px 3px 22px;
}

.brand-icon {
    width: 46px;
    height: 46px;
    border-radius: 14px;
    background: linear-gradient(135deg, #8AE3D0, #55BBAA);
    color: #0A1821;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Manrope', sans-serif;
    font-size: 25px;
    font-weight: 800;
    box-shadow: 0 5px 22px rgba(117, 213, 194, 0.15);
}

.brand-name {
    color: var(--text);
    font-family: 'Manrope', sans-serif;
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -1px;
}

.brand-subtitle {
    color: #8295AB;
    font-size: 9px;
    letter-spacing: 1.7px;
    margin-top: 3px;
}

.sidebar-tagline {
    color: #91A5B9;
    font-size: 12px;
    letter-spacing: 0.3px;
    padding: 0 2px 8px;
}

/* =====================================================
   CUSTOM SIDEBAR NAVIGATION
===================================================== */

.nav-label {
    color: #71869D;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.7px;
    margin: 20px 0 9px 3px;
}

section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] {
    border-radius: 9px;
    padding: 9px 11px;
    margin: 3px 0;
    color: #AFC0D1;
    transition:
        background 0.2s ease,
        color 0.2s ease,
        transform 0.2s ease;
}

section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover {
    background: #1A2B40;
    color: var(--accent);
    transform: translateX(3px);
}

section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"][aria-current="page"] {
    background: #193A3B;
    color: var(--accent);
    border: 1px solid #285D58;
}

/* =====================================================
   METRIC CARDS
===================================================== */

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #152237, #111B2D);
    border: 1px solid var(--border);
    padding: 21px;
    border-radius: 15px;
    transition:
        transform 0.25s ease,
        border-color 0.25s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: #65BDAE;
}

div[data-testid="stMetricLabel"] {
    color: #A5B4C6;
    font-size: 0.86rem;
    font-weight: 500;
}

div[data-testid="stMetricValue"] {
    color: var(--text);
    font-family: 'Manrope', sans-serif;
    font-weight: 800;
}

/* =====================================================
   BUTTONS
===================================================== */

.stButton > button,
.stDownloadButton > button {
    border-radius: 10px;
    min-height: 43px;
    font-weight: 600;
    border: 1px solid #38536A;
    transition: all 0.22s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: var(--accent);
    color: var(--accent);
    transform: translateY(-2px);
}

/* =====================================================
   INPUTS
===================================================== */

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: var(--surface);
    border-color: #30445B;
    border-radius: 10px;
}

.stTextInput input,
.stNumberInput input {
    background: var(--surface);
}

/* =====================================================
   FILE UPLOADER
===================================================== */

div[data-testid="stFileUploader"] {
    background: #142238;
    border: 1px dashed #557487;
    border-radius: 14px;
    padding: 13px;
    transition:
        border-color 0.25s ease,
        background 0.25s ease;
}

div[data-testid="stFileUploader"]:hover {
    border-color: var(--accent);
    background: #172B3D;
}

/* =====================================================
   TABS
===================================================== */

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    border-bottom: 1px solid var(--border);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 9px 9px 0 0;
    padding: 11px 18px;
    color: var(--muted);
}

.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
}

/* =====================================================
   DATAFRAMES
===================================================== */

div[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
}

/* =====================================================
   ALERTS AND DIVIDERS
===================================================== */

div[data-testid="stAlert"] {
    border-radius: 11px;
}

hr {
    border-color: var(--border);
}

/* =====================================================
   STARTUP / WELCOME SCREEN
===================================================== */

.welcome-shell {
    position: relative;
    overflow: hidden;
    background: linear-gradient(
        135deg,
        #14243A 0%,
        #101C2E 55%,
        #122B32 100%
    );
    border: 1px solid #2C4658;
    border-radius: 25px;
    padding: 65px 55px;
    margin-top: 25px;
    animation: welcomeFade 0.8s ease both;
}

.welcome-shell::before {
    content: "";
    position: absolute;
    width: 350px;
    height: 350px;
    right: -100px;
    top: -160px;
    background: rgba(117, 213, 194, 0.12);
    filter: blur(75px);
    border-radius: 50%;
    animation: glowFloat 7s ease-in-out infinite alternate;
}

.welcome-eyebrow {
    color: var(--accent);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.welcome-heading {
    color: #F5F8FC;
    font-family: 'Manrope', sans-serif;
    font-size: clamp(38px, 5vw, 62px);
    line-height: 1.12;
    font-weight: 800;
    letter-spacing: -2.5px;
    max-width: 700px;
}

.welcome-heading span {
    color: var(--accent);
}

.welcome-description {
    color: #A8B8C9;
    font-size: 16px;
    line-height: 1.8;
    max-width: 590px;
    margin-top: 20px;
}

.welcome-note {
    color: #8FA3B8;
    font-size: 13px;
    margin-top: 28px;
}

/* =====================================================
   FEATURE CARDS
===================================================== */

.feature-card {
    background: rgba(21, 35, 55, 0.8);
    border: 1px solid #2A4055;
    border-radius: 15px;
    padding: 20px;
    min-height: 125px;
    height: 100%;
    transition:
        transform 0.25s ease,
        border-color 0.25s ease;
}

.feature-card:hover {
    transform: translateY(-4px);
    border-color: var(--accent);
}

.feature-title {
    color: #F1F5F9;
    font-family: 'Manrope', sans-serif;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 7px;
}

.feature-description {
    color: #9AAABD;
    font-size: 13px;
    line-height: 1.6;
}

/* =====================================================
   ANIMATIONS
===================================================== */

@keyframes welcomeFade {
    from {
        opacity: 0;
        transform: translateY(14px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes glowFloat {
    from {
        transform: translate(0, 0);
    }

    to {
        transform: translate(-45px, 35px);
    }
}

/* =====================================================
   RESPONSIVE DESIGN
===================================================== */

@media (max-width: 700px) {

    .welcome-shell {
        padding: 35px 25px;
    }

    .welcome-heading {
        letter-spacing: -1.5px;
    }

    .block-container {
        padding-top: 1.5rem;
    }
}

/* =====================================================
   ACCESSIBILITY
===================================================== */

@media (prefers-reduced-motion: reduce) {

    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }

}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. SESSION STATE INITIALIZATION
# =====================================================

if "dataset" not in st.session_state:
    st.session_state.dataset = None

if "filename" not in st.session_state:
    st.session_state.filename = None

if "dataset_signature" not in st.session_state:
    st.session_state.dataset_signature = None

if "cleaned_dataset" not in st.session_state:
    st.session_state.cleaned_dataset = None

if "cleaned_filename" not in st.session_state:
    st.session_state.cleaned_filename = None


# =====================================================
# 4. PAGE DEFINITIONS
# =====================================================

overview_page = st.Page(
    "pages/overview.py",
    title="Overview",
    icon=":material/dashboard:",
    default=True
)

explorer_page = st.Page(
    "pages/data_explorer.py",
    title="Data Explorer",
    icon=":material/search:"
)

quality_page = st.Page(
    "pages/data_quality.py",
    title="Data Quality",
    icon=":material/verified_user:"
)

analytics_page = st.Page(
    "pages/visual_analytics.py",
    title="Visual Analytics",
    icon=":material/monitoring:"
)

insights_page = st.Page(
    "pages/insights.py",
    title="Insights",
    icon=":material/lightbulb:"
)

export_page = st.Page(
    "pages/export.py",
    title="Export Center",
    icon=":material/download:"
)


# =====================================================
# 5. HIDDEN STREAMLIT NAVIGATION
# =====================================================

pg = st.navigation(
    [
        overview_page,
        explorer_page,
        quality_page,
        analytics_page,
        insights_page,
        export_page
    ],
    position="hidden"
)


# =====================================================
# 6. PREMIUM SIDEBAR
# =====================================================

with st.sidebar:

    # BRANDING

    
    st.html("""
    <div class="brand-lockup">

        <div class="brand-icon">D</div>

        <div>
            <div class="brand-name">DataLens</div>

            <div class="brand-subtitle">
                DATA INTELLIGENCE STUDIO
            </div>
        </div>

    </div>
    """)


    st.markdown(
        '<div class="sidebar-tagline">'
        'Explore. Understand. Improve.'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # CUSTOM NAVIGATION

    st.markdown(
        '<div class="nav-label">WORKSPACE</div>',
        unsafe_allow_html=True
    )

    st.page_link(
        overview_page,
        label="Overview",
        width="stretch"
    )

    st.page_link(
        explorer_page,
        label="Data Explorer",
        width="stretch"
    )

    st.page_link(
        quality_page,
        label="Data Quality",
        width="stretch"
    )

    st.markdown(
        '<div class="nav-label">ANALYSIS</div>',
        unsafe_allow_html=True
    )

    st.page_link(
        analytics_page,
        label="Visual Analytics",
        width="stretch"
    )

    st.page_link(
        insights_page,
        label="Intelligent Insights",
        width="stretch"
    )

    st.markdown(
        '<div class="nav-label">OUTPUT</div>',
        unsafe_allow_html=True
    )

    st.page_link(
        export_page,
        label="Export Center",
        width="stretch"
    )

        
    # SIDEBAR DIVIDER

    st.divider()

    # DATASET UPLOAD

    st.markdown("### Your Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload a CSV dataset to begin your analysis."
    )

    if uploaded_file is not None:

        try:

            file_bytes = uploaded_file.getvalue()

            file_signature = hashlib.sha256(
                file_bytes
            ).hexdigest()

            # Reset cleaning state only when file content changes

            if st.session_state.dataset_signature != file_signature:

                st.session_state.cleaned_dataset = None
                st.session_state.cleaned_filename = None

                st.session_state.dataset_signature = file_signature

            # Load CSV

            df = load_csv(file_bytes)

            if df.empty:

                st.error("The uploaded dataset is empty.")

                st.session_state.dataset = None
                st.session_state.filename = None

            else:

                st.session_state.dataset = df
                st.session_state.filename = uploaded_file.name

                st.success("Dataset loaded successfully!")

        except Exception as e:

            st.error(f"Unable to load CSV: {e}")

            st.session_state.dataset = None
            st.session_state.filename = None
            st.session_state.dataset_signature = None

            st.session_state.cleaned_dataset = None
            st.session_state.cleaned_filename = None

    else:

        st.session_state.dataset = None
        st.session_state.filename = None
        st.session_state.dataset_signature = None

        st.session_state.cleaned_dataset = None
        st.session_state.cleaned_filename = None

    # ACTIVE DATASET INFORMATION

    st.divider()

    if st.session_state.dataset is not None:

        st.caption("ACTIVE DATASET")

        st.markdown(
            f"**{st.session_state.filename}**"
        )

        st.caption(
            f"{len(st.session_state.dataset):,} records · "
            f"{len(st.session_state.dataset.columns):,} columns"
        )

    else:

        st.caption(
            "Upload a dataset to unlock your workspace."
        )

    st.divider()

    st.caption("DataLens · Built with Python")


# =====================================================
# 7. STARTUP / WELCOME EXPERIENCE
# =====================================================

if st.session_state.dataset is None:

    st.html("""
    <div class="welcome-shell">

        <div class="welcome-eyebrow">
            DATA INTELLIGENCE STUDIO
        </div>

        <div class="welcome-heading">
            Your Data.<br>
            <span>Decoded.</span>
        </div>

        <div class="welcome-description">
            Turn raw datasets into meaningful discoveries.
            Explore your data, uncover hidden patterns,
            improve data quality and generate intelligent insights
            — all in one workspace.
        </div>

        <div class="welcome-note">
            ↑ Upload your CSV using the sidebar to get started.
        </div>

    </div>
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "### Everything you need to understand your data"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.html("""
        <div class="feature-card">

            <div class="feature-title">
                01 · Explore
            </div>

            <div class="feature-description">
                Inspect rows, columns, data types and
                understand the structure of your dataset.
            </div>

        </div>
        """)

    with col2:

        st.html("""
        <div class="feature-card">

            <div class="feature-title">
                02 · Improve
            </div>

            <div class="feature-description">
                Identify missing values, duplicates and
                outliers. Clean your data with confidence.
            </div>

        </div>
        """)

    with col3:

        st.html("""
        <div class="feature-card">

            <div class="feature-title">
                03 · Discover
            </div>

            <div class="feature-description">
                Create interactive visualizations and
                uncover useful statistical insights.
            </div>

        </div>
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption(
        "Supports CSV datasets · Interactive analytics · "
        "Data quality assessment"
    )

    st.stop()


# =====================================================
# 8. RUN SELECTED PAGE
# =====================================================

pg.run()
