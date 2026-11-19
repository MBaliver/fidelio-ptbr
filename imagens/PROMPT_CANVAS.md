Crie no Canvas um app web (HTML + JavaScript num arquivo só) chamado "Tradutor do Diário" para traduzir para português do Brasil as texturas de texto de um jogo. A interface deve ser em português.

## O que são as imagens
PNGs de 2048×1024 (RGBA) do jogo The Fidelio Incident, passado na Irlanda do Norte dos anos 80. No centro há uma folha de papel envelhecido. O fundo é preto ou transparente. Quase todas são páginas do diário da Leonore: data no topo e texto manuscrito em tinta preta, com algumas palavras escritas bem maiores para dar ênfase. Algumas têm bilhetes colados com texto em vermelho e números de pista. Duas são recortes de jornal ("THE IRISH NEWS"). O nome do arquivo identifica a página (ex.: 09_Michael.png).

## Fluxo do app
1. **Arquivo de traduções (GEMINI.md)**: logo no topo, antes de tudo, um campo para eu carregar o arquivo `GEMINI.md` (upload de .md ou colar o conteúdo). Ele tem as traduções já revisadas de cada página. Formato: cada página é um título `## <nome do arquivo sem .png>` (às vezes seguido de um comentário, ex.: `## 26_Freedom (usar também como 26_SecurePassports)`) e, logo abaixo, um bloco de código delimitado por três crases com o texto da página. Faça o parse assim: para cada linha que começa com `## ` seguida de um nome no formato `NN_Nome`, pegue o primeiro bloco de código que vem depois; ignore as seções que não seguem esse formato (Prompt, Decisões de tradução, Não traduzir). Mostre quantas páginas foram reconhecidas e a lista de nomes. Guarde o conteúdo no localStorage para não precisar carregar de novo. Se a página "26_Freedom" estiver no arquivo, use o mesmo texto para "26_SecurePassports".
2. **Upload das imagens**: aceita uma ou várias imagens (arrastar e soltar ou botão). Cada uma vira um card na fila, com miniatura e nome do arquivo.
3. **Texto de cada página**: associe cada imagem à seção do GEMINI.md pelo nome do arquivo (sem a extensão, sem diferenciar maiúsculas de minúsculas).
   - **Se houver tradução no GEMINI.md**: use esse texto **exatamente como está**, sem retraduzir nem "melhorar". Mostre no card a etiqueta "Tradução do GEMINI.md".
   - **Se não houver**: como alternativa, chame o modelo de texto do Gemini (use a integração de IA do próprio Canvas, sem pedir chave de API) mandando a imagem e pedindo, em JSON, `original` (o texto em inglês transcrito linha por linha, exatamente como aparece, separando blocos/caixas de papel com linha em branco e marcando com [[ ]] os trechos escritos maiores) e `traducao` (com as mesmas quebras de linha e marcações, seguindo as regras de tradução abaixo). Mostre a etiqueta "Tradução automática — revisar".
   - Nos dois casos, mostre o texto num campo **editável** ao lado da imagem original, para eu revisar antes de gerar. Linhas entre parênteses no texto (ex.: "(bilhete azul, tinta vermelha; o 280 continua igual)") são notas de posição para o modelo de imagem, não texto a ser escrito, e devem ser mantidas.
   - Os arquivos 32_Manifest e 33_Map não devem ser traduzidos: avise no card e desabilite a geração (com um botão "gerar mesmo assim").
4. **Geração da imagem**: botão "Gerar imagem". Chama o modelo de edição de imagem do Gemini (gemini-3.1-flash-image ou o mais novo disponível no Canvas) mandando a imagem original e o prompt de edição abaixo. **Antes de enviar, pré-processe o texto revisado**: (a) extraia cada trecho entre `[[` e `]]` para uma lista de destaques; (b) remova do texto **todos** os colchetes (`[[`, `]]`, `[` e `]`), deixando só as palavras; (c) coloque o texto limpo no lugar de {TEXTO} e a lista de destaques, um por linha entre aspas, no lugar de {DESTAQUES} (ou "(none)" se não houver). O modelo de imagem nunca deve receber colchetes, porque ele os desenha na imagem. Mostre no card o texto limpo e a lista de destaques que foram enviados. Deve haver a opção de gerar 1 a 4 variações e eu escolher a melhor clicando nela. Peça a maior resolução de saída que o modelo suportar (ex.: imageConfig com imageSize "2K" ou "4K", se existir) e mostre, em cada variação, **a imagem bruta como veio do modelo**, a resolução dela e o nome do modelo que respondeu. Assim dá para saber se um defeito vem da geração ou do pós-processamento.
5. **Pós-processamento** (no navegador, com <canvas>), sempre aplicado à variação escolhida. O modelo devolve 16:9 (não 2:1), sem transparência e com margens brancas ou pretas, então **não basta redimensionar**: é preciso alinhar a folha de papel.
   - **Páginas com transparência** (o original tem pixels com alpha < 10):
     a) bounding box do papel no original = pixels com alpha > 128;
     b) bounding box do papel na imagem gerada = pixels diferentes da cor de fundo (se o canto superior esquerdo for claro, fundo branco: pixel com algum canal < 235; se for escuro, fundo preto: algum canal > 20);
     c) recortar a gerada nesse box e reescalar para o tamanho do box do original;
     d) refinar o alinhamento: testar largura e altura com variação de -2, 0, +2 e +4 px e deslocamentos de -3 a +3 px, escolhendo a combinação de menor erro quadrático médio RGB numa amostra de pixels das faixas laterais internas do papel (de 15 a 55 px para dentro de cada borda, y de 120 a 900, só onde o alpha original > 200). Mostrar o RMSE na interface: abaixo de ~25 está bom, acima de ~35 avisar para conferir as bordas;
     e) montar a saída: alpha = **alpha original intacto**; RGB = **sempre o da imagem gerada** em todos os pixels onde o alpha original > 0. **Nunca** usar o RGB do original dentro do papel, porque ele contém o texto em inglês e cria letras "falhadas", com restos do inglês misturados (as caixas de papel pautado são quase brancas, então nada de filtrar pixels claros no interior). A única exceção é uma faixa de até 10 px junto à borda do alpha: ali, se o pixel gerado for cor de fundo (quase branco > 235 ou quase preto < 15, porque a folha gerada ficou um pouco menor), use o pixel gerado não-fundo mais próximo para dentro do papel.
   - **Páginas opacas** (os jornais, com faixas pretas nas laterais): achar a faixa horizontal não preta no original (algum canal > 25), achar a área que não é preta nem branca na gerada, recortar a gerada nessa largura (altura inteira) e reescalar para a largura da faixa × 1024. Fora da faixa, manter o original.
   - Resultado: PNG 2048×1024 RGBA.
6. **Comparação**: visualização com controle deslizante (antes/depois) e zoom 100%, para eu conferir os acentos, com o texto esperado exibido ao lado para eu comparar linha por linha.
7. **Download**: botão para baixar o PNG final com **o mesmo nome do arquivo original**, e um botão "Baixar todos" para os aprovados.
8. Mostrar o status de cada card (transcrevendo, aguardando revisão, gerando, pronto, erro). Mostrar a mensagem de erro e permitir tentar de novo. Se aparecer erro de limite de uso, avisar claramente.

## Regras de tradução (instrução para o modelo de texto, usada só quando a página não está no GEMINI.md)
- Português do Brasil informal, na voz de uma jovem irlandesa escrevendo no diário: use "a gente", "pra", "você". Mantenha os palavrões com força equivalente (fucking → porra/do caralho, shite → merda, bastard → desgraçado). Gírias irlandesas viram equivalentes naturais (bolloxed → chapados, blathered → ficamos de papo, runners → tênis, lad → rapaz, da → pai, mates → amigos, pint → caneca/cerveja, grand → maravilhoso, a gas → hilário, deadly → incrível).
- Datas no formato brasileiro: "13- January -1985" → "13 de janeiro de 1985".
- Não traduzir nomes de pessoas (Leonore, Stanley, Molly, Colin, Rory, Paddy, Michael O'Shae, Margaret Keene, Udom). Manter grafias inconsistentes do original (Whitaker/Whitacre, Rory Calhoun/Cochrane).
- Lugares com nome em português: Irlanda, Munique, Leste de Belfast, Bornéu. "Rory's Pub" → "Pub do Rory". "The Troubles" → "os Troubles". "Starry Plough" e "UVF" ficam iguais.
- "Boxing Day" (nome britânico) fica "Boxing Day". "Wren's Day" (nome irlandês do mesmo dia) vira "Dia de Santo Estêvão".
- Números de pista (ex.: 280, 3128) nunca mudam. "#'s" → "nºs".
- Jornais: traduzir só a manchete, as legendas das fotos e a faixa do rodapé. O nome do jornal, o site e as colunas de texto miúdo ficam em inglês.
- Se a imagem for um formulário de carga (Delivery Bill) ou um mapa com nomes em islandês, retornar `traducao` vazia e avisar na interface que essa página não deve ser traduzida (no mapa, no máximo "NORWEGIAN SEA" → "MAR DA NORUEGA").

## Prompt de edição de imagem (enviar exatamente assim, em inglês)
```
Edit this image: replace all English text with the Brazilian Portuguese text given below, keeping everything else identical.

This is a texture from a narrative video game set in Northern Ireland in the 1980s (a woman's personal diary page or a newspaper clipping about the Troubles). It will be reinserted into the game, so the layout must match the original exactly.

Strict rules:
1. Preserve the image pixel-for-pixel outside the text: same paper texture, stains, torn edges, lined paper boxes, drawings, photos, colors, lighting, and the black background/borders. Do NOT crop, zoom, stretch, rotate, add or remove anything; keep the full centered page with side margins matching the original framing.
2. Match the original lettering: same handwritten style (thin, slightly irregular, casual marker handwriting), same ink color, same size, same line positions and alignment. The phrases listed under EMPHASIS below must be written larger, in the same places where the original has its larger emphasized words; everything else uses the normal size.
3. Each block of text must stay inside its own paper box/area. If a Portuguese line is longer, shrink the letters slightly; never overflow the box or cover the drawings.
4. Accented letters (á à â ã é ê í ó ô õ ú ç) must be clearly drawn and legible.
5. Replace ONLY the text listed below. Anything not listed (newspaper masthead, website, small dense body-text columns, numbers) stays exactly as it is.
6. Use exactly this text, with the line breaks shown. Blank lines separate text blocks/boxes. Lines in (parentheses) are placement notes for you, not text to draw:
---
{TEXTO}
---

EMPHASIS (write these exact phrases larger; they already appear in the text above, do not add them again):
{DESTAQUES}

Output only the edited image. Never write any part of these instructions into the image, and never draw brackets, quotes around the emphasis list, or labels like "EMPHASIS".
```

## Extras
- Guardar no localStorage as edições que eu fizer no texto de cada página, por nome de arquivo, para não perder se eu recarregar a página. Um botão "Voltar ao texto do GEMINI.md" desfaz minhas edições.
- Visual simples e escuro, funcional no desktop.
