#!/usr/bin/env python3
"""Extrai texturas DXT1/DXT5 (UE 4.14 cooked) do pak do jogo para PNG.

Uso: python3 textures.py <jogo.pak> <pasta_saida> <filtro> [filtro...]
Salva <nome>.png e um textures.json com os metadados (para reinjeção futura).
"""
import json, os, struct, sys, zlib
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pak


def parse_texture(d):
    """Retorna dict com tamanho, formato e offsets dos mips, ou None."""
    i = d.find(b'PF_')
    i = d.find(b'PF_', i + 3)  # 1ª ocorrência é a tabela de nomes
    if i < 0:
        return None
    n = struct.unpack_from('<i', d, i - 4)[0]
    fmt = d[i:i + n - 1].decode()
    sx, sy, slices = struct.unpack_from('<3i', d, i - 16)
    o = i + n
    first_mip, nmips = struct.unpack_from('<2i', d, o); o += 8
    mips = []
    for _ in range(nmips):
        cooked, flags, count, size, off = struct.unpack_from('<IIiiq', d, o); o += 24
        mips.append(dict(data_offset=o, size=size, flags=flags))
        o += size
        mx, my = struct.unpack_from('<2i', d, o); o += 8
        mips[-1].update(w=mx, h=my)
    return dict(format=fmt, width=sx, height=sy, mips=mips)


def rgb565(c):
    r = (c >> 11) & 31; g = (c >> 5) & 63; b = c & 31
    return (r << 3 | r >> 2, g << 2 | g >> 4, b << 3 | b >> 2)


def color_palette(c0, c1, four):
    a, b = rgb565(c0), rgb565(c1)
    if four:
        return [a, b, tuple((2 * x + y) // 3 for x, y in zip(a, b)), tuple((x + 2 * y) // 3 for x, y in zip(a, b))]
    return [a, b, tuple((x + y) // 2 for x, y in zip(a, b)), (0, 0, 0)]


def decode(data, w, h, fmt):
    out = bytearray(w * h * 4)
    bsize = 16 if fmt == 'PF_DXT5' else 8
    o = 0
    for by in range(0, h, 4):
        for bx in range(0, w, 4):
            alphas = None
            if fmt == 'PF_DXT5':
                a0, a1 = data[o], data[o + 1]
                ab = int.from_bytes(data[o + 2:o + 8], 'little')
                if a0 > a1:
                    pal = [a0, a1] + [((6 - k) * a0 + (k + 1) * a1) // 7 for k in range(6)]
                else:
                    pal = [a0, a1] + [((4 - k) * a0 + (k + 1) * a1) // 5 for k in range(4)] + [0, 255]
                alphas = [pal[(ab >> (3 * k)) & 7] for k in range(16)]
                co = o + 8
            else:
                co = o
            c0, c1, idx = struct.unpack_from('<HHI', data, co)
            four = fmt == 'PF_DXT5' or c0 > c1
            cp = color_palette(c0, c1, four)
            for k in range(16):
                ci = (idx >> (2 * k)) & 3
                px, py = bx + (k & 3), by + (k >> 2)
                p = (py * w + px) * 4
                r, g, b = cp[ci]
                a = alphas[k] if alphas else (0 if (not four and ci == 3) else 255)
                out[p:p + 4] = bytes((r, g, b, a))
            o += bsize
    return out


def write_png(path, w, h, rgba):
    raw = b''.join(b'\0' + bytes(rgba[y * w * 4:(y + 1) * w * 4]) for y in range(h))
    def chunk(t, b):
        return struct.pack('>I', len(b)) + t + b + struct.pack('>I', zlib.crc32(t + b))
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(raw, 6)) + chunk(b'IEND', b'')
    open(path, 'wb').write(png)


def work(args):
    pakpath, name, outdir = args
    f, ver, mount, ents = pak.index(pakpath)
    d = pak.extract(f, ver, ents[name])
    try:
        t = parse_texture(d)
    except Exception:
        t = None
    if not t or t['format'] not in ('PF_DXT1', 'PF_DXT5'):
        return None
    m = t['mips'][0]
    rgba = decode(d[m['data_offset']:m['data_offset'] + m['size']], m['w'], m['h'], t['format'])
    png = os.path.basename(os.path.dirname(name)) + '.png'  # pasta = nome único da página
    write_png(os.path.join(outdir, png), m['w'], m['h'], rgba)
    t.update(asset=name, png=png, asset_size=len(d))
    print('ok', png, t['format'], m['w'], 'x', m['h'], len(t['mips']), 'mips', flush=True)
    return t


if __name__ == '__main__':
    pakpath, outdir, filters = sys.argv[1], sys.argv[2], sys.argv[3:]
    os.makedirs(outdir, exist_ok=True)
    f, ver, mount, ents = pak.index(pakpath)
    names = [k for k in ents if k.endswith('.uasset') and any(x in k for x in filters)]
    with Pool() as p:
        res = [r for r in p.map(work, [(pakpath, n, outdir) for n in names]) if r]
    json.dump(res, open(os.path.join(outdir, 'textures.json'), 'w'), indent=1)
    print(len(res), 'texturas extraídas')
