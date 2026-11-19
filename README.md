# The Fidelio Incident — tradução PT-BR

Tradução não oficial para português do Brasil de *The Fidelio Incident* (Unreal Engine 4.14, versão Steam/Windows rodando via Proton).

Cobre legendas, menus, cartas, créditos, as 29 páginas manuscritas do diário da Leonore e os 2 recortes de jornal. Também inclui fontes com acentos.
Fica em inglês: a narração do diário (o jogo não tem legendas para ela), o formulário de carga (32_Manifest) e o mapa (33_Map).

O patch é um pak separado (`TheFidelioIncident-WindowsNoEditor_ptBR_P.pak`). Os arquivos originais do jogo não são alterados: para desinstalar, basta apagar esse pak.

## Uso rápido
```sh
python3 -m venv .venv && .venv/bin/pip install numpy pillow   # só na primeira vez
PAK="$HOME/.local/share/Steam/steamapps/common/The Fidelio Incident/TheFidelioIncident/Content/Paks/TheFidelioIncident-WindowsNoEditor.pak"
.venv/bin/python tools/inject_textures.py "$PAK" imagens/traduzidas texturas   # imagens -> texturas/
python3 build.py              # gera dist/…_ptBR_P.pak e instala na pasta do jogo
python3 build.py --no-install # só gera
python3 build.py --uninstall  # remove o patch do jogo
```
`dist/` e `texturas/` são gerados e não vão para o git. Rode o `inject_textures.py` sempre que mudar alguma imagem em `imagens/traduzidas/`.

## Estrutura
| Caminho | O que é |
|---|---|
| `textos_en_pt.csv` | Todos os textos (inglês x português). Edite a coluna **portugues**; se ficar vazia, o texto continua em inglês. Não mexa em `chaves`. |
| `build.py` | Monta o `Game.locres` (culturas en, pt e pt-BR) a partir do CSV. Empacota o locres, `fontes/` e `texturas/` num pak v3 sem compressão e instala. |
| `fontes/` | `.uasset` das fontes manuscritas já com os acentos desenhados. `amostra.png` mostra o resultado. |
| `imagens/traduzidas/` | **As imagens que vão para o jogo** (PNG 2048×1024 RGBA, alfa do original). Só as páginas presentes nessa pasta são trocadas no jogo. |
| `imagens/originais/textures.json` | Metadados das 33 texturas (asset, formato DXT1/DXT5, offsets dos mips), usados pela reinjeção. |
| `imagens/GEMINI.md` | Texto traduzido e revisado de cada página, mais o prompt de edição e as decisões de tradução. É a referência para conferir as imagens. |
| `imagens/PROMPT_CANVAS.md` | Prompt que cria no Gemini Canvas o app "Tradutor do Diário", usado para gerar as imagens. |
| `imagens/STATUS.md` | Origem de cada página traduzida, defeitos conhecidos e histórico do processo. |
| `imagens/composite.py` | Alinha uma imagem gerada (16:9, sem alfa) ao papel do original e mantém o alfa. É usado pelo `gemini_batch.py`. |
| `tools/pak.py` | Leitura do índice e extração de arquivos do pak do jogo. |
| `tools/textures.py` | Extrai as texturas do pak para PNG e gera o `textures.json`. |
| `tools/inject_textures.py` | Recodifica os PNGs em DXT1/DXT5 (todos os mips) dentro do `.uasset` original e grava em `texturas/`. |
| `tools/fonts.py` | Adiciona os acentos às fontes manuscritas (precisa de `fonttools`). |
| `tools/gemini_batch.py` | Alternativa via API do Gemini (`GEMINI_API_KEY`) para gerar as imagens em lote. |
| `tools/extract.py`, `tools/build_rows.py` | Usados uma vez para levantar os textos do jogo e montar o CSV. |

## Textos
O jogo procura `Content/Localization/Game/<cultura>/Game.locres`. O `build.py` gera esse arquivo com chave + hash do texto em inglês para cada tradução. Também preserva os espaços nas pontas, porque o jogo concatena alguns trechos.

## Fontes (acentos)
A fonte manuscrita "CF I Dont Want to Grow Up" não tinha nenhum acento, então essas letras sumiam. Ela aparece nos assets `GrowUp` e `CFIDONTWANTTOGROWUP-REGULAR` (cartas da prisão, diário e menu de pausa).
O `tools/fonts.py` desenha ´ ` ^ ~ ¸ no traço da fonte, cria as letras acentuadas (á à â ã é ê í ó ô õ ú ç, também em maiúsculas) e regrava os `.uasset` em `fontes/`.
- Regerar: `pip install fonttools` e depois `python3 tools/fonts.py "$PAK" fontes`.
- As demais fontes já têm acentos. A Darkwoman ("Pressione Esc…", "Segure Shift…") não tem ã, õ nem ç, mas esses textos não usam essas letras.

## Imagens (diário e jornais)
- **Originais:** não vão para o git porque são arquivos do jogo. Para extraí-las de novo para `imagens/originais/`, nomeadas pela pasta do asset:
  `.venv/bin/python tools/textures.py "$PAK" imagens/originais Notes/Diary/`
- **Formato:** diários em DXT5 com transparência e jornais (11 e 17) em DXT1 opacos. As páginas 05, 09, 32 e 33 têm 12 mips.
- **26_Freedom e 26_SecurePassports:** são a mesma imagem, então use o mesmo PNG para as duas. Não existe página 21.
- **Para refazer uma página:**
  1. Abra o app do Canvas (`PROMPT_CANVAS.md`), carregue o `GEMINI.md` e o PNG original.
  2. Confira se o texto do card é o do `GEMINI.md`, e não uma tradução automática.
  3. Gere 2 a 4 variações, escolha uma e confira o resultado no zoom 100%.
  4. Baixe o PNG em `imagens/traduzidas/` com o mesmo nome.
  5. Rode `inject_textures.py` e `build.py`.
- **Ao validar:** confira se o PNG é 2048×1024 RGBA com o alfa igual ao do original. Leia também o texto contra o `GEMINI.md`, procurando palavras em inglês, linhas duplicadas, acentos e palavras cortadas na borda.
