from pathlib import Path
from datetime import datetime
import pandas as pd
import streamlit as st
from core.ui import apply_theme,section_header
from core.model_loader import load_models
from core.prediction_engine import prepare_image,predict_material
from core.storage import add_recognition,get_recognition_history,clear_recognition_history
ROOT=Path(__file__).resolve().parents[1]
apply_theme(st.session_state.get('ui_theme','Dark'))
section_header('Material Image','Classify one dominant waste material: paper, plastic or metal.')
@st.cache_resource
def get_models(path): return load_models(path)
model_dir=ROOT/'models'; options=['CNN']
if (model_dir/'mobilenetv2_waste.keras').is_file(): options.append('MobileNetV2')
default=st.session_state.get('image_model_choice','CNN'); selected=st.selectbox('Classification model',options,index=options.index(default) if default in options else 0)
left,right=st.columns([.9,1.1],gap='large')
with left:
    uploaded=st.file_uploader('Upload a JPG or PNG',type=['jpg','jpeg','png'],help='Use a clear image with one main material.')
    run=st.button('♻️ Analyse material',type='primary',use_container_width=True,disabled=uploaded is None)
with right:
    if uploaded:
        image,batch=prepare_image(uploaded); st.image(image,caption='96 × 96 RGB model input',width=340)
    else: st.markdown('<div style="border:1px dashed #4c9b77;border-radius:18px;padding:55px 18px;text-align:center"><div style="font-size:42px">♻️</div><b>Image preview</b><p>Upload a paper, plastic or metal image</p></div>',unsafe_allow_html=True)
if uploaded and run:
    try:
        models=get_models(str(model_dir)); st.session_state['_loaded_model_keys']=list(k for k in models if not k.startswith('_'))
        result=predict_material(models,batch,selected)
        now=datetime.now().astimezone().isoformat(timespec='seconds')
        add_recognition(now,result['class'],result['confidence'],selected,uploaded.name)
        a,b,c=st.columns(3); a.metric('Predicted material',result['class'].title()); b.metric('Confidence',f"{result['confidence']:.1%}"); c.metric('Model',selected)
        st.markdown('**Class probability breakdown**'); st.bar_chart(pd.Series(result['probabilities']),horizontal=True)
        st.caption('Whole-image classification only; it does not detect multiple objects in mixed-waste scenes.')
    except Exception as e: st.error(f'Image prediction failed: {e}')

st.markdown('### Recognition history')
history=get_recognition_history(100)
if history:
    d=pd.DataFrame(history); x,y=st.columns(2)
    with x: st.markdown('**Material distribution**'); st.bar_chart(d.material.value_counts())
    with y: st.markdown('**Confidence trend · latest 30**'); st.line_chart(d.head(30).iloc[::-1].set_index('time')['confidence'])
    st.dataframe(d,use_container_width=True,hide_index=True)
    if st.button('Clear saved recognition history'): clear_recognition_history(); st.rerun()
else: st.info('No saved recognition records yet. History is stored locally in data/app_history.sqlite3.')
