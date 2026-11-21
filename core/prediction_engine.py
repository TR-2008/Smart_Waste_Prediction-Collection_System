from pathlib import Path
import json
import numpy as np
import pandas as pd
from PIL import Image
from core.model_loader import require_models

def read_json(path, default=None):
    p=Path(path)
    if not p.exists(): return {} if default is None else default
    return json.loads(p.read_text(encoding='utf-8'))

def predict_collection(models, model_dir, fill_pct, days_since_collection, footfall, capacity_l, location_type):
    require_models(models,'supervised','baseline')
    metadata=read_json(Path(model_dir)/'supervised_metadata.json')
    features=metadata.get('features',['fill_pct','days_since_collection','footfall','capacity_l','location_type'])
    values={'fill_pct':float(fill_pct),'days_since_collection':int(days_since_collection),'footfall':int(footfall),'capacity_l':int(capacity_l),'location_type':str(location_type)}
    unknown=[f for f in features if f not in values]
    if unknown: raise ValueError(f'Unsupported model feature(s): {unknown}')
    row=pd.DataFrame([{name:values[name] for name in features}])
    model=models['supervised']; pred=int(model.predict(row)[0]); probs=None
    if hasattr(model,'predict_proba'):
        probs=model.predict_proba(row)[0]; probs={str(int(c)):float(v) for c,v in zip(model.classes_,probs)}
    base=int(models['baseline'].predict(row)[0])
    labels=metadata.get('class_labels',{})
    return {'prediction':pred,'label':labels.get(str(pred),'Collection review' if pred else 'No collection review'),'probabilities':probs,'baseline_prediction':base,'baseline_label':'Collection review' if base else 'No collection review','features':values}

def predict_cluster(models, model_dir, fill_pct, days_since_collection, footfall, capacity_l):
    require_models(models,'clusters')
    metadata=read_json(Path(model_dir)/'cluster_metadata.json')
    features=metadata.get('features',['fill_pct','days_since_collection','footfall','capacity_l'])
    values={'fill_pct':float(fill_pct),'days_since_collection':int(days_since_collection),'footfall':int(footfall),'capacity_l':int(capacity_l)}
    row=pd.DataFrame([{n:values[n] for n in features}])
    cid=int(models['clusters'].predict(row)[0])
    return {'cluster':cid,'description':metadata.get('group_descriptions',{}).get(str(cid),'Cluster profile'),'features':values}

def prepare_image(uploaded_file):
    image=Image.open(uploaded_file).convert('RGB').resize((96,96))
    return image, np.expand_dims(np.asarray(image,dtype=np.uint8),axis=0)

def predict_material(models, image_batch, model_choice='CNN', metadata_dir=None):
    key='mobilenet' if model_choice=='MobileNetV2' else 'cnn'
    require_models(models,key)
    probs=np.asarray(models[key].predict(image_batch,verbose=0))[0]
    classes=['paper','plastic','metal']
    if len(probs)!=len(classes): raise ValueError(f'Model returned {len(probs)} scores; expected 3 classes in order paper, plastic, metal.')
    idx=int(np.argmax(probs))
    return {'model':model_choice,'class':classes[idx],'confidence':float(probs[idx]),'probabilities':{n:float(v) for n,v in zip(classes,probs)}}
