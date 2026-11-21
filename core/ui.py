import base64
from pathlib import Path
import streamlit as st
ROOT=Path(__file__).resolve().parents[1]
DARK="""<style>
:root{--bg:#071321;--panel:#101f32;--panel2:#142941;--line:#263e55;--green:#20df83;--muted:#9bb0c4;--text:#f3f8ff}
.stApp{background:radial-gradient(ellipse at 82% -5%,#123b39 0,#091827 34%,#06111d 78%);color:var(--text)}
.block-container{max-width:1680px;padding:1.05rem 1.35rem 2.5rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0b1b2d,#071421);border-right:1px solid #244054}
[data-testid="stSidebarNav"]{padding-top:.3rem}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:#b7c9d8}
[data-testid="stSidebar"] a{border-radius:11px!important;margin:2px 7px!important;padding:9px 10px!important}
[data-testid="stSidebar"] a[aria-current="page"]{background:linear-gradient(90deg,#087d50,#0dbb70)!important;color:#fff!important;box-shadow:0 0 18px #0ac87955}
[data-testid="stMetric"]{background:linear-gradient(145deg,#132a40,#0e2032);border:1px solid #28445a;padding:15px 17px;border-radius:17px;box-shadow:0 8px 26px #0003;min-height:112px}
[data-testid="stMetricLabel"]{color:#a9bdce;font-size:.82rem}
[data-testid="stMetricValue"]{color:#f7fbff;font-weight:800}
[data-testid="stMetricDelta"]{font-size:.78rem}
[data-testid="stVerticalBlockBorderWrapper"]{background:linear-gradient(145deg,#11243aee,#0c1b2cee);border:1px solid #263f56;border-radius:18px;padding:12px}
.stButton>button{border-radius:11px;font-weight:700;min-height:2.55rem;border:1px solid #2e6b55}
[data-testid="stFileUploader"]{border:1px dashed #42a879;border-radius:15px;padding:10px}
[data-testid="stImage"] img{border-radius:14px}
[data-testid="stAlert"]{border-radius:13px}
hr{border-color:#243b50}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:2px 2px 12px;border-bottom:1px solid #254055;margin-bottom:13px}
.brandline{display:flex;align-items:center;gap:12px;min-width:0}.brandline img{width:43px;height:43px}.brandname{font-size:clamp(1.05rem,2vw,1.65rem);font-weight:850;line-height:1.15;color:#f5f9ff}.brandname span{color:#73e98d}.tagline{font-size:.78rem;color:#72d8d0;font-style:italic;margin-top:3px}
.livepill{border:1px solid #16865b;background:#0d382f;color:#a8ffd0;padding:7px 13px;border-radius:30px;font-size:.76rem;white-space:nowrap}
.hero-wrap{height:228px;border-radius:19px;overflow:hidden;position:relative;border:1px solid #238c78;margin:5px 0 15px;background:#0d2938}
.hero-wrap img{width:100%;height:100%;object-fit:cover;display:block;filter:saturate(1.08)}
.hero-overlay{position:absolute;inset:0;background:linear-gradient(90deg,rgba(3,16,29,.08) 0%,rgba(3,16,29,.14) 34%,rgba(3,16,29,.73) 54%,rgba(3,16,29,.20) 100%);display:flex;align-items:center;justify-content:center;text-align:center;padding:18px}
.hero-copy{max-width:650px;text-shadow:0 2px 10px #06111dcc}.hero-copy h1{font-size:clamp(1.45rem,3vw,2.65rem);line-height:1.05;margin:0 0 8px;color:#fff;font-weight:900}.hero-copy h1 span{color:#6df28b}.hero-copy p{color:#effff6;margin:0;font-size:.92rem}
.panel-title{font-size:1.02rem;font-weight:800;color:#f3f8ff;margin:0 0 8px}.panel-sub{color:#92a9bb;font-size:.76rem;margin-top:-5px}
@media(max-width:850px){.hero-wrap{height:190px}.hero-overlay{background:rgba(4,17,29,.48)}.topbar{align-items:flex-start}.livepill{font-size:.68rem}}
</style>"""
LIGHT="""<style>
.stApp{background:linear-gradient(135deg,#eff8f3,#e8f1f7);color:#163448}.block-container{max-width:1680px;padding:1.05rem 1.35rem 2.5rem}
[data-testid="stSidebar"]{background:#f9fffb;border-right:1px solid #d5e7df}[data-testid="stSidebar"] a[aria-current="page"]{background:linear-gradient(90deg,#087d50,#0dbb70)!important;color:white!important}
[data-testid="stMetric"]{background:linear-gradient(145deg,#fff,#f2faf5);border:1px solid #d6e9de;padding:15px 17px;border-radius:17px;box-shadow:0 8px 24px #214c3510;min-height:112px}
[data-testid="stMetricLabel"]{color:#587365}[data-testid="stMetricValue"]{color:#173a30;font-weight:800}
[data-testid="stVerticalBlockBorderWrapper"]{background:#ffffffd9;border:1px solid #d8e9e0;border-radius:18px;padding:12px}
.stButton>button{border-radius:11px;font-weight:700}.topbar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:2px 2px 12px;border-bottom:1px solid #d5e6df;margin-bottom:13px}
.brandline{display:flex;align-items:center;gap:12px}.brandline img{width:43px;height:43px}.brandname{font-size:clamp(1.05rem,2vw,1.65rem);font-weight:850;color:#163448}.brandname span{color:#168052}.tagline{font-size:.78rem;color:#168b83;font-style:italic;margin-top:3px}.livepill{border:1px solid #69c79a;background:#e0f8eb;color:#087747;padding:7px 13px;border-radius:30px;font-size:.76rem}
.hero-wrap{height:228px;border-radius:19px;overflow:hidden;position:relative;border:1px solid #8bc9ad;margin:5px 0 15px;background:#0d2938}.hero-wrap img{width:100%;height:100%;object-fit:cover}.hero-overlay{position:absolute;inset:0;background:linear-gradient(90deg,rgba(3,16,29,.05),rgba(3,16,29,.65) 55%,rgba(3,16,29,.12));display:flex;align-items:center;justify-content:center;text-align:center;padding:18px}.hero-copy{max-width:650px;text-shadow:0 2px 10px #06111dcc}.hero-copy h1{font-size:clamp(1.45rem,3vw,2.65rem);line-height:1.05;margin:0 0 8px;color:white;font-weight:900}.hero-copy h1 span{color:#7df09b}.hero-copy p{color:#effff6;margin:0;font-size:.92rem}.panel-title{font-size:1.02rem;font-weight:800;color:#173448;margin:0 0 8px}.panel-sub{color:#658071;font-size:.76rem;margin-top:-5px}
</style>"""
def apply_theme(theme='Dark'):
    st.markdown(DARK if theme=='Dark' else LIGHT,unsafe_allow_html=True)
def render_brand(mode='Manual'):
    logo=ROOT/'assets'/'logo.svg'
    
    encoded=base64.b64encode(logo.read_bytes()).decode('ascii') if logo.exists() else ''
    with st.sidebar:
        if encoded: st.markdown(f'<div style="display:flex;gap:11px;align-items:center;padding:8px 2px 13px"><img src="data:image/svg+xml;base64,{encoded}" style="width:43px;height:43px"><div style="font-weight:850;font-size:14px;line-height:1.25;color:#f4fbff">Smart Waste<br><span style="color:#70e68c">Management & Prediction</span><br><small style="color:#b4c8d7">System</small></div></div>',unsafe_allow_html=True)
        st.caption('COMMUNITY WASTE INTELLIGENCE')
        st.markdown(f'<div style="border:1px solid #246b50;background:#0d3029;border-radius:12px;padding:10px;margin:10px 0;color:#a9ffd0;font-size:12px">● System workspace<br><b>{mode} Mode</b></div>',unsafe_allow_html=True)
def render_topbar(mode='Manual'):
    logo=ROOT/'assets'/'logo.svg'
    
    encoded=base64.b64encode(logo.read_bytes()).decode('ascii') if logo.exists() else ''
    img=f'<img src="data:image/svg+xml;base64,{encoded}">' if encoded else '<span style="font-size:32px">♻️</span>'
    st.markdown(f'<div class="topbar"><div class="brandline">{img}<div><div class="brandname">Smart Waste <span>Management</span> & Prediction System</div><div class="tagline">Smarter Decisions. A Cleaner Tomorrow.</div></div></div><div class="livepill">● &nbsp; Workspace Mode: {mode}</div></div>',unsafe_allow_html=True)
def hero(title='Smarter waste. Cleaner communities.',subtitle='One intelligent workspace for material recognition, collection decisions and waste analytics.'):
    art=ROOT/'assets'/'recycling_hero_banner.png'
    if art.exists():
        encoded=base64.b64encode(art.read_bytes()).decode('ascii')
        st.markdown(f'<div class="hero-wrap"><img src="data:image/png;base64,{encoded}" alt="Green city, recycling globe and sorting bins"><div class="hero-overlay"><div class="hero-copy"><h1>{title}</h1><p>{subtitle}</p></div></div></div>',unsafe_allow_html=True)
    else: st.info(subtitle)
def section_header(title,subtitle=None):
    st.title(title)
    if subtitle: st.caption(subtitle)
def load_plotly():
    try:
        import plotly.express as px
        import plotly.graph_objects as go
        return px,go
    except ImportError: return None,None
