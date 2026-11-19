#!/usr/bin/env python3
"""Gera o patch PT-BR de The Fidelio Incident a partir de textos_en_pt.csv.

Uso:
  python3 build.py            # gera e instala o pak na pasta do jogo
  python3 build.py --no-install
  python3 build.py --uninstall

Como funciona: o jogo (Unreal Engine 4.14) procura arquivos .locres em
Content/Localization/Game/<cultura>/. Este script cria um Game.locres com as
traduções (chave + hash do texto original em inglês) e o empacota num pak
"_P" separado, que o jogo carrega por cima do original. Nenhum arquivo
original é modificado; para desinstalar basta apagar o pak.
"""
import csv, hashlib, os, struct, sys, zlib
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, 'textos_en_pt.csv')
FONTES = os.path.join(HERE, 'fontes')
TEXTURAS = os.path.join(HERE, 'texturas')
OUT = os.path.join(HERE, 'dist', 'TheFidelioIncident-WindowsNoEditor_ptBR_P.pak')
GAME_PAKS = os.path.expanduser(
    '~/.local/share/Steam/steamapps/common/The Fidelio Incident/TheFidelioIncident/Content/Paks')
# Cultura "en" sobrescreve o inglês nativo; pt/pt-BR cobrem o caso de o jogo
# detectar o idioma do sistema como português.
CULTURES = ['en', 'pt', 'pt-BR']


def fstr(s):
    if s == '':
        return struct.pack('<i', 0)
    try:
        b = s.encode('ascii') + b'\0'
        return struct.pack('<i', len(b)) + b
    except UnicodeEncodeError:
        b = s.encode('utf-16-le') + b'\0\0'
        return struct.pack('<i', -(len(b) // 2)) + b


def load_rows():
    table = defaultdict(dict)  # ns -> key -> (hash, text)
    n = 0
    with open(CSV, encoding='utf-8-sig', newline='') as f:
        for row in csv.DictReader(f):
            en, pt = row['ingles'], row['portugues']
            if not pt.strip():
                continue  # vazio = mantém o inglês
            # preserva espaços nas pontas (o jogo concatena alguns trechos)
            lead = en[:len(en) - len(en.lstrip())]
            trail = en[len(en.rstrip()):]
            text = lead + pt.strip() + trail
            for item in row['chaves'].split():
                ns, key, h = item.rsplit('|', 2)
                table[ns][key] = (int(h, 16), text)
                n += 1
    return table, n


def build_locres(table):
    out = struct.pack('<i', len(table))
    for ns, keys in table.items():
        out += fstr(ns) + struct.pack('<i', len(keys))
        for key, (h, text) in keys.items():
            out += fstr(key) + struct.pack('<I', h) + fstr(text)
    return out


def pak_entry(offset, data):
    # FPakEntry v3, sem compressão nem criptografia
    return (struct.pack('<qqqi', offset, len(data), len(data), 0)
            + hashlib.sha1(data).digest() + struct.pack('<BI', 0, 0))


def build_pak(files):
    body = b''
    index_entries = b''
    for path, data in files:
        off = len(body)
        body += pak_entry(0, data) + data
        index_entries += fstr(path) + pak_entry(off, data)
    index = fstr('../../../') + struct.pack('<i', len(files)) + index_entries
    footer = struct.pack('<IIqq', 0x5A6F12E1, 3, len(body), len(index)) + hashlib.sha1(index).digest()
    return body + index + footer


def main():
    if '--uninstall' in sys.argv:
        p = os.path.join(GAME_PAKS, os.path.basename(OUT))
        if os.path.exists(p):
            os.remove(p); print('Removido:', p)
        else:
            print('Nada instalado.')
        return
    table, n = load_rows()
    locres = build_locres(table)
    files = [(f'TheFidelioIncident/Content/Localization/Game/{c}/Game.locres', locres) for c in CULTURES]
    # fontes com acentos (tools/fonts.py) e texturas traduzidas (tools/inject_textures.py)
    # substituem as originais
    n_assets = {}
    for base in (FONTES, TEXTURAS):
        n_assets[base] = 0
        for root, _, names in os.walk(base):
            for name in names:
                if name.endswith('.uasset'):
                    p = os.path.join(root, name)
                    with open(p, 'rb') as fh:
                        files.append((os.path.relpath(p, base).replace(os.sep, '/'), fh.read()))
                    n_assets[base] += 1
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'wb') as f:
        f.write(build_pak(files))
    print(f'{n} textos traduzidos, {n_assets[FONTES]} fontes, {n_assets[TEXTURAS]} texturas -> {OUT}')
    if '--no-install' not in sys.argv:
        dst = os.path.join(GAME_PAKS, os.path.basename(OUT))
        with open(OUT, 'rb') as s, open(dst, 'wb') as d:
            d.write(s.read())
        print('Instalado em:', dst)


if __name__ == '__main__':
    main()
