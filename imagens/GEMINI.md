# Tradução das imagens com o Gemini

Uma imagem por conversa: anexe o PNG de `imagens/originais/`, cole o prompt abaixo e troque o bloco `---` pelo texto da página correspondente.
Salve o resultado em `imagens/traduzidas/` com o mesmo nome do arquivo original. O fluxo recomendado é o app do Canvas (ver `PROMPT_CANVAS.md` e o README).

`[[texto]]` marca o trecho que no original está escrito maior/destacado. As quebras de linha seguem as do original.

## Prompt

```
Edit this image: replace all English text with the Brazilian Portuguese text given below, keeping everything else identical.

This is a texture from a narrative video game set in Northern Ireland in the 1980s (a woman's personal diary page or a newspaper clipping about the Troubles). It will be reinserted into the game, so the layout must match the original exactly.

Strict rules:
1. Preserve the image pixel-for-pixel outside the text: same paper texture, stains, torn edges, lined paper boxes, drawings, photos, colors, lighting, and the black background/borders. Do not crop, zoom, rotate, add or remove anything. Keep the exact same 2:1 aspect ratio and canvas framing.
2. Match the original lettering: same handwritten style (thin, slightly irregular, casual marker handwriting), same ink color, same size, same line positions and alignment. The phrases listed under EMPHASIS below must be written larger, where the original has its larger emphasized words.
3. Each block of text must stay inside its own paper box/area. If a Portuguese line is longer, shrink the letters slightly; never overflow the box or cover the drawings.
4. Accented letters (á à â ã é ê í ó ô õ ú ç) must be clearly drawn and legible.
5. Replace ONLY the text listed below. Anything not listed (newspaper masthead, website, small dense body-text columns, numbers) stays exactly as it is.
6. Use exactly this text, with the line breaks shown. Blank lines separate text blocks/boxes:
---
[TEXTO DA PÁGINA]
---

Output only the edited image.
```

## Decisões de tradução
- Tom informal brasileiro, "a gente", palavrões mantidos (como nas legendas).
- **Boxing Day × Wren's Day**: o diário contrasta o nome britânico com o irlandês. Mantive "Boxing Day" (britânico) e usei "Dia de Santo Estêvão" para o irlandês (é o mesmo 26/12; "Wren's Day" é o nome popular irlandês dele).
- Nomes de pessoas intactos, inclusive as inconsistências do original (Whitaker/Whitacre, Rory Calhoun/Cochrane).
- Lugares com nome em português: Munique, Irlanda, Leste de Belfast, Bornéu. "The Troubles" ficou "os Troubles". "Starry Plough" e "UVF" sem tradução.
- Números das pistas (280, 3128) não mudam.
- Datas no formato brasileiro: "13- January -1985" → "13 de janeiro de 1985".
- Coerente com o CSV: "Eu tinha medo disso." e "Eu o ouvi dizer "Não vá". Será que está falando comigo".

## Não traduzir
- **32_Manifest**: formulário de carga com texto pequeno e denso; o Gemini vai embaralhar. Não tem nada narrativo.
- **33_Map**: os nomes estão em islandês de propósito (Helvíti = Inferno, Játning = Confissão etc.). No máximo troque "NORWEGIAN SEA" por `MAR DA NORUEGA` (mesma fonte máquina de escrever, maiúsculas). Opcional.
- **26_SecurePassports**: é idêntica à 26_Freedom; copie o resultado.

---

## 01_Gatsby
```
13 de janeiro de 1985
Eu e a Molly saímos escondidas pra uma [[festa]] hoje à noite.
Quando a gente chegou, já estava bombando.
Ou seja, os garotos estavam todos chapados. Bem, nem todos.

A gente mal tinha chegado quando um rapaz lindo
me entregou uma cerveja e disse que se chamava [[Colin.]]
Era alto, tinha olhos verdes brilhantes e usava tênis neon.
Perguntei se a festa era dele.
Ele balançou a cabeça e disse que agora a festa era minha.
Aí ele se virou e abanou a mão em volta como se fosse o [[Grande Gatsby do caralho,]]

E a primeira coisa que vimos foi o [[Stanley Whitaker]] vomitando na pia da cozinha.
Eu ri e disse que ele podia ficar com a festa de volta.
A gente ficou de papo um tempão, e estava rolando um clima quando

o Stanley Whitacre veio cambaleando e perguntou ao Colin se ele
usava aqueles sapatos na rua. Antes que eu mandasse ele se foder,
o Stanley perguntou ao Colin se ele sabia que eu era a
[[filha do Michael O'Shae.]]
Senti minhas pernas amolecerem.
O Colin não conseguiu fugir de mim rápido o bastante.
```

## 02_Brave
```
18 de janeiro de 1985
Eu e a Molly estávamos no [[Pub do Rory]] quando entrou o [[Stanley Whitaker.]]
Peguei minha caneca e fui encontrar com ele no meio do salão.
Quando ele me viu chegando, os olhos dele brilharam com um sorrisão lindo e bobo.
[[Joguei minha bebida na cara dele.]]
Depois agarrei ele pela gola e mandei ele fechar aquela matraca sobre o meu pai.
O Stanley piscou pra tirar a cerveja dos olhos e disse que só estava me protegendo, porque
o "Senhor Sapatinho Chique" era bonito demais
e que eu devia ficar com um cara sem graça, pra todo mundo reparar na
mulher linda. Disse que eu era "radiante".
Depois disse que as pessoas também iam saber que eu sou corajosa.
Sabe Deus por quê, mas eu ri e perguntei: [["Por que eu sou corajosa?"]]
"Tem que ser", ele disse,
[["pra ser vista com um cara como eu."]]
O pub inteiro caiu na gargalhada.
O Rory jogou uma toalha pra ele e o Stanley pegou sem tirar os olhos de mim.
Eram as coisas mais azuis que eu já tinha visto.
[[Que desgraçado.]] Mal posso esperar pra ver ele de novo.
```

## 03_Texas
```
20 de abril de 1985
Eu e o Stanley resolvemos nos aventurar mais longe pela cidade hoje.
Ele disse que a gente não devia atravessar pro Leste de Belfast, mas eu não liguei.
Eu estava me sentindo corajosa. Quando vimos a festa, parecia incrível,
então arrastei o Stanley escada acima.
Adoro ir a festas onde ninguém me conhece.
Posso ser quem eu quiser.
Falei pro Stanley fingir que aquela era a nossa casa.
A gente ficou zanzando, inventando histórias de onde
tinha arrumado cada móvel.
Eu estava falando do relógio de pêndulo que veio de Bornéu
quando um bêbado babaca se virou e disse que eu estava falando merda.
Era o dono da casa. Aí ele perguntou de onde a gente era.
Juntou gente em volta, e a resposta errada podia dar problema.
O Stanley passou o braço em volta do homem e disse: "Somos do [[Texas,]]
[[América."]]
O rosto do homem se iluminou. Ele amava a América!
O sotaque do Stanley era ridículo, mas a confiança dele era inspiradora,
então acreditaram em cada palavra.
Foi maravilhoso.
```

## 04_Margaret
```
11 de junho de 1985
O Stanley me levou numa [[árvore velha]] linda
nos penhascos de frente pro mar.
Era simplesmente o [[lugar perfeito.]]

Aí eu vi que tinha marcas talhadas no tronco.
Apontei pra elas e perguntei quantas outras garotas ele já tinha trazido ali.
O [[Stanley riu]] e disse que, quando ainda era moleque,
ele e o pai vinham fazer piquenique nesse mesmo lugar
e o Paddy marcava a árvore pra mostrar o quanto o Stanley tinha crescido.
Fiquei vermelha feito um pimentão e murmurei algum tipo de desculpa.
Quando sentamos pra almoçar,
vi outra marca na base da árvore.
Quando perguntei pra que era aquela,
ele piscou e disse: [["Margaret Keene."]]
```

## 05_Speech
```
2 de agosto de 1985
A mamãe me implorou pra não ir, mas garanti a ela que era uma
[[manifestação pacífica.]]
A Molly não quis ir comigo. Ela tinha medo de o exército aparecer.

Então arrastei o [[Stanley]] comigo.
Achei que ele com certeza ia querer estar lá
porque o [[pai]] dele era um dos oradores.
O [[Paddy Whitaker]] tinha uma presença eletrizante.
As pessoas aplaudiam e gritavam enquanto ele falava
sobre o fim da violência. Um fim pacífico para [[os Troubles.]]
Ele falava com tanta convicção que eu quase chorei.

Mas quando olhei pro Stanley,
ele estava com a porra dos fones de ouvido, mexendo no walkman.
Disse que já tinha ouvido tudo aquilo antes.
Não acreditei. Ele não faz ideia da [[sorte que tem.]]

(bilhete azul, tinta vermelha; o 280 continua igual)
Pelo menos uma vez, Stanley,
me escute!!!
Use estes 5 nºs
```

## 06_StarryPlough
```
12 de setembro de 1985
Não sei qual é o problema daquele homem!
O Stanley chegou no Pub do Rory hoje à noite, suado e sem fôlego.
O olho estava inchado, o lábio [[sangrando]]
e ele estava todo orgulhoso, feito um pavão.
Ele e um dos amigos inúteis dele foram se meter no Leste de Belfast
pra arrumar confusão. O Stanley teve a brilhante ideia de pichar
a Starry Plough por cima de um mural unionista, mas foram pegos
por uns moradores de lá e saíram na porrada.
O Rory achou aquilo hilário e pagou uma cerveja pro Stanley.
[[Eu disse ao Stanley que ele era um idiota.]]
E se ele tivesse sido pego pela Guarda? Ou pela UVF?
Iam ter matado ele, porra.
Mas ele estava [[orgulhoso demais de si mesmo pra escutar.]]
```

## 07_Guitar
```
26 de setembro de 1985
O Stanley ainda consegue me surpreender, mesmo depois de todo esse tempo.
Fomos de carro fazer um piquenique na nossa [[Árvore à beira-mar.]]
Mas quando chegamos, o Stanley tirou um estojo de violão do porta-malas.
Eu nem sabia que ele tocava violão.
A tarde toda, ficamos deitados juntos na grama debaixo da árvore
enquanto o Stanley dedilhava sem parar. Foi maravilhoso.
Aí ele me mandou fechar os olhos.
Falei que era bom ele não estar tendo nenhuma ideia engraçadinha,
mas ele disse que tinha tentado aprender uma música nova só pra mim.
Depois de alguns compassos, começou a soar familiar,
mas não me segurei e beijei ele antes que ele terminasse a música.
[[Um dia eu deixo ele terminar pra mim.]]
```

## 08_BrokenIsland
```
15 de novembro de 1985
[[Belfast]] está tão fria que o ar parece se quebrar nos meus pulmões. Não importa o que eu faça,
simplesmente não consigo me esquentar.
Outra noite, no Pub do Rory, perguntei ao Stanley se ele me levaria pra algum lugar quente,
tipo outro país.
Ele disse que, se fizesse isso, [[a gente nunca mais voltaria.]]
Mas a ideia pareceu tão boa que passamos o resto da noite
falando de viajar pra terras exóticas. De conhecer gente que a gente
não ia entender. De comer comida apimentada até o rosto ficar vermelho
e o suor escorrer pelas costas.
Acho que ele não percebeu o quanto eu estava falando sério. A gente devia deixar esta
[[ilha partida]] enquanto ainda temos chance.
```

## 09_Michael
```
12 de dezembro de 1985
A mamãe está chorando no quarto ao lado.
Diz que é de felicidade, mas eu não acredito.
[[Meu pai vai sair da prisão.]]
Meus amigos protestam contra as prisões ilegais,
mas eu queria que deixassem o Michael O'Shae trancado pra sempre.
Prisão perpétua não é tempo suficiente pra ele.
Isso mataria a mamãe, se ela lesse.
E se o Michael lesse? Isso mataria ele, ou ele me mataria?
A violência não parou enquanto ele estava lá dentro,
mas pelo menos, quando eu lia sobre alguma coisa terrível no jornal,
eu sabia que não tinha sido meu pai.
Mas agora...
[[Que Deus nos ajude.]]

(bilhete de papelão, tinta vermelha; o 3128 continua igual)
Stanley, esses 5
nºs vão te salvar!!!
```

## 10_Fidelio
```
21 de julho de 1986
[[Meu rosto dói de tanto tentar sorrir a noite toda.]]
Não posso culpar o Stanley. Ele não tinha como saber.
Ele não é tão cruel.
Ele sabia que meu nome vinha da
[[ópera de Beethoven]]
e simplesmente achou que eu fosse fã.
Mas quem amava ópera era o meu pai.
Ele botava aqueles discos no último volume noite adentro e cambaleava
com uma garrafa pela metade, balançando no ritmo da música.
[[Era aterrorizante.]]
Mas eu amo o Stanley. Então apertei a mão dele e sorri a apresentação inteira.
```

## 11_NewspaperPaddy
```
(manchete, mesma fonte serifada em negrito)
Batida do Boxing Day em
esconderijo do IRA - 7 mortos

(legenda da foto)
Paddy Whitacre, ativista
pela paz, é morto

(faixa verde no rodapé, opcional)
Não deixe a política estragar um aniversário
```

## 12_Killed
```
26 de dezembro de 1986
Mãe de Deus,
[[Mataram o Paddy!]]
Os jornais britânicos chamaram de
"A Batida do Boxing Day". Mas não foi uma batida.
Por aqui, estão chamando de
[["O Massacre do Dia de Santo Estêvão."]]
Sete pessoas mortas a tiros no dia seguinte ao Natal.
Não sei sobre o que era a reunião.
Não quero saber. Eram todos homens violentos, menos o pai do Stanley.
O que o Paddy Whitaker estava fazendo lá?
Como ele ficou sabendo da reunião?
Será que estava tentando convencer eles a desistir do que estavam planejando?
Preciso achar o [[Stanley. Ele deve estar passando pelo inferno.]]
```

## 13_Funeral
```
1 de janeiro de 1987
Tantos funerais hoje.
Fui com o Stanley ao [[funeral do pai dele.]]
Tinha uma multidão.
Falei pro Stanley que o pai dele ficaria orgulhoso
de ver tanta gente,
ele disse que o [[Paddy]] só ia querer fazer um discurso.

A polícia estava de olho na multidão,
mas não incomodou ninguém.
Estavam escondidos, mas eu vi na hora.

Tive que ajudar o Stanley a escrever o discurso fúnebre
do [[Paddy,]]
mas quando chegou a hora de ler,
ele não conseguiu falar.
Apertou as laterais do púlpito
com tanta força que tive medo de que rachasse nas mãos dele.
Por fim, o Stanley disse que
[[quem fazia discursos era o Paddy]]
e que ele não era parecido o bastante com o pai pra fazer jus a ele.
Só dobrou o discurso e saiu em [[silêncio.]]
```

## 14_BlackPub
```
1 de janeiro de 1987
O [[Rory]] fez um velório no pub pras vítimas do [[Santo Estêvão.]]
Acho que ele só queria se exibir. Ele foi [[preso]]
no ano passado por tráfico e a polícia quebrou a mão dele,
então de repente ele virou todo político.

Eu e o Stanley ficamos um tempão no carro, vendo
a porta da frente engolir todos os ternos pretos até o pub
parecer cheio de tinta.

O Stanley abriu a porta do carro, mas eu agarrei o braço dele
e pedi pra ele [[me levar pra nossa árvore.]]
Senti uma ansiedade paralisante de que, se eu entrasse naquele pub preto,
nunca mais veria o céu.
O Stanley não disse uma palavra, só ligou o carro e fomos embora.
```

## 15_MothBalls
```
30 de janeiro de 1987
A gente não ia ao mar desde a primavera,
e foi um choque ver a nossa árvore tão seca e frágil.
Enquanto caminhávamos, o Stanley pôs o casaco dele
nos meus ombros. Ainda estava quente do corpo dele e
puxei a gola até o nariz pra ver se ainda
tinha o cheiro dele. Não tinha, só cheirava a poeira
e naftalina.
O Stanley disse que o pai dele o trazia aqui e dizia:
[["É por isso que a gente luta."]]
Ele acha que agora finalmente entende o que o pai quis dizer,
[[mas eu fico pensando...]]
Estendi o casaco no chão e puxei nós dois pra cima dele.
Eu só queria fazer ele esquecer o resto do dia.
Eu queria esquecer o resto do mundo, menos ele.
A grama pinicava e estava seca, e o céu estava branco feito papel de açougue.
Nenhum de nós se deu ao trabalho de dizer mais nada. O vento frio
só ia levar nossas palavras embora.
```

## 16_Rory
```
12 de fevereiro de 1987
Não sei o que está acontecendo com o [[Stanley.]] Tenho medo de que ele tenha [[enlouquecido.]]
Hoje à noite, eu estava esperando por ele no [[Pub do Rory.]]
O Rory estava reclamando da porra da mão dele de novo.
Quando o Stanley finalmente apareceu,
estava [[branco feito um fantasma.]]
Agarrou meu cotovelo e disse que a gente tinha que ir.
Eu já estava lá fazia um tempo, então não estava
com paciência pra ser arrastada.
Mandei ele sentar enquanto eu terminava minha cerveja,
mas ele arrancou o copo da minha mão e espatifou no chão.
O Rory começou a berrar feito louco.
E foi aí que [[o Stanley partiu pra cima dele.]]
Ele se jogou em cima do Rory,
tentando agarrar o pescoço dele.
O Rory levou um susto tão grande que escorregou e caiu no chão.
Precisei de toda a minha força pra tirar o Stanley
de cima dele e arrastar ele até a porta da frente.
O Rory ficou atrás do balcão,
xingando todos os Whitaker.
```

## 17_NewspaperPubBomb
```
(manchete, mesma fonte serifada em negrito)
Bomba no pub do informante
Rory Calhoun. IRA é suspeito

(legenda ao lado da foto da menina)
Menina de 9
anos morta
em atentado
a pub!

(faixa verde no rodapé, opcional)
Não deixe a política estragar um aniversário
```

## 18_Bomb
```
15 de fevereiro de 1987
Achei que as coisas estavam melhorando.
Eu tinha esperança de que estávamos seguindo em frente.
Eu acreditava na [[mensagem do Paddy Whitaker.]]
A violência não pode ser a resposta.
Mas agora ele se [[foi.]]
[[O Pub do Rory foi bombardeado ontem à noite.]]

Graças à Virgem Santa, o Rory fechou o pub pra festa de aniversário dele.
Mas [[16]] pessoas morreram.
Uma das vítimas era uma [[menininha.]]
Da última vez que fomos atacados assim,
[[meu pai enlouqueceu.]] Ele jogou bebida na raiva dele
até ela virar um incêndio que quase engoliu todos nós.
Agora ele está calado feito um túmulo. E isso é ainda mais
[[aterrorizante.]]
```

## 19_Arrested
```
5 de março de 1987
Mal consigo sentir a caneta nos dedos.
Meu corpo inteiro está dormente.
Mal consigo ver as palavras na página.
[[Não consigo parar de chorar.]]
Levaram embora o meu coração.
[[O Stanley foi preso]]
pelo atentado ao [[Pub do Rory.]]

Alguém deve ter armado pra ele.
Perguntei ao meu [[pai]] se ele sabia quem faria isso com o Stanley.
Ele só disse que eu devia seguir em frente.
Que o Stanley não vai durar muito na prisão.
Quase cuspi na cara dele.
Juro por tudo que é mais sagrado,

se eu descobrir que ele teve alguma coisa a ver com a prisão do Stanley...
[[Eu queimo ele vivo!]]
```

## 20_Wife
```
8 de março de 1987
Não vou ser mulher de presidiário.

Não vou virar uma daquelas outras esposas vazias.
[[Como a minha mãe.]]

Não vou ser vigiada, nem cuidada,
[[Isolada.]]

Não existe luz sem ele.

Ele é o meu coração, e eu não consigo viver sem o meu coração.

Vou fazer o que for preciso pra tirar ele de lá.
[[Não vou ser mulher de presidiário.]]
```

## 22_Rescue
```
3 de abril de 1987
Está tudo pronto.
Mas o ar parece oco e vazio no meu peito.
Consigo ouvir meu coração batendo nos ouvidos.
Em poucas horas, a vida como eu conheço vai acabar.
Mas isso só se eu tiver muita sorte.
Senão, a minha vida simplesmente vai... acabar.
[[Hoje eu vou resgatar o Stanley.]]
```

## 23_Plan
```
3 de abril de 1987
A Molly trabalha na prisão. Ela ficou com medo de aceitar o emprego,
mas o [[meu pai]] insistiu que era bom ter alguém nosso lá dentro.
Ele só queria usar ela.
Mas no fim quem está pondo ela em risco sou eu.
Ela levou o pó lá pra dentro, e tem um rapaz do bairro
que vai botar no café da manhã do Stanley.
Se ele comer o bastante, a dor na barriga vai ser tão forte
que vão transferir ele pro hospital.
Mas se ele comer demais,
[[pode matar ele.]]
```

## 24_TheTruth
```
18 de março de 1987
Até agora, eu nunca soube o quanto meu pai odiava o Stanley.
O homem sempre teve os segredos dele, mas nunca tinha simplesmente mentido pra mim.
Ele tentou me contar por que o Stanley foi preso de verdade,
e [[A VERDADE]] sobre o Rory Cochrane.
Mas não consigo acreditar no que ele disse sobre o Stanley. Não consigo!
Todas aquelas pessoas.
O Stanley nunca...
```

## 25_Escape
```
3 de abril de 1987
Eu não podia pedir ajuda ao meu pai.
Ele é todo a favor de deixar o Stanley levar a culpa.
Mas o maluco desgraçado que estava comigo hoje não sabia disso,
então fez tudo o que eu mandei, inclusive roubar uma ambulância.
A Molly ligou pra avisar da transferência médica do Stanley,
o que nos deu uma vantagem sobre a ambulância de verdade.
Eu estava ridícula no uniforme, mas nossos documentos estavam perfeitos,
então mantive a cabeça erguida e me inspirei na confiança do Stanley.
Mesmo assim, quase desmaiei quando os guardas trouxeram ele na maca.
[[Ele já parecia morto.]]
Os guardas colocaram ele a bordo, e eu saí dirigindo.
Cinco minutos depois, o maluco desgraçado apagou os dois guardas com anestésico.
E simples assim, [[o Stanley estava livre.]]
```

## 26_Freedom (usar também como 26_SecurePassports)
```
3 de abril de 1987
O Stanley está tentando ser corajoso, mas eu vejo que ele
ainda está com dor. Consegui passaportes perfeitos
e um barco com um capitão que não faz perguntas.
Tem tantas enseadas na costa oeste.
Vamos desembarcar em segredo absoluto.
O mundo inteiro está aberto pra nós.
O mundo inteiro, menos a [[Irlanda,]]
mas não vou sentir falta nem por um segundo.
Agora temos uma vida nova.
[[Juntos.]]
```

## 27_SadEyes
```
22 de outubro de 1990
Os verões em [[Munique]] são lindos.
As praças ficam cheias de turistas,
então eu e o Stanley nos misturamos fácil.
Mas mesmo nesse mar de rostos anônimos,
a gente precisa tomar cuidado.

Hoje, eu estava sentada no parque com meu almoço
quando um rapaz com uma câmera grande e chique
veio até mim. Era bonito e estiloso,
bem do tipo artista,
e perguntou se podia tirar umas fotos minhas.
Claro que eu tive que dizer não.
Mas aí ele disse uma coisa que me pegou de surpresa.
Disse que meus olhos eram os [[mais tristes]] que ele já tinha visto.
"Claro que são", eu disse.
[["Sou irlandesa."]]
Deixei tudo no banco e sumi na multidão.

(papel azul à esquerda, escrito inclinado)
10 dias desde os últimos
pesadelos do Stanley, as [[orações]]
estão funcionando!!
```

## 28_Curry
```
(papel azul no canto, escrito inclinado)
sem pesadelos, mas a
depressão do Stanley está piorando.

4 de junho de 1995
Tinha tanta gente no mercado
que eu não conseguia nem pensar.
Eu precisava sair dali, mas quando
pedi pro Stanley escolher alguma coisa
pro jantar, ele só respondeu com o "o que você quiser" de sempre.
Eu queria que ele [[tomasse uma decisão]]
pelo menos uma vez, pra eu parar de pensar em
absolutamente tudo o tempo todo.
As sacolas estavam tão pesadas que minhas mãos
estavam com cãibra. E alguém por perto
estava fedendo a bode. Pode até ter sido eu.
Então larguei tudo e deixei as sacolas
se espalharem pela rua toda. Nem liguei.
Estou cansada da multidão e do fedor de curry.
Estou cansada do calor.
Quero andar na grama verde.
Quero sentir o ar fresco na pele debaixo de
um céu da cor de papel de açougue.
```

## 29_IrishDream
```
14 de janeiro de 2001
Não consigo parar de pensar no [[sonho.]]
A gente estava voando no avião, mas eu não estava com medo.
Eu estava eufórica porque estávamos voltando [[pra Irlanda.]]
O Stanley mergulhou o avião tão rápido que senti meu estômago flutuar
e [[a gente ria]] como não ria há séculos.

Quando saímos das nuvens e descemos rasante sobre o oceano,
eu vi os penhascos brancos e as colinas verdes.
Muros de pedra e cercas vivas dividiam os campos em retalhos salpicados de gado.
E a nossa árvore, nos recebendo em casa.
Aí eu acordei neste quarto quente e imundo, pingando de suor.
O Stanley ainda está dormindo. Sem pesadelos, graças a Deus.
[[Talvez seja a minha vez.]]

(bilhete laranja circulado, tinta vermelha)
Stanley, use meu
diário pra destrancar
seu caminho....
```

## 30_VillageBoy
```
4 de maio de 2006
Não sei por que continuo com esses malditos diários.
[[Tem tantas coisas que eu queria poder esquecer.]]
Hoje, no terreno da escola, meus sentidos se encheram
do zumbido dos insetos e do cheiro da selva.
Mas aí, de repente, achei que estava de volta em Belfast.
O ar tremeu com o baque pesado de uma [[bomba explodindo.]]
O [[Stanley]] saiu em disparada na direção do barulho.
Uma vaca tinha pisado numa mina terrestre antiga,
e tinha um homem na beira do campo
gritando pra todo mundo ficar longe.
Mas o Stanley passou correndo por ele, chapinhando na lama.
Eu quis impedir, mas minha voz travou na garganta
quando vi o Stanley levantar o corpinho do meio do mato.
O nome do menino era Udom.
Ele estava andando com a vaca.
O pai do Udom desabou quando o Stanley entregou o menino a ele com cuidado.
O pai do Udom não parava de pedir desculpas por não ter protegido o filho
[[dos males trazidos a esta aldeia.]]
```

## 31_Nightmares
```
20 de maio de 2006
Eu tinha medo disso.
Eu soube, no momento em que vi o Stanley apertando aquele corpinho nos braços,
[[que os pesadelos iam voltar.]]
Estão piores do que nunca.
Sinto o coração do Stanley se partindo a cada respiração trêmula.
Eu o ouvi dizer "Não vá". Será que está falando comigo?

[[Eu nunca vou deixar ele.]]
```
