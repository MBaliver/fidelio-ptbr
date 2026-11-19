#!/usr/bin/env python3
"""Reinjeta as texturas traduzidas (PNG 2048x1024 RGBA) nos .uasset do jogo.

Uso: python3 tools/inject_textures.py <jogo.pak> <pasta_png> <pasta_saida>
  ex.: .venv/bin/python tools/inject_textures.py "$PAK" imagens/traduzidas texturas

Para cada PNG de <pasta_png> que esteja em imagens/originais/textures.json, extrai o
.uasset original do pak, recodifica todos os mips em DXT1/DXT5 (mesmo formato e tamanho)
e grava o .uasset em <pasta_saida>/<caminho no pak>. O build.py inclui essa pasta no patch.
A pasta de saída é limpa antes, então só vão para o patch as páginas presentes em <pasta_png>.
Precisa de numpy e Pillow (pip install numpy pillow).
"""
import json, os, shutil, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pak

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = os.path.join(HERE, 'imagens', 'originais', 'textures.json')


def blocks(img):
    """(H, W, C) -> (nblocos, 16, C), blocos 4x4 em ordem de linha."""
    h, w, c = img.shape
    return img.reshape(h // 4, 4, w // 4, 4, c).transpose(0, 2, 1, 3, 4).reshape(-1, 16, c)


def to565(c):
    c = np.clip(np.rint(c), 0, 255).astype(np.uint32)
    return ((c[..., 0] >> 3) << 11) | ((c[..., 1] >> 2) << 5) | (c[..., 2] >> 3)


def from565(v):
    r = (v >> 11) & 31; g = (v >> 5) & 63; b = v & 31
    return np.stack([(r << 3) | (r >> 2), (g << 2) | (g >> 4), (b << 3) | (b >> 2)], -1).astype(np.float32)


def encode_color(px):
    """px: (n, 16, 3) float -> (n, 8) bytes de bloco DXT1 (modo 4 cores)."""
    mean = px.mean(1, keepdims=True)
    d = px - mean
    cov = np.einsum('nki,nkj->nij', d, d)
    axis = np.ones((len(px), 3), np.float32)
    for _ in range(8):  # iteração de potência: eixo principal
        axis = np.einsum('nij,nj->ni', cov, axis)
        axis /= np.maximum(np.linalg.norm(axis, axis=1, keepdims=True), 1e-6)
    t = np.einsum('nki,ni->nk', d, axis)
    lo = mean[:, 0] + axis * t.min(1, keepdims=True)
    hi = mean[:, 0] + axis * t.max(1, keepdims=True)
    c0, c1 = to565(hi), to565(lo)
    swap = c0 < c1
    c0, c1 = np.where(swap, c1, c0), np.where(swap, c0, c1)
    e0, e1 = from565(c0), from565(c1)
    pal = np.stack([e0, e1, (2 * e0 + e1) / 3, (e0 + 2 * e1) / 3], 1)  # (n, 4, 3)
    dist = ((px[:, :, None, :] - pal[:, None, :, :]) ** 2).sum(-1)
    idx = dist.argmin(2).astype(np.uint32)
    idx[c0 == c1] = 0  # cor única: evita o modo 3 cores (índice 3 = transparente)
    bits = (idx << (2 * np.arange(16, dtype=np.uint32))).sum(1, dtype=np.uint64).astype(np.uint32)
    out = np.zeros((len(px), 8), np.uint8)
    out[:, 0:2] = c0.astype('<u2').view(np.uint8).reshape(-1, 2)
    out[:, 2:4] = c1.astype('<u2').view(np.uint8).reshape(-1, 2)
    out[:, 4:8] = bits.astype('<u4').view(np.uint8).reshape(-1, 4)
    return out


def encode_alpha(a):
    """a: (n, 16) -> (n, 8) bytes de bloco de alfa DXT5 (modo 8 valores)."""
    a0 = a.max(1).astype(np.int32); a1 = a.min(1).astype(np.int32)
    k = np.arange(1, 7)
    pal = np.concatenate([a0[:, None], a1[:, None],
                          ((7 - k) * a0[:, None] + k * a1[:, None]) // 7], 1)
    idx = np.abs(a[:, :, None].astype(np.int32) - pal[:, None, :]).argmin(2).astype(np.uint64)
    idx[a0 == a1] = 0
    bits = (idx << (3 * np.arange(16, dtype=np.uint64))).sum(1, dtype=np.uint64)
    out = np.zeros((len(a), 8), np.uint8)
    out[:, 0] = a0; out[:, 1] = a1
    out[:, 2:8] = bits.astype('<u8').view(np.uint8).reshape(-1, 8)[:, :6]
    return out


def encode(rgba, fmt):
    h, w = rgba.shape[:2]
    ph, pw = -h % 4, -w % 4
    if ph or pw:
        rgba = np.pad(rgba, ((0, ph), (0, pw), (0, 0)), mode='edge')
    b = blocks(rgba.astype(np.float32))
    col = encode_color(b[..., :3])
    if fmt == 'PF_DXT1':
        return col.tobytes()
    return np.concatenate([encode_alpha(b[..., 3].astype(np.uint8)), col], 1).tobytes()


def main():
    pakpath, src, out = sys.argv[1:4]
    meta = json.load(open(META))
    f, ver, mount, ents = pak.index(pakpath)
    if os.path.isdir(out):
        shutil.rmtree(out)
    n = 0
    for t in meta:
        p = os.path.join(src, t['png'])
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert('RGBA')
        assert im.size == (t['width'], t['height']), (p, im.size)
        d = bytearray(pak.extract(f, ver, ents[t['asset']]))
        assert len(d) == t['asset_size'], t['asset']
        for m in t['mips']:
            mip = im if (m['w'], m['h']) == im.size else im.resize((m['w'], m['h']), Image.LANCZOS)
            data = encode(np.asarray(mip), t['format'])
            assert len(data) == m['size'], (t['png'], m, len(data))
            d[m['data_offset']:m['data_offset'] + m['size']] = data
        dst = os.path.join(out, t['asset'])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'wb').write(d)
        n += 1
        print('ok', t['png'], t['format'], len(t['mips']), 'mip(s)', flush=True)
    print(n, 'texturas ->', out)


if __name__ == '__main__':
    main()
