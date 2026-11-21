from pathlib import Path
import json,pandas as pd,streamlit as st
from core.ui import apply_theme,section_header
ROOT=Path(__file__).resolve().parents[1]; apply_theme(st.session_state.get('ui_theme','Dark'))
section_header('Bin Profiles','Explore supplied facility and collection profiles.')
p=ROOT/'data'/'main.csv'
if p.exists():
 d=pd.read_csv(p); a,b,c=st.columns(3); a.metric('Records',f'{len(d):,}'); b.metric('Mean fill',f'{d.fill_pct.mean():.1f}%'); c.metric('Review labels',int(d.needs_collection.sum()))
 st.markdown('**Average fill by location**'); st.bar_chart(d.groupby('location_type').fill_pct.mean())
 st.markdown('**Fill level by location · record order**')
 for loc,g in d.sort_values('record_id').groupby('location_type'): st.line_chart(g.set_index('record_id').fill_pct.rename(loc))
 st.markdown('**Train / validation / test distribution**'); st.bar_chart(d.split.value_counts())
 st.caption('All rows are generated classroom practice data, not live bin telemetry.')
else: st.warning('data/main.csv not found.')
