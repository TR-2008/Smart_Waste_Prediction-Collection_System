import streamlit as st
from core.ui import apply_theme,section_header
from core.settings_manager import load_settings,save_settings
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; current=load_settings(); apply_theme(current['theme'])
section_header('System Settings','Preferences are saved locally and applied after restart/rerun.')
with st.form('settings'):
 mode=st.radio('Operating mode',['Manual','Advanced'],index=['Manual','Advanced'].index(current['system_mode']),horizontal=True)
 theme=st.radio('Appearance',['Dark','Light'],index=['Dark','Light'].index(current['theme']),horizontal=True)
 model=st.selectbox('Default image classifier',['CNN','MobileNetV2'],index=['CNN','MobileNetV2'].index(current['image_model']))
 summary=st.selectbox('AI summary provider',['Offline','Groq'],index=['Offline','Groq'].index(current['summary_mode']))
 layout=st.selectbox('Dashboard layout',['Expanded','Compact'],index=['Expanded','Compact'].index(current['dashboard_layout']))
 notifications=st.checkbox('Enable in-app notifications',value=current['notifications'])
 auto=st.checkbox('Load available model artifacts when required',value=current['auto_model_loading'])
 submit=st.form_submit_button('Save settings',type='primary')
if submit:
    saved=save_settings({'system_mode':mode,'theme':theme,'image_model':model,'summary_mode':summary,'dashboard_layout':layout,'notifications':notifications,'auto_model_loading':auto})
    for k,v in {'operating_mode':mode,'ui_theme':theme,'image_model_choice':model}.items(): st.session_state[k]=v
    st.success('Settings saved. The workspace is refreshing with the selected preferences.'); st.rerun()
st.info('Groq API integration is not included yet. If enabled later, keep its API key in Streamlit secrets; never paste it into source code.')
