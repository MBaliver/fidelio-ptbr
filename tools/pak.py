import struct, sys, zlib, os
def rd_fstr(b, o):
    n = struct.unpack_from('<i', b, o)[0]; o += 4
    if n == 0: return '', o
    if n > 0: s = b[o:o+n-1].decode('latin1'); return s, o+n
    n = -n; s = b[o:o+2*n-2].decode('utf-16le'); return s, o+2*n
def read_entry(b, o, ver):
    off, size, usize, comp = struct.unpack_from('<qqqi', b, o); o += 28
    o += 20
    blocks = []
    if ver >= 3:
        if comp != 0:
            nb = struct.unpack_from('<i', b, o)[0]; o += 4
            for _ in range(nb):
                blocks.append(struct.unpack_from('<qq', b, o)); o += 16
        enc, bs = struct.unpack_from('<BI', b, o); o += 5
    else: enc = 0; bs = 0
    return dict(off=off,size=size,usize=usize,comp=comp,blocks=blocks,enc=enc,bs=bs), o
def index(path):
    f = open(path,'rb'); f.seek(-44, 2); ft = f.read(44)
    magic, ver, io, isz = struct.unpack_from('<IIqq', ft)
    assert magic == 0x5A6F12E1, hex(magic)
    f.seek(io); b = f.read(isz)
    mount, o = rd_fstr(b, 0); n = struct.unpack_from('<i', b, o)[0]; o += 4
    ents = {}
    for _ in range(n):
        name, o = rd_fstr(b, o); e, o = read_entry(b, o, ver); ents[name] = e
    return f, ver, mount, ents
def extract(f, ver, e):
    # in-data header: same entry struct repeated before data
    f.seek(e['off']); hdr = f.read(1024)
    _, hl = read_entry(hdr, 0, ver)
    if e['enc']: raise Exception('encrypted')
    if e['comp'] == 0:
        f.seek(e['off']+hl); return f.read(e['size'])
    out = b''
    for s, en in e['blocks']:
        # v3+: block offsets are absolute in older versions
        f.seek(s); out += zlib.decompress(f.read(en-s))
    return out
if __name__ == '__main__':
    f, ver, mount, ents = index(sys.argv[1])
    cmd = sys.argv[2]
    if cmd == 'ls':
        print('mount', mount, 'count', len(ents))
        for k in ents:
            if not sys.argv[3:] or any(p.lower() in k.lower() for p in sys.argv[3:]): print(k, ents[k]['usize'], ents[k]['comp'], ents[k]['enc'])
    elif cmd == 'x':
        outdir = sys.argv[3]
        for k in ents:
            if any(p.lower() in k.lower() for p in sys.argv[4:]):
                d = extract(f, ver, ents[k]); p = os.path.join(outdir, k); os.makedirs(os.path.dirname(p), exist_ok=True); open(p,'wb').write(d); print('x', k, len(d))
