# Desafio 1 — Sistema de Análise de Atendimentos de Suporte Técnico

Programa FIC_DEV | Escola Técnica Estadual de Cuiabá

## Identificação

- **Alunos:** Túlio F. Q. Dantas e Leandro José Conceição Souza
- **Turma:** Noturno

## Descrição resumida da solução

Aplicação que lê registros de atendimentos em CSV, JSON e TXT, valida cada
registro individualmente, trata e padroniza os dados, remove duplicidades,
calcula indicadores estatísticos e gera gráficos e relatórios de saída.

Segue as etapas: leitura → validação → remoção de duplicados →
padronização → cálculo de indicadores → geração de gráficos → exportação,
implementadas em módulos separados dentro do pacote `src/`:

| Módulo | Responsabilidade |
|---|---|
| `leitura.py` | Verificação de diretórios e leitura de CSV, JSON, TXT e Excel |
| `validacao.py` | Validação de campos (e-mail, telefone, data, tempo, categoria, status) via regex e regras de negócio |
| `processamento.py` | Remoção de duplicados, padronização em massa e cálculo de indicadores (Pandas + NumPy) |
| `relatorio.py` | Geração de gráficos (Matplotlib) e exportação dos resultados (CSV/JSON) |
| `main.py` | Orquestra todas as funções |

## Ambiente virtual

Criação e ativação do ambiente virtual (Windows / PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Instalação das dependências

Com o ambiente virtual ativado:

```bash
pip install -r requirements.txt
```

## Comando de execução

A partir da **raiz do projeto**:

```bash
python -m src.main
```

Os arquivos de saída são gerados em `output/`:
- `atendimentos_processados.csv` — dados tratados
- `resumo.json` — indicadores consolidados
- `erros.log` — log de execução e validação
- `graficos/` — 4 gráficos em PNG

## Decisões adotadas para tratar dados inválidos

- **Formato de data de saída:** `DD/MM/AAAA`. Formatos de entrada aceitos:
  `DD/MM/AAAA`, `AAAA-MM-DD`, `DD-MM-AAAA`, `AAAA/MM/DD`.
- **Tempo de atendimento válido:** número entre 0 (exclusivo) e 600 minutos
  (10 horas).
- **Categoria:** normalizada via mapa de-para construído a partir do
  `categorias.json` (aliases → categoria padrão), ignorando maiúsculas e
  espaços extras. Categorias não reconhecidas (ex: `"categoria inexistente"`)
  invalidam o registro.
- **Status:** normalizado para minúsculo, restrito ao conjunto
  `{aberto, em andamento, resolvido}`. Diferente de e-mail/data/categoria/
  tempo, um status não reconhecido **não invalida** o registro — o
  atendimento em si é válido, só o status fica sem valor.
- **Protocolo:** campo tratado como **obrigatório** de forma bloqueante,
  além dos campos com validação de formato — sem ele não é possível
  identificar duplicatas.
- **Duplicidade:** identificada pelo campo `protocolo`. Mantém-se a
  **primeira ocorrência**; ocorrências seguintes com o mesmo protocolo são
  descartadas e registradas no log.
- **Valores ausentes (`NaN`) do Pandas:** campos vazios do CSV são lidos
  pelo Pandas como `NaN` (tipo `float`), não como `None`/string vazia. Isso
  é tratado explicitamente antes da validação (conversão `NaN → None`),
  pois `NaN` é um valor "verdadeiro" em Python e passaria despercebido por
  checagens simples de campo vazio.
- **Tolerância a falhas:** cada linha do CSV é validada individualmente;
  uma linha inválida é registrada no log e descartada, sem interromper o
  processamento das demais.
- **Extração de telefone/protocolo do TXT:** não implementada nesta
  entrega, por decisão de priorização de tempo da dupla.

## Uso de ferramentas de IA

- **Ferramentas utilizadas:** Claude (Anthropic), Gemini e ChatGPT.
- **Finalidade:** apoio pedagógico e de desenvolvimento — explicação de
  conceitos (regex, Pandas, tratamento de exceções), revisão de código,
  depuração de erros de execução, sugestão de estrutura de funções e
  geração de parte da suíte de testes unitários.
- **Exemplos resumidos de solicitações feitas:**
  - "Como validar e-mail com regex?"
  - "Como remover duplicados de um DataFrame mantendo a primeira
    ocorrência?"
  - "Como fazer o gráfico de evolução por data ordenar corretamente?"
  - "Revisa esse `processamento.py` e aponta problemas antes de eu
    rodar."
  - "Otimize a visualização ao plotar os graficos"
- **Partes geradas/sugeridas por IA e revisadas pelos discentes:**
  - A função `construir_mapa_categorias`, em `validacao.py`, foi
    implementada após sugestão da IA, para facilitar a validação de
    categorias.
  - O arquivo `test_validacao.py` foi gerado com IA, a partir do
    `validacao.py` como entrada, solicitando um arquivo de testes pytest.
  - As instruções de ambiente virtual/instalação de dependências foram
     gerados com apoio de IA.
  - Todos os arquivos foram revisados com apoio de IA antes da entrega.
  - Tratamento de erros e debug foram feitos com IA.

## Testes

```bash
python -m pytest
```

Cobre as funções de `validacao.py`: validação de e-mail, telefone, data,
tempo de atendimento, categoria, status, extração de contatos do TXT e a
função orquestradora `validar_registro`.
