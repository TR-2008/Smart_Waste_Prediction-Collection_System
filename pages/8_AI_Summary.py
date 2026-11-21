from pathlib import Path
import pandas as pd,streamlit as st
from core.ui import apply_theme,section_header
ROOT=Path(__file__).resolve().parents[1]; apply_theme(st.session_state.get('ui_theme','Dark'))
section_header('AI Summary','Grounded operational summary from the supplied classroom dataset.')
p=ROOT/'data'/'main.csv'
if p.exists():
 d=pd.read_csv(p); st.markdown('### Offline dataset summary')
 st.write(f"The supplied dataset contains **{len(d):,}** generated classroom records. Average fill is **{d.fill_pct.mean():.1f}%**. **{int(d.needs_collection.sum())}** records ({d.needs_collection.mean():.1%}) carry the collection-review label.")
 loc=d.groupby('location_type').agg(records=('record_id','count'),mean_fill=('fill_pct','mean'),review_labels=('needs_collection','sum')).reset_index()
 st.dataframe(loc,use_container_width=True,hide_index=True)
 st.caption('This is a deterministic offline summary of generated practice data, not a live operational recommendation.')
else: st.warning('main.csv is missing; summary cannot be generated.')
st.info('Groq-powered summaries are not connected in this bundle. Configure a secret and provider integration before selecting a cloud summary provider.')
