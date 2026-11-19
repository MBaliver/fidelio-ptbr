#!/usr/bin/env python3
"""Adiciona letras acentuadas às fontes manuscritas do jogo que não as têm.

Uso: python3 tools/fonts.py <pak do jogo> <pasta de saída>
Requer fontTools (pip install fonttools).

A fonte "CF I Dont Want to Grow Up" (assets GrowUp e CFIDONTWANTTOGROWUP-REGULAR,
usada nas cartas da prisão, no diário e no menu de pausa) não tem nenhum
acento. Este script desenha os acentos (´ ` ^ ~ ¸) como traços de caneta com a
espessura da fonte, monta as letras acentuadas como glifos compostos
(base + acento, herdando o kerning da base) e regrava o .uasset com a TTF nova.
Os .uasset gerados vão para a pasta de saída e o build.py os inclui no pak.

Formato do .uasset (UE 4.14, UFont com CompositeFont): a TTF fica num
FUntypedBulkData no fim do arquivo, comprimida em zlib:
  [flags u32][qtd. elementos i32][tamanho em disco i32][offset i64]
  [tag 0x9E2A83C1 i64][tam. do bloco i64][total comp i64][total descomp i64]
  ([comp i64][descomp i64] por bloco) (zlib por bloco)
  ... e o arquivo termina com a tag do pacote (4 bytes).
"""
import io, math, os, struct, sys, zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pak

TAG = 0x9E2A83C1
CHUNK = 131072
ASSETS = ['TheFidelioIncident/Content/Menu/MainMenu/Font/GrowUp.uasset',
          'TheFidelioIncident/Content/Menu/MainMenu/Font/CFIDONTWANTTOGROWUP-REGULAR.uasset']


# ---------------------------------------------------------------- uasset
def _find_bulk(d):
    tag = struct.pack('<q', TAG)
    i = d.find(tag, 4)
    while i >= 0:
        h = i - 20
        flags, count, size, off = struct.unpack_from('<IiiQ', d, h)
        if i + size + 4 == len(d) and flags & 2:
            return h, i, flags, off
        i = d.find(tag, i + 1)
    raise ValueError('bulk data da fonte não encontrado')


def font_from_uasset(d):
    h, i, flags, off = _find_bulk(d)
    _, chunk, csz, usz = struct.unpack_from('<qqqq', d, i)
    n = (usz + chunk - 1) // chunk
    o = i + 32 + 16 * n
    out = b''
    for k in range(n):
        c, _ = struct.unpack_from('<qq', d, i + 32 + 16 * k)
        out += zlib.decompress(d[o:o + c]); o += c
    assert len(out) == usz
    return out


def uasset_with_font(d, ttf):
    h, i, flags, off = _find_bulk(d)
    chunks = [zlib.compress(ttf[k:k + CHUNK], 9) for k in range(0, len(ttf), CHUNK)]
    body = struct.pack('<qqqq', TAG, CHUNK, sum(map(len, chunks)), len(ttf))
    for k, c in enumerate(chunks):
        body += struct.pack('<qq', len(c), len(ttf[k * CHUNK:(k + 1) * CHUNK]))
    body += b''.join(chunks)
    return d[:h] + struct.pack('<IiiQ', flags, len(ttf), len(body), off) + body + d[-4:]


# ---------------------------------------------------------------- acentos
W = 78  # espessura média do traço da fonte (unidades de 1000/em)


def stroke(path, w=W, steps=40):
    """Contorno (pontos on-curve, sentido horário) de um traço de caneta ao
    longo de uma curva cúbica/polilinha, com pontas arredondadas e leve
    variação de espessura, imitando o marcador da fonte."""
    def bez(p, t):
        if len(p) == 2:
            return (p[0][0] + (p[1][0] - p[0][0]) * t, p[0][1] + (p[1][1] - p[0][1]) * t)
        a, b, c, e = p
        u = 1 - t
        return tuple(u**3 * a[k] + 3*u*u*t * b[k] + 3*u*t*t * c[k] + t**3 * e[k] for k in (0, 1))
    pts = [bez(path, s / steps) for s in range(steps + 1)]
    L, R = [], []
    for k, (x, y) in enumerate(pts):
        a = pts[max(k - 1, 0)]; b = pts[min(k + 1, len(pts) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; n = math.hypot(dx, dy) or 1
        t = k / steps
        r = w / 2 * (0.88 + 0.22 * math.sin(math.pi * t))  # mais grosso no meio
        nx, ny = -dy / n * r, dx / n * r
        L.append((x + nx, y + ny)); R.append((x - nx, y - ny))

    def cap(c, frm, to):
        a0 = math.atan2(frm[1] - c[1], frm[0] - c[0]); r = math.hypot(frm[0] - c[0], frm[1] - c[1])
        return [(c[0] + r * math.cos(a0 - math.pi * s / 8), c[1] + r * math.sin(a0 - math.pi * s / 8))
                for s in range(1, 8)]
    ring = L + cap(pts[-1], L[-1], R[-1]) + R[::-1] + cap(pts[0], R[0], L[0])
    # sentido horário (TrueType)
    area = sum(ring[k][0] * ring[k - 1][1] - ring[k - 1][0] * ring[k][1] for k in range(len(ring)))
    if area < 0:
        ring = ring[::-1]
    return [(round(x), round(y)) for x, y in ring]


def accent_shapes(cap):
    """Acentos centrados em x=0 com a base em y=0 (s = escala para maiúsculas)."""
    s = 0.8 if cap else 1.0
    S = lambda pts: [(x * s, y * s) for x, y in pts]
    return {
        'acute': [stroke(S([(-45, 0), (-10, 45), (25, 95), (60, 150)]))],
        'grave': [stroke(S([(45, 0), (10, 45), (-25, 95), (-60, 150)]))],
        'circumflex': [stroke(S([(-115, 0), (-75, 50), (-35, 100), (0, 140)])),
                       stroke(S([(0, 140), (35, 100), (75, 50), (115, 0)]))],
        'tilde': [stroke(S([(-125, 15), (-70, 115), (0, 0), (60, 95)]), w=W * 0.9),
                  stroke(S([(55, 90), (85, 125), (110, 125), (125, 100)]), w=W * 0.9)],
        'cedilla': [stroke([(0, 30), (0, -30), (5, -60), (15, -75)], w=W * 0.85),
                    stroke([(15, -75), (95, -85), (90, -170), (-40, -175)], w=W * 0.85)],
    }


# letra -> (base, acento)
COMPOSE = {}
for base in 'aeiouAEIOU':
    COMPOSE[{'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú', 'A': 'Á', 'E': 'É', 'I': 'Í', 'O': 'Ó', 'U': 'Ú'}[base]] = (base, 'acute')
    COMPOSE[{'a': 'à', 'e': 'è', 'i': 'ì', 'o': 'ò', 'u': 'ù', 'A': 'À', 'E': 'È', 'I': 'Ì', 'O': 'Ò', 'U': 'Ù'}[base]] = (base, 'grave')
    COMPOSE[{'a': 'â', 'e': 'ê', 'i': 'î', 'o': 'ô', 'u': 'û', 'A': 'Â', 'E': 'Ê', 'I': 'Î', 'O': 'Ô', 'U': 'Û'}[base]] = (base, 'circumflex')
for base, ch in zip('aoAOnN', 'ãõÃÕñÑ'):
    COMPOSE[ch] = (base, 'tilde')
COMPOSE['ç'] = ('c', 'cedilla'); COMPOSE['Ç'] = ('C', 'cedilla')


def add_accents(ttf):
    from fontTools.ttLib import TTFont
    from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphComponent, GlyphCoordinates
    from fontTools.ttLib.tables import ttProgram

    f = TTFont(io.BytesIO(ttf))
    glyf, hmtx = f['glyf'], f['hmtx']
    cmap = f.getBestCmap()
    order = list(f.getGlyphOrder())

    def simple(contours):
        g = Glyph(); coords = []; ends = []
        for c in contours:
            coords += c; ends.append(len(coords) - 1)
        g.coordinates = GlyphCoordinates(coords); g.endPtsOfContours = ends
        g.flags = bytearray([1] * len(coords)); g.numberOfContours = len(ends)
        g.program = ttProgram.Program(); g.program.fromBytecode(b'')
        g.recalcBounds(glyf)
        return g

    def add(name, g, adv, lsb=None):
        glyf[name] = g
        if name not in order:
            order.append(name)
        g.recalcBounds(glyf)
        hmtx[name] = (adv, g.xMin if lsb is None else lsb)

    # i sem pingo: tira o contorno mais alto (o pingo) do i original
    gi = glyf['i']; co = gi.getCoordinates(glyf)[0]; s = 0; parts = []
    for e in gi.endPtsOfContours:
        parts.append(list(co[s:e + 1])); s = e + 1
    top = max(range(len(parts)), key=lambda k: min(p[1] for p in parts[k]))
    add('dotlessi', simple([p for k, p in enumerate(parts) if k != top]), hmtx['i'][0])

    for cap in (False, True):
        for name, contours in accent_shapes(cap).items():
            add(name + ('.cap' if cap else ''), simple(contours), 0)

    kern = f['kern'].kernTables[0].kernTable if 'kern' in f else {}
    new_kern = {}
    for ch, (base, acc) in COMPOSE.items():
        if ord(ch) in cmap or base not in glyf:
            continue
        bg = glyf['dotlessi' if base == 'i' else base]
        is_cap = base.isupper()
        acc_name = acc + ('.cap' if is_cap and acc != 'cedilla' else '')
        ag = glyf[acc_name]
        cx = (bg.xMin + bg.xMax) // 2
        if acc == 'cedilla':
            dx, dy = cx, max(bg.yMin, 0)
        else:
            dx, dy = cx + (12 if not is_cap else 8), bg.yMax + (55 if not is_cap else 45)
        comps = []
        for gname, x, y in (('dotlessi' if base == 'i' else base, 0, 0), (acc_name, dx, dy)):
            c = GlyphComponent(); c.glyphName = gname; c.x, c.y = x, y; c.flags = 0
            comps.append(c)
        comps[0].flags = 0x0200  # USE_MY_METRICS
        g = Glyph(); g.numberOfContours = -1; g.components = comps
        gname = 'uni%04X' % ord(ch)
        glyf[gname] = g; order.append(gname)
        g.recalcBounds(glyf)
        hmtx[gname] = (hmtx[base][0], g.xMin)
        for t in f['cmap'].tables:
            if t.isUnicode() or (t.platformID == 1 and ord(ch) < 256):
                if t.platformID == 1:
                    # Mac Roman: só os códigos que existem nessa codificação
                    try:
                        code = ch.encode('mac_roman')[0]
                    except UnicodeEncodeError:
                        continue
                    t.cmap[code] = gname
                else:
                    t.cmap[ord(ch)] = gname
        for (l, r), v in kern.items():
            if l == base: new_kern[(gname, r)] = v
            if r == base: new_kern[(l, gname)] = v
    for (l, r), v in list(new_kern.items()):
        kern.setdefault((l, r), v)

    f.setGlyphOrder(order)
    f['maxp'].numGlyphs = len(order)
    f['post'].extraNames = []; f['post'].mapping = {}
    out = io.BytesIO(); f.save(out)
    return out.getvalue()


def main():
    game_pak, out_dir = sys.argv[1], sys.argv[2]
    fh, ver, mount, ents = pak.index(game_pak)
    for a in ASSETS:
        d = pak.extract(fh, ver, ents[a])
        new = uasset_with_font(d, add_accents(font_from_uasset(d)))
        assert font_from_uasset(new)  # relê para conferir
        dst = os.path.join(out_dir, a)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'wb').write(new)
        print(a, len(d), '->', len(new))


if __name__ == '__main__':
    main()
