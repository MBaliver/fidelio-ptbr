# The Fidelio Incident — Tradução PT-BR

Tradução não oficial para português do Brasil de **The Fidelio Incident** (Unreal Engine 4.14, compatível com a versão Steam no Windows e no Linux via Proton).

---

## 📥 Download

Você pode obter o arquivo do patch (`TheFidelioIncident-WindowsNoEditor_ptBR_P.pak`) de duas formas:
1. Pela página de **[Releases](https://github.com/MBaliver/fidelio-ptbr/releases)** (Recomendado).
2. Ou baixando diretamente da pasta [`dist/`](dist/TheFidelioIncident-WindowsNoEditor_ptBR_P.pak) neste repositório.

---

## 🎮 Como Instalar

Instalar a tradução é muito simples e **não altera** nenhum arquivo original do jogo:

### 1. Localize a pasta do jogo na Steam
* Abra a **Steam**, clique com o botão direito em **The Fidelio Incident** na sua biblioteca.
* Selecione **Gerenciar** > **Explorar arquivos locais**.

Ou navegue manualmente até o diretório padrão:
* **Windows:**
  ```text
  C:\Program Files (x86)\Steam\steamapps\common\The Fidelio Incident\
  ```
* **Linux (Steam / Proton):**
  ```text
  ~/.local/share/Steam/steamapps/common/The Fidelio Incident/
  ```

### 2. Copie o arquivo do patch
1. Dentro da pasta do jogo, acesse a pasta:
   ```text
   TheFidelioIncident/Content/Paks/
   ```
2. Cole o arquivo `TheFidelioIncident-WindowsNoEditor_ptBR_P.pak` dentro dessa pasta.

### 3. Pronto!
Inicie o jogo normalmente pela Steam. Ele já estará em português do Brasil!

---

## 🗑️ Como Desinstalar

Para desinstalar e voltar o jogo ao inglês original:
* Acesse `TheFidelioIncident/Content/Paks/` e apague o arquivo `TheFidelioIncident-WindowsNoEditor_ptBR_P.pak`.
* Os arquivos originais do jogo permanecem intactos.

---

## 📝 O Que Foi Traduzido

- ✅ **Legendas** completas dos diálogos
- ✅ **Menus** e telas de configuração
- ✅ **Cartas e notas** encontradas pelo cenário
- ✅ **Créditos**
- ✅ **29 páginas manuscritas** do diário da Leonore (com as caligrafias e estilos originais preservados)
- ✅ **Recortes de jornais**
- ✅ **Fontes acentuadas** (á, à, â, ã, é, ê, í, ó, ô, õ, ú, ç desenhados à mão no padrão das fontes originais)

> **Observação:** A narração em áudio das páginas do diário permanece em inglês (o jogo não possui suporte nativo a legendas para essas falas). O formulário de carga (32_Manifest) e o mapa (33_Map) foram mantidos no original por coerência de design e contexto narrativo.

---

## 🛠️ Desenvolvimento e Código-Fonte

Os arquivos-fonte da tradução (planilhas CSV, ferramentas de extração/injeção de texturas, fontes vetoriais, scripts e prompts) estão disponíveis na branch [`dev`](https://github.com/MBaliver/fidelio-ptbr/tree/dev).
