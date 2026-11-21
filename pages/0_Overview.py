from pathlib import Path
import json
import pandas as pd
import streamlit as st
from core.ui import apply_theme, render_topbar, hero, load_plotly
from core.model_loader import check_model_files
from core.storage import get_recognition_history
ROOT=Path(__file__).resolve().parents[1]
mode=st.session_state.get('operating_mode','Manual')
theme=st.session_state.get('ui_theme','Dark')
apply_theme(theme)
render_topbar(mode)
hero('Smart Waste Management<br><span>& Prediction System</span>','AI-powered insights for cleaner communities, smarter sorting and efficient collection decisions.')

def read_json(path):
    try: return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    except Exception: return {}
main_path=ROOT/'data'/'main.csv'; image_path=ROOT/'data'/'image_manifest.csv'
df=pd.read_csv(main_path) if main_path.exists() else pd.DataFrame()
images=pd.read_csv(image_path) if image_path.exists() else pd.DataFrame()
reports=read_json(ROOT/'reports'/'supervised_metrics.json'); img_report=read_json(ROOT/'reports'/'mobilenetv2_test_metrics.json')
if not df.empty:
    total=len(df); avg=float(df['fill_pct'].mean()); flagged=int(df['needs_collection'].sum()); locations=int(df['location_type'].nunique())
else: total=avg=flagged=locations=None
img_acc=img_report.get('test_accuracy')
cols=st.columns(5)
items=[('Dataset Records',f'{total:,}' if total is not None else 'N/A','Supplied classroom dataset'),('Average Bin Fill',f'{avg:.1f}%' if avg is not None else 'N/A','Mean across available records'),('Collection Review',f'{flagged:,}' if flagged is not None else 'N/A','Records flagged for review'),('Material Images',f'{len(images):,}' if not images.empty else 'N/A','Manifest entries'),('MobileNetV2 Accuracy',f'{img_acc:.1%}' if isinstance(img_acc,(int,float)) else 'N/A','Saved held-out test report')]
for c,(label,value,helptext) in zip(cols,items): c.metric(label,value,help=helptext)
st.caption('Dataset provenance: supplied generated classroom/practice data and saved evaluation reports. These are not live municipal or IoT measurements.')
st.markdown('')
px,go=load_plotly(); plot_template='plotly_dark' if theme=='Dark' else 'plotly_white'
left,right=st.columns([1.0,1.55],gap='medium')
with left:
    with st.container(border=True):
        st.markdown('<div class="panel-title">♻️ Waste Composition Overview</div><div class="panel-sub">Material image manifest · paper, plastic and metal</div>',unsafe_allow_html=True)
        if not images.empty and 'class_id' in images.columns:
            names={0:'Paper',1:'Plastic',2:'Metal'}
            comp=images['class_id'].map(names).fillna('Unknown').value_counts().rename_axis('Material').reset_index(name='Images')
            if px:
                fig=px.pie(comp,names='Material',values='Images',hole=.67,color_discrete_sequence=['#28d17c','#278dff','#f5a623'],template=plot_template)
                fig.update_layout(height=285,margin=dict(l=0,r=0,t=5,b=0),legend=dict(orientation='h',y=-.08),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
                fig.update_traces(textposition='inside',textinfo='percent+label',hole=.67)
                st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
            else: st.bar_chart(comp.set_index('Material'))
        else: st.info('Image manifest is not available; composition chart cannot be calculated.')
with right:
    with st.container(border=True):
        st.markdown('<div class="panel-title">↗ Waste Trends & Bin Fill Pattern</div><div class="panel-sub">Mean fill percentage by record sequence · not a date-based live trend</div>',unsafe_allow_html=True)
        if not df.empty and px:
            trend=df.sort_values('record_id').reset_index(drop=True).copy(); trend['sequence_group']=(trend.index//50)+1
            agg=trend.groupby(['sequence_group','location_type'],as_index=False)['fill_pct'].mean()
            fig=px.line(agg,x='sequence_group',y='fill_pct',color='location_type',markers=True,template=plot_template,color_discrete_sequence=['#2ed47a','#258dff','#f5a623','#a56bff'])
            fig.update_layout(height=285,margin=dict(l=5,r=8,t=5,b=5),xaxis_title='Record batch (50 records)',yaxis_title='Average fill (%)',legend_title='',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',hovermode='x unified')
            st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
        elif not df.empty: st.line_chart(df.groupby('location_type')['fill_pct'].mean())
        else: st.info('main.csv is missing; trend chart is unavailable.')

st.markdown('')
col1,col2,col3=st.columns([1.05,1.0,1.0],gap='medium')
with col1:
    with st.container(border=True):
        st.markdown('<div class="panel-title">📷 Material Recognition</div><div class="panel-sub">Latest saved prediction</div>',unsafe_allow_html=True)
        history=get_recognition_history(1)
        if history:
            latest=history[0]; st.markdown(f"### {str(latest.get('class','Unknown')).title()}")
            st.metric('Confidence',f"{float(latest.get('confidence',0)):.1%}")
            st.caption(f"Model: {latest.get('model','Unknown')} · {latest.get('time','')}")
            st.caption('Prediction metadata is saved; original uploaded image is not retained by the history database.')
        else:
            st.markdown('### No recognition yet')
            st.caption('Open Material Recognition to upload an image and run the classifier.')
        st.page_link('pages/2_Material_Recognition.py',label='Open Material Recognition →',icon='♻️')
with col2:
    with st.container(border=True):
        st.markdown('<div class="panel-title">🧠 Model Performance</div><div class="panel-sub">Saved evaluation reports</div>',unsafe_allow_html=True)
        test_rows=reports.get('test',[])
        if test_rows:
            for row in test_rows:
                acc=row.get('accuracy'); f1=row.get('macro_f1')
                st.markdown(f"**{row.get('model','Model')}**")
                st.progress(max(0,min(1,float(acc or 0))),text=f"Test accuracy: {acc:.1%} · Macro F1: {f1:.3f}" if acc is not None and f1 is not None else 'Metrics unavailable')
        if img_acc is not None:
            st.markdown('**MobileNetV2 image classifier**')
            st.progress(float(img_acc),text=f"Test accuracy: {img_acc:.1%} · {img_report.get('test_images','?')} test images")
        if not test_rows and img_acc is None: st.info('No saved model evaluation reports found.')
        st.caption('Accuracy values are report results, not proof that a model is currently loaded.')
with col3:
    with st.container(border=True):
        st.markdown('<div class="panel-title">🗂 Dataset Split Distribution</div><div class="panel-sub">Main dataset · supplied split labels</div>',unsafe_allow_html=True)
        if not df.empty and 'split' in df.columns:
            split=df['split'].value_counts().rename_axis('Split').reset_index(name='Records')
            if px:
                fig=px.pie(split,names='Split',values='Records',hole=.62,color_discrete_sequence=['#28d17c','#278dff','#f5a623'],template=plot_template)
                fig.update_layout(height=205,margin=dict(l=0,r=0,t=0,b=0),showlegend=True,legend=dict(orientation='h',y=-.08),paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
            else: st.bar_chart(split.set_index('Split'))
        else: st.info('Split labels unavailable.')

st.markdown('')
with st.container(border=True):
    st.markdown('<div class="panel-title">🕘 Recent Recognition Activity</div><div class="panel-sub">Locally stored prediction history</div>',unsafe_allow_html=True)
    recent=get_recognition_history(5)
    if recent:
        out=pd.DataFrame(recent).rename(columns={'time':'Timestamp','class':'Material','confidence':'Confidence','model':'Model','filename':'File'})
        if 'Confidence' in out: out['Confidence']=out['Confidence'].map(lambda x:f'{float(x):.1%}')
        st.dataframe(out,use_container_width=True,hide_index=True)
    else: st.info('No saved recognitions yet. Your latest predictions will appear here after using Material Recognition.')

with st.expander('System & model availability'):
    checks=check_model_files(ROOT/'models')
    loaded=set(st.session_state.get('_loaded_model_keys',[]))
    model_rows=[('Decision Tree','supervised','supervised.joblib'),('Baseline','baseline','baseline.joblib'),('K-Means','clusters','clusters.joblib'),('Image CNN','cnn','images.keras'),('MobileNetV2','mobilenet','mobilenetv2_waste.keras')]
    status=[]
    for label,key,file in model_rows:
        present=checks.get(file,False); state='Active' if key in loaded else ('Artifact found — not loaded' if present else 'Missing')
        status.append({'Model':label,'Status':state})
    st.dataframe(pd.DataFrame(status),use_container_width=True,hide_index=True)
    st.caption('The dashboard only marks a model Active after the application confirms it has loaded.')
