# Status das imagens traduzidas

Atualizado em 19/11/2026. As 31 páginas de `traduzidas/` estão no patch: as 29 do diário (contando as duas 26) e os 2 jornais. Todas são PNG 2048×1024 RGBA com o alfa idêntico ao original.

## Origem de cada página
| Páginas | Origem |
|---|---|
| 01, 02, 05, 06, 08, 11, 12, 13, 14, 15, 17, 18, 19, 20, 22, 23, 24, 28, 31 | Leva do app do Canvas de 18/11 |
| 26_Freedom e 26_SecurePassports | 26_SecurePassports da leva do Canvas de 18/11, usada nas duas. A 26_Freedom dessa leva tinha "asgredo" e foi descartada. |
| 09, 16, 25, 27, 29, 30 | Regeradas no app do Canvas em 19/11. Na leva de 18/11, a 09 saiu quase toda em inglês, a 16 e a 27 tinham linhas em inglês, a 25 repetia "do Stanley", a 29 duplicava uma linha e a 30 tinha "Stanley bomba"/"grass". |
| 03, 04, 07, 10 | Leva anterior, feita com o gerador de imagem do Antigravity + `composite.py`. A versão de 18/11 dessas páginas era pior. |

Não traduzidas, de propósito: 32_Manifest (formulário de carga) e 33_Map (nomes em islandês). Trocar "NORWEGIAN SEA" por "MAR DA NORUEGA" no mapa seria opcional.

## Defeitos conhecidos (cosméticos, dá para ler)
- **07_Guitar:** a 1ª linha diz "consegu" em vez de "consegue".
- **12_Killed:** "pas.sando".
- **15_MothBalls:** "embrulh…" cortado na borda.
- **25_Escape:** "anestésico" encosta na borda direita.

Para corrigir, regere a página no app do Canvas (veja o README).

## Ressalvas de qualidade
- O modelo de imagem redesenha a página inteira. A textura fica muito parecida com a original, mas a letra sai mais regular que a manuscrita, e às vezes um bloco de texto muda um pouco de lugar.
- A ênfase `[[...]]` do `GEMINI.md` nem sempre cai exatamente no trecho marcado. Na 01, por exemplo, "do caralho" saiu pequeno, e isso foi aceito.

## Histórico do processo
1. As texturas foram extraídas com `tools/textures.py`, e o texto de cada página foi traduzido e revisado no `GEMINI.md`.
2. Na primeira tentativa (páginas 01 a 10), cada página foi gerada pelo subagente de imagem do Antigravity, que devolve JPG 16:9 com margens brancas. O `composite.py` alinhava esse JPG ao papel do original e mantinha o alfa. A tentativa parou na cota do modelo e é a origem da leva anterior.
3. Depois disso, as imagens foram geradas no app "Tradutor do Diário" no Gemini Canvas (`PROMPT_CANVAS.md`). O app faz o mesmo alinhamento no navegador e permite escolher entre variações.
4. Por fim, o `tools/inject_textures.py` recodifica os PNGs em DXT e o `build.py` empacota tudo.
