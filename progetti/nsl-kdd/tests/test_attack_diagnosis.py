import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def cell(number, tag):
    paths=list((ROOT/'notebooks').glob(f'{number}_*.ipynb'))
    assert paths, 'Manca il notebook diagnostico'
    n=json.loads(paths[0].read_text(encoding='utf-8'))
    return next(''.join(c['source']) for c in n['cells'] if tag in c.get('metadata',{}).get('tags',[]))

def test_groups_depend_only_on_training_vocabulary_and_keep_normal_separate():
    ctx=dict(pd=pd,np=np,
             train=pd.DataFrame({'attack_label':['normal','old_attack']}),
             test=pd.DataFrame({'attack_label':['normal','old_attack','new_attack']}))
    exec(cell(22,'groups'),ctx)
    assert ctx['groups'].tolist()==['Normal','Attacchi presenti nel training','Attacchi assenti dal training']

def test_group_rates_distinguish_family_classification_from_detection():
    frame=pd.DataFrame({'model':['A']*4,'family':['Normal','R2L','U2R','U2R'],
                        'group':['Normal','Attacchi presenti nel training','Attacchi assenti dal training','Attacchi assenti dal training'],
                        'predicted':['DoS','R2L','Normal','Probe']})
    ctx=dict(pd=pd,np=np,predictions=frame)
    exec(cell(22,'group_metrics'),ctx)
    novel=ctx['group_summary'].query("group=='Attacchi assenti dal training'").iloc[0]
    assert novel['support']==2 and novel['family_correct']==0
    assert novel['family_recall']==0 and novel['attack_detection_recall']==.5
    normal=ctx['group_summary'].query("group=='Normal'").iloc[0]
    assert pd.isna(normal['attack_detection_recall'])

def test_rare_attack_errors_partition_support_and_preserve_small_groups():
    frame=pd.DataFrame({'model':['A']*4,'attack':['old','new','new','normal'],
                        'family':['R2L','U2R','U2R','Normal'],
                        'predicted':['R2L','Normal','Probe','Normal'],
                        'train_support':[3,0,0,20]})
    ctx=dict(pd=pd,np=np,predictions=frame)
    exec(cell(23,'subtype_metrics'),ctx)
    table=ctx['subtype_summary'].set_index('attack')
    assert 'normal' not in table.index
    assert table.loc['old','support']==1 and table.loc['old','family_recall']==1
    assert table.loc['new','support']==2
    assert table.loc['new','family_correct']==0
    assert table.loc['new','predicted_normal']==1
    assert table.loc['new','wrong_attack_family']==1
    assert table.loc['new','train_support']==0
    assert table.loc['new','attack_detection_recall']==.5
