from pathlib import Path
import streamlit as st
from core.ui import apply_theme,section_header
from core.model_loader import load_models
from core.prediction_engine import predict_collection,predict_cluster
ROOT=Path(__file__).resolve().parents[1]
apply_theme(st.session_state.get('ui_theme','Dark'))
section_header('Bin Overview & Collection Review','Decision support using the saved supervised and clustering models.')
@st.cache_resource
def get_models(path): return load_models(path)
with st.form('collection_form'):
    a,b=st.columns(2)
    with a:
        fill=st.slider('Current fill level (%)',0,100,70); days=st.slider('Days since last collection',1,7,4); location=st.selectbox('Location type',['campus','market','park'])
    with b:
        footfall=st.number_input('Daily footfall',0,1000,150); capacity=st.selectbox('Bin capacity (litres)',[40,60,80,100,120],index=4)
    submitted=st.form_submit_button('Run collection prediction',type='primary')
if submitted:
    try:
        models=get_models(str(ROOT/'models')); st.session_state['_loaded_model_keys']=list(k for k in models if not k.startswith('_'))
        result=predict_collection(models,ROOT/'models',fill,days,footfall,capacity,location)
        cluster=predict_cluster(models,ROOT/'models',fill,days,footfall,capacity)
        a,b,c=st.columns(3); a.metric('Decision Tree',result['label']); b.metric('Baseline reference',result['baseline_label']); c.metric('K-Means group',f"Cluster {cluster['cluster']}")
        if result['probabilities']: st.json(result['probabilities'])
        st.info('Cluster profile: '+cluster['description'])
        st.caption('Decision-support output from generated classroom practice data; not a real dispatch instruction.')
    except Exception as e: st.error(f'Prediction could not be completed: {e}')
