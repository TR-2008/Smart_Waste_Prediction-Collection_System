from pathlib import Path
import json,streamlit as st
from core.ui import apply_theme,section_header
ROOT=Path(__file__).resolve().parents[1]; apply_theme(st.session_state.get('ui_theme','Dark'))
section_header('Model Comparison','Only comparable metrics from documented held-out test sets are displayed.')
p=ROOT/'reports'/'mobilenetv2_test_metrics.json'
if p.exists():
 m=json.loads(p.read_text()); a,b,c=st.columns(3); a.metric('MobileNetV2 accuracy',f"{m['test_accuracy']:.1%}"); b.metric('Macro F1',f"{m['test_macro_f1']:.3f}"); c.metric('Test images',m['test_images']); st.write('Test loss:',round(m['test_loss'],4)); st.write('Classes:',', '.join(m['class_names']))
 st.warning('CNN test metrics were not supplied, so a fair CNN vs MobileNetV2 comparison cannot yet be shown. The MobileNetV2 report alone is not a comparison.')
else: st.info('No image-model test report found.')
p=ROOT/'reports'/'supervised_metrics.json'
if p.exists():
 d=json.loads(p.read_text()); st.markdown('### Tabular classifier · test report'); st.dataframe(d.get('test',[]),use_container_width=True,hide_index=True)
