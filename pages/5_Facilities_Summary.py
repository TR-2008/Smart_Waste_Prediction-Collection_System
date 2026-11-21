from pathlib import Path
import pandas as pd,streamlit as st
from core.ui import apply_theme,section_header
ROOT=Path(__file__).resolve().parents[1]; apply_theme(st.session_state.get('ui_theme','Dark'))
section_header('Facilities Summary','Combined summary of supplied classroom facility records.')
p=ROOT/'data'/'main.csv'
if p.exists():
 d=pd.read_csv(p); a,b,c=st.columns(3); a.metric('Dataset records',len(d)); b.metric('Mean bin fill',f'{d.fill_pct.mean():.1f}%'); c.metric('Collection review labels',int(d.needs_collection.sum()))
 st.markdown('**Average fill by location**'); st.bar_chart(d.groupby('location_type').fill_pct.mean())
 st.markdown('**Record counts by location**'); st.bar_chart(d.location_type.value_counts())
 st.caption('Generated practice dataset. No live facilities are connected.')
else: st.warning('data/main.csv not found.')
