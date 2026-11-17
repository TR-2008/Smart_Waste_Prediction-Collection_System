import streamlit as st

DARK_CSS = """
<style>
:root { color-scheme: dark; }
.stApp { background: radial-gradient(circle at 80% 0%, #132c3a 0, #0a1220 42%, #080f1a 100%); color:#e8f1f7; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#101e2d,#0c1724); border-right:1px solid #24384a; }
.block-container { padding-top:1.7rem; max-width:1500px; }
[data-testid="stMetric"] { background:linear-gradient(145deg,#14283a,#102131); border:1px solid #254357; padding:16px 18px; border-radius:16px; }
.hero { padding:32px; border-radius:24px; border:1px solid #28516a; background:linear-gradient(115deg,rgba(10,92,89,.55),rgba(19,37,60,.95)); margin:8px 0 24px; }
.hero-kicker { letter-spacing:.18em; color:#5ee3c0; font-size:.72rem; font-weight:800; }
.hero h1 { font-size:clamp(2rem,4vw,3.5rem); line-height:1.08; margin:.6rem 0; color:#f3fbff; }
.hero h1 span { color:#5ee3c0; }
.hero p { color:#b6cbd8; font-size:1.05rem; max-width:700px; }
[data-testid="stVerticalBlock"] > div:has(> .stButton) .stButton button { border-radius:12px; }
div[data-testid="stAlert"] { border-radius:14px; }
</style>
"""
LIGHT_CSS = """
<style>
:root { color-scheme: light; }
.stApp { background:linear-gradient(135deg,#f3f8fb,#edf5f4); color:#172b3a; }
[data-testid="stSidebar"] { background:#ffffff; border-right:1px solid #dce8ec; }
.block-container { padding-top:1.7rem; max-width:1500px; }
[data-testid="stMetric"] { background:#ffffff; border:1px solid #dbe8e9; padding:16px 18px; border-radius:16px; box-shadow:0 5px 18px rgba(19,54,67,.05); }
.hero { padding:32px; border-radius:24px; border:1px solid #c4e7df; background:linear-gradient(115deg,#d9f5ed,#e9f2fb); margin:8px 0 24px; }
.hero-kicker { letter-spacing:.18em; color:#087d6b; font-size:.72rem; font-weight:800; }
.hero h1 { font-size:clamp(2rem,4vw,3.5rem); line-height:1.08; margin:.6rem 0; color:#173747; }
.hero h1 span { color:#078b76; }
.hero p { color:#4b6672; font-size:1.05rem; max-width:700px; }
div[data-testid="stAlert"] { border-radius:14px; }
</style>
"""

def apply_theme(theme):
    st.markdown(DARK_CSS if theme == "Dark" else LIGHT_CSS, unsafe_allow_html=True)

def render_sidebar(root):
    with st.sidebar:
        st.markdown("## ♻️ Smart Waste AI")
        st.caption("Collection & sorting intelligence")
        st.selectbox("Appearance", ["Dark", "Light"], key="ui_theme")
        st.divider()
        st.page_link("app.py", label="Overview", icon="🏠")
        st.page_link("pages/1_Manual_AI.py", label="Collection prediction", icon="🧠")
        st.page_link("pages/2_Material_Recognition.py", label="Material recognition", icon="♻️")
        st.page_link("pages/3_Analytics.py", label="Analytics & reports", icon="📊")
        st.page_link("pages/4_Feedback_NLP.py", label="Feedback intelligence", icon="💬")
        st.page_link("pages/5_System_Settings.py", label="System settings", icon="⚙️")
        st.page_link("pages/6_IoT_Status.py", label="IoT status", icon="📡")

def section_header(title, subtitle=None):
    st.title(title)
    if subtitle:
        st.caption(subtitle)

def metric_card(column, label, value, status="success"):
    with column:
        st.metric(label, value)
