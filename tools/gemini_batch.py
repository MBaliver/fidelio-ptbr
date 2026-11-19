#!/usr/bin/env python3
"""Traduz as imagens do diário pela API do Gemini, usando o prompt e os textos de imagens/GEMINI.md.

Uso:
  GEMINI_API_KEY=... python3 tools/gemini_batch.py [páginas...]   (ex.: 09_Michael 12_Killed)
Sem argumentos, processa todas as páginas do GEMINI.md que ainda não estão em imagens/traduzidas/.
Opções: --model NOME (padrão gemini-3.1-flash-image), --force (refaz mesmo se já existir),
        --tries N (tentativas por página, guarda todas como _v1, _v2...; padrão 1).
Só usa a biblioteca padrão. A saída do modelo (16:9, sem alfa) passa por imagens/composite.py,
que alinha ao papel do original e mantém o alfa; a imagem bruta fica ao lado como <nome>.png.gerado.
"""
import base64, json, os, re, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(HERE, 'imagens', 'GEMINI.md')
SRC = os.path.join(HERE, 'imagens', 'originais')
DST = os.path.join(HERE, 'imagens', 'traduzidas')
API = 'https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent'


def parse_md():
    text = open(MD, encoding='utf-8').read()
    prompt = re.search(r'## Prompt\s*```\n(.*?)```', text, re.S).group(1)
    pages = {}
    for m in re.finditer(r'^## (\d\d_\w+)[^\n]*\n```\n(.*?)```', text, re.S | re.M):
        pages[m.group(1)] = m.group(2).rstrip('\n')
    return prompt, pages


def call(model, key, prompt, png):
    body = {
        'contents': [{'parts': [
            {'text': prompt},
            {'inline_data': {'mime_type': 'image/png', 'data': base64.b64encode(png).decode()}},
        ]}],
        'generationConfig': {'responseModalities': ['IMAGE', 'TEXT']},
    }
    req = urllib.request.Request(API.format(model), json.dumps(body).encode(),
                                 {'Content-Type': 'application/json', 'x-goog-api-key': key})
    with urllib.request.urlopen(req, timeout=300) as r:
        resp = json.load(r)
    for cand in resp.get('candidates', []):
        for part in cand.get('content', {}).get('parts', []):
            data = part.get('inlineData') or part.get('inline_data')
            if data:
                return base64.b64decode(data['data'])
    raise RuntimeError('sem imagem na resposta: ' + json.dumps(resp)[:500])


def fit(name, raw, path):
    """Alinha a saída do modelo ao papel do original e preserva o alfa (imagens/composite.py)."""
    import subprocess
    gen = path + '.gerado'
    open(gen, 'wb').write(raw)
    subprocess.run([sys.executable, os.path.join(HERE, 'imagens', 'composite.py'),
                    os.path.join(SRC, name + '.png'), gen, path], check=True)


def main():
    args = sys.argv[1:]
    model, force, tries = 'gemini-3.1-flash-image', False, 1
    if '--model' in args:
        i = args.index('--model'); model = args[i + 1]; del args[i:i + 2]
    if '--tries' in args:
        i = args.index('--tries'); tries = int(args[i + 1]); del args[i:i + 2]
    if '--force' in args:
        args.remove('--force'); force = True
    key = os.environ.get('GEMINI_API_KEY')
    if not key:
        sys.exit('defina GEMINI_API_KEY')
    prompt, pages = parse_md()
    names = args or sorted(pages)
    os.makedirs(DST, exist_ok=True)
    for name in names:
        if name not in pages:
            print('?', name, 'não está no GEMINI.md'); continue
        out = os.path.join(DST, name + '.png')
        if os.path.exists(out) and not force:
            print('=', name, '(já existe)'); continue
        png = open(os.path.join(SRC, name + '.png'), 'rb').read()
        # O modelo desenha os colchetes: manda o texto limpo e os destaques à parte.
        text = pages[name]
        emph = re.findall(r'\[\[(.+?)\]\]', text)
        clean = re.sub(r'\[\[|\]\]|\[|\]', '', text)
        full = prompt.replace('[TEXTO DA PÁGINA]', clean)
        full = full.replace(
            'Output only the edited image.',
            'EMPHASIS (write these exact phrases larger, where the original has its larger words; '
            'they already appear in the text above):\n'
            + ('\n'.join(f'"{e}"' for e in emph) or '(none)')
            + '\n\nOutput only the edited image. Never draw brackets or the word EMPHASIS.')
        for t in range(1, tries + 1):
            path = out if tries == 1 else os.path.join(DST, f'{name}_v{t}.png')
            for attempt in range(3):
                try:
                    img = call(model, key, full, png); break
                except urllib.error.HTTPError as e:
                    msg = e.read().decode()[:300]
                    if e.code == 429 and attempt < 2:
                        print('  limite, aguardando 60s'); time.sleep(60); continue
                    sys.exit(f'{name}: HTTP {e.code} {msg}')
            fit(name, img, path)
            print('+', os.path.relpath(path, HERE))
    if '26_Freedom' in names and os.path.exists(os.path.join(DST, '26_Freedom.png')):
        import shutil
        shutil.copy(os.path.join(DST, '26_Freedom.png'), os.path.join(DST, '26_SecurePassports.png'))


if __name__ == '__main__':
    main()
