from pathlib import Path
import pandas as pd,streamlit as st
from core.ui import apply_theme,section_header
ROOT=Path(__file__).resolve().parents[1]; apply_theme(st.session_state.get('ui_theme','Dark'))
section_header('Advanced Analytics','Detailed splits, distributions and evaluation indicators.')
p=ROOT/'data'/'main.csv'
if p.exists():
 d=pd.read_csv(p); st.markdown('### Collection labels by dataset split'); st.bar_chart(pd.crosstab(d['split'],d['needs_collection']))
 st.markdown('### Fill distribution'); st.line_chart(d.sort_values('record_id').set_index('record_id')['fill_pct'])
 st.markdown('### Location profile'); st.dataframe(d.groupby('location_type').agg(records=('record_id','count'),average_fill=('fill_pct','mean'),review_count=('needs_collection','sum')).reset_index(),use_container_width=True,hide_index=True)
 st.caption('All source records are synthetic classroom practice data; no live telemetry is represented.')
else: st.warning('main.csv missing.')
