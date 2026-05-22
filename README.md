# MD2HTML

MD2HTML é um compilador leve feito em Python que converte arquivos Markdown (`.md`) em arquivos HTML (`.html`) completos e estilizados. Ele utiliza um Lexer e um Parser personalizados construídos com a biblioteca **PLY** (Python Lex-Yacc) para interpretar a sintaxe Markdown e renderizá-la diretamente em HTML com uma estilização CSS embutida e inspirada no GitHub.

## Funcionalidades Suportadas
O parser suporta uma grande variedade de elementos padrão do Markdown:
- **Cabeçalhos:** Suporta de H1 (`#`) até H6 (`######`).
- **Formatação de Texto:** Negrito (`**texto**`), Itálico (`*texto*`) e Tachado (`~~texto~~`).
- **Código:** Blocos de código em linha (` `código` `) e blocos de código de múltiplas linhas (` ```código``` `).
- **Links e Imagens:** Suporta links padrão `[título](url)` e imagens `![alt](url)`.
- **Listas:** Listas Ordenadas (`1. `) e Não Ordenadas (`- ` ou `* `).
- **Tabelas:** Suporte completo para tabelas em Markdown com cabeçalhos e linhas.
- **Citações (Blockquotes):** Blocos de texto citados usando `>`.
- **Linhas Horizontais:** Divisores de seção (`---`).

## Estrutura do Projeto
- `main.py`: O ponto de entrada da aplicação. Ele lê um arquivo `input.md`, passa pelo compilador e gera o `output.html`.
- `compiler.py`: O motor principal. Define as regras gramaticais usando expressões regulares para análise léxica (lexer) e regras gramaticais estruturais para análise sintática (parser/yacc).
- `css.py`: Contém um bloco de estilos CSS pré-definidos que são injetados automaticamente no `<head>` do documento HTML resultante, dando a ele um visual moderno, limpo e parecido com o do GitHub.
- `requirements.txt`: Dependências do projeto (requer `ply`).

## Como Funciona
Quando você executa o `main.py`:
1. O script lê o texto bruto de `input.md`.
2. O **Lexer** tokeniza o texto (ex: identificando `HASH`, `BOLD`, `CODE_BLOCK`).
3. O **Parser** pega esses tokens e constrói estruturas HTML (ex: transformando um token `HASH` seguido de texto em uma tag `<h1>`).
4. O corpo HTML gerado é combinado com a estrutura HTML base e o CSS de `css.py`.
5. O documento final é salvo como `output.html`.

## Como Usar
1. Instale as dependências: `pip install -r requirements.txt` (requer `ply`).
2. Crie ou edite um arquivo `input.md` no diretório raiz.
3. Execute o script: `python main.py`
4. Abra o arquivo `output.html` gerado no seu navegador de internet.
