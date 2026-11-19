import sys, re, os, json, struct
sys.path.insert(0, os.path.dirname(__file__))
import pak
f, ver, mount, ents = pak.index(sys.argv[1])
keypat = re.compile(rb'\x21\x00\x00\x00([0-9A-F]{32})\x00')
bcpat = re.compile(rb'\x1f[^\x00]{0,2000}?\x00\x1f([0-9A-F]{32})\x00')
out = []; bc = 0
for k, e in ents.items():
    if not k.startswith('TheFidelioIncident/Content'): continue
    if '/Textures' in k or k.endswith('.ubulk') or e['usize'] > 400e6: continue
    if not (k.endswith('.uasset') or k.endswith('.umap')): continue
    d = pak.extract(f, ver, e)
    bc += len(bcpat.findall(d))
    for m in keypat.finditer(d):
        s = m.start(); key = m.group(1).decode()
        # namespace: empty (int32 0) or "[...]" string
        if d[s-4:s] == b'\0\0\0\0': ns = ''; hs = s-4
        else:
            j = d.rfind(b'\x00', 0, s-1)  # crude: look back for length prefix
            ns = None
            for L in range(1, 200):
                if struct.unpack_from('<i', d, s-4-L)[0] == L and d[s-1] == 0:
                    ns = d[s-L:s-1].decode('latin1'); hs = s-4-L; break
            if ns is None: print('NS?', k, key, file=sys.stderr); continue
        hist = d[hs-1]; flags = struct.unpack_from('<I', d, hs-5)[0]
        src, _ = pak.rd_fstr(d, m.end())
        out.append(dict(asset=k.replace('TheFidelioIncident/Content/',''), ns=ns, key=key, en=src, hist=hist, flags=flags))
json.dump(out, open(sys.argv[2],'w'), ensure_ascii=False, indent=0)
print('texts', len(out), 'bytecode-like', bc)
