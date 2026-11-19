# Build ordered rows (one per asset+English) with all ns/key pairs, from texts.json + bytecode texts
import sys, os, re, json
sys.path.insert(0, os.path.dirname(__file__)); import pak
f, ver, mount, ents = pak.index(sys.argv[1])
texts = json.load(open(sys.argv[2]))
bcpat = re.compile(rb'\x1f([^\x00]{0,2000}?)\x00\x1f([0-9A-F]{32})\x00\x1f([^\x00]*)\x00')
for k in ['MainSelectedButton_Widget','VideoMainOptions_Widget','SelectedButton_Widget','PauseVideoOptions_Widget']:
    name = [n for n in ents if n.endswith('/'+k+'.uasset')][0]
    d = pak.extract(f, ver, ents[name])
    for m in bcpat.finditer(d):
        texts.append(dict(asset=name.replace('TheFidelioIncident/Content/',''), ns=m.group(3).decode('latin1'), key=m.group(2).decode(), en=m.group(1).decode('latin1')))
SKIP_ASSETS = ('Checkpoint_Enum','Levels_Enum','Diary_Enum','KeyBind.uasset','KeyBindingState','SubtitleText_Widget','Gameplay_Enum','Notes_Enum','EAudioType','ActionBinding_States','QualityMenu/Blueprints/util/AudioType')
rows = {}; order = []
seen = set()
for t in texts:
    if (t['ns'], t['key']) in seen: continue
    seen.add((t['ns'], t['key']))
    if any(s in t['asset'] for s in SKIP_ASSETS): continue
    if t['asset'].endswith('MyController.uasset') and (len(t['en']) <= 3 or t['en'] in ('Null','BackSpaceNUll')): continue
    if not t['en'].strip(): continue
    rk = (t['asset'], t['en'])
    if rk not in rows: rows[rk] = []; order.append(rk)
    rows[rk].append(t['ns'] + '|' + t['key'])
out = [dict(asset=a, en=e, keys=' '.join(rows[(a,e)])) for a, e in order]
json.dump(out, open(sys.argv[3], 'w'), ensure_ascii=False, indent=0)
print(len(out), 'rows;', len({r['en'].strip() for r in out}), 'unique stripped english')
