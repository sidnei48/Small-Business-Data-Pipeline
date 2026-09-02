# Apoio à gestão de pequenos negócios

## Sobre o projeto

O Small Business Data Pipeline é um projeto de Engenharia de Dados desenvolvido com o objetivo de organizar, processar e disponibilizar dados de um pequeno negócio para apoiar a gestão e a tomada de decisões.

Neste projeto, foi utilizado como cenário uma escola de idiomas, utilizando informações relacionadas a alunos, professores, turmas e matrículas.

O projeto implementa um pipeline capaz de realizar a extração, transformação, armazenamento e análise dos dados, transformando informações brutas de uma planilha em dados estruturados e disponíveis para análise.

Além do pipeline, foi desenvolvida uma aplicação web interativa conectada ao banco de dados, permitindo visualizar indicadores e gráficos diretamente pelo navegador.

## Objetivo

Desenvolver um pipeline de Engenharia de Dados capaz de coletar, tratar, armazenar e disponibilizar informações gerenciais para auxiliar a tomada de decisão em um pequeno negócio.

O projeto também busca facilitar o acesso às informações através de uma interface web interativa, permitindo que os dados sejam analisados de maneira mais simples e visual.

## Contexto

Pequenos negócios frequentemente armazenam informações importantes em planilhas e arquivos pouco estruturados, dificultando a organização, análise e utilização desses dados.

Neste projeto, foi utilizada como fonte de dados uma planilha de uma escola de idiomas contendo informações sobre alunos, professores, turmas e matrículas.

O projeto busca demonstrar como técnicas de Engenharia de Dados podem ser utilizadas para transformar esses dados brutos em informações estruturadas e indicadores úteis para a gestão.

## Arquitetura

<img width="1086" height="1448" alt="Arquitetura do projeto" src="https://github.com/user-attachments/assets/a277a10b-0ce1-41d4-aea1-91ee3928d593" />

O fluxo principal do projeto pode ser representado da seguinte forma:

```text
Planilha Excel
      ↓
Python / Pandas
      ↓
PostgreSQL
      ↓
FastAPI
      ↓
JavaScript
      ↓
Dashboard Web Interativo
```

O Power BI também é utilizado como ferramenta de visualização e análise dos dados armazenados no PostgreSQL.

## Tecnologias

- Python - Desenvolvimento do pipeline e da API
- Pandas - Manipulação, limpeza e transformação dos dados
- PostgreSQL - Armazenamento dos dados
- SQL - Criação das tabelas, consultas e análise dos dados
- Psycopg - Comunicação entre Python e PostgreSQL
- Python-dotenv - Gerenciamento das variáveis de ambiente
- OpenPyXL - Leitura dos arquivos Excel
- FastAPI - Desenvolvimento da API utilizada pela aplicação web
- Uvicorn - Servidor utilizado para executar a API
- HTML - Estrutura da aplicação web
- CSS - Estilização e responsividade da página
- JavaScript - Comunicação com a API e interatividade do dashboard
- Chart.js - Criação dos gráficos interativos
- Power BI - Visualização e criação do dashboard
- Git - Controle de versão
- GitHub - Hospedagem do código e documentação
- Visual Studio Code - Ambiente de desenvolvimento

## Ferramentas de apoio

- Notion - Organização das fases, tarefas e acompanhamento do desenvolvimento
- Inteligência Artificial - Apoio na revisão de código, explicação de conceitos, documentação e validação das etapas do projeto

## Pipeline

O pipeline foi desenvolvido seguindo as etapas de ETL:

### 1. Extração

Os dados são extraídos de uma planilha Excel utilizando Python e Pandas.

### 2. Transformação

Os dados são tratados utilizando Python e Pandas, incluindo:

- Remoção de dados duplicados;
- Tratamento de valores nulos;
- Padronização de nomes e informações;
- Correção de tipos de dados;
- Identificação de alunos, professores e turmas;
- Padronização de dias e horários;
- Classificação dos tipos de turma;
- Validação das matrículas;
- Criação de novas informações utilizadas durante o processamento.

### 3. Carga

Após o tratamento, os dados são armazenados em um banco de dados PostgreSQL estruturado nas tabelas de professores, turmas, alunos e matrículas.

### 4. Análise

Consultas SQL são utilizadas para validar os dados e gerar informações relevantes para a análise das matrículas e turmas.

### 5. Visualização

Os dados armazenados no PostgreSQL podem ser analisados através do Power BI e também por meio da aplicação web desenvolvida para o projeto.

A aplicação web utiliza uma API construída com FastAPI para consultar o PostgreSQL e disponibilizar os dados para o dashboard interativo.

## Aplicação Web

Como evolução do projeto, foi desenvolvida uma aplicação web para tornar a visualização dos dados mais acessível e interativa.

A aplicação utiliza uma API desenvolvida com FastAPI para consultar os dados armazenados no PostgreSQL.

O frontend foi desenvolvido utilizando HTML, CSS e JavaScript, enquanto os gráficos são gerados utilizando Chart.js.

O fluxo da aplicação funciona da seguinte forma:

```text
PostgreSQL
    ↓
FastAPI
    ↓
JSON
    ↓
JavaScript
    ↓
Dashboard Interativo
```

Os filtros selecionados pelo usuário são enviados para a API, que realiza novas consultas no banco de dados e retorna os valores atualizados para os indicadores e gráficos.

## Dashboard

O dashboard apresenta informações relevantes para apoiar a análise das turmas e matrículas da escola.

Entre os indicadores apresentados estão:

- Matrículas ativas
- Matrículas canceladas
- Quantidade de alunos ativos
- Média de alunos por turma
- Ocupação das turmas
- Alunos ativos por professor
- Turmas por tipo
- Distribuição de matrículas por situação

O dashboard web possui filtros interativos por:

- Professor
- Idioma
- Tipo de turma

Ao selecionar um filtro, os indicadores e gráficos são atualizados automaticamente utilizando dados consultados diretamente no PostgreSQL.

Entre os gráficos disponíveis estão:

- Matrículas por situação
- Alunos ativos por professor
- Turmas por tipo
- Ocupação das turmas

## API

A API foi desenvolvida utilizando FastAPI e funciona como uma camada de comunicação entre o banco PostgreSQL e a aplicação web.

Entre os principais endpoints estão:

```text
GET /
GET /indicadores
GET /filtros
GET /graficos/alunos-professor
GET /graficos/turmas-tipo
GET /graficos/ocupacao-turmas
```

Os endpoints dos indicadores e gráficos permitem utilizar filtros como:

```text
professor
idioma
tipo_turma
```

Exemplo:

```text
/indicadores?professor=Bianca&idioma=Inglês
```

A documentação automática da API pode ser acessada através do Swagger disponibilizado pelo FastAPI.

## Estrutura do projeto

A estrutura do projeto está organizada da seguinte forma:

```text
small-business-data-pipeline/
│
├── api/
│   ├── main.py
│   └── queries.py
│
├── data/
│   └── raw/
│
├── src/
│   ├── config/
│   ├── extraction/
│   ├── transformation/
│   ├── loading/
│   ├── utils/
│   └── main.py
│
├── sql/
│   ├── tables/
│   └── queries/
│
├── web/
│   ├── assets/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── powerbi/
│   └── bussines_small.pbix
│
├── docs/
│   ├── arquitetura.md
│   ├── banco-de-dados.md
│   ├── pipeline.md
│   └── tecnologias.md
│
├── tests/
│   └── data/
│
├── logs/
│   └── pipeline.log
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/sidnei48/Small-Business-Data-Pipeline.git
```

### 2. Acessar o diretório

```bash
cd Small-Business-Data-Pipeline
```

### 3. Criar o ambiente virtual

```bash
python -m venv .venv
```

### 4. Ativar o ambiente virtual

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Configurar o PostgreSQL

Criar o banco de dados e configurar as informações de conexão utilizando as variáveis de ambiente.

O arquivo `.env.example` pode ser utilizado como referência para a configuração.

### 7. Criar as tabelas

Executar os scripts SQL disponíveis em:

```text
sql/tables/
```

### 8. Executar o pipeline

```bash
python src/main.py
```

Após a execução, os dados tratados serão armazenados no PostgreSQL.

### 9. Executar a API

Com o ambiente virtual ativado, executar:

```bash
uvicorn api.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

A documentação automática da API pode ser acessada em:

```text
http://127.0.0.1:8000/docs
```

### 10. Abrir a aplicação web

Abrir o arquivo:

```text
web/index.html
```

A aplicação utilizará a API para consultar os dados armazenados no PostgreSQL e atualizar os indicadores e gráficos.

Para que o dashboard funcione corretamente, a API deve permanecer em execução.

## Resultados

O projeto resultou em um pipeline ETL funcional capaz de:

- Extrair dados de uma planilha Excel;
- Tratar e padronizar os dados utilizando Python e Pandas;
- Remover duplicidades e validar informações;
- Organizar dados de alunos, professores, turmas e matrículas;
- Armazenar os dados em um banco PostgreSQL estruturado;
- Atualizar registros já existentes no banco;
- Registrar as execuções através de logs;
- Executar consultas SQL para análise e validação;
- Gerar indicadores sobre alunos, matrículas e turmas;
- Disponibilizar informações através de uma API desenvolvida com FastAPI;
- Criar uma aplicação web para apresentação dos dados;
- Permitir filtros interativos por professor, idioma e tipo de turma;
- Atualizar indicadores e gráficos utilizando dados consultados diretamente do PostgreSQL;
- Disponibilizar as informações em um dashboard interativo desenvolvido com JavaScript e Chart.js;
- Disponibilizar também um dashboard desenvolvido no Power BI.

## Autor

Sidnei