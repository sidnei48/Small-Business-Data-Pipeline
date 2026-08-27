# Apoio à gestão de pequenos negócios

## Sobre o projeto

O Small Business Data Pipeline é um projeto de Engenharia de Dados desenvolvido com o objetivo de organizar, processar e disponibilizar dados de um pequeno negócio para apoiar a gestão e a tomada de decisões.

Neste projeto, foi utilizado como cenário uma escola de idiomas, utilizando informações relacionadas a alunos, professores, turmas e matrículas.

O projeto implementa um pipeline capaz de realizar a extração, transformação, armazenamento e análise dos dados, transformando informações brutas de uma planilha em dados estruturados e disponíveis para análise.

## Objetivo

Desenvolver um pipeline de Engenharia de Dados capaz de coletar, tratar, armazenar e disponibilizar informações gerenciais para auxiliar a tomada de decisão em um pequeno negócio.

## Contexto

Pequenos negócios frequentemente armazenam informações importantes em planilhas e arquivos pouco estruturados, dificultando a organização, análise e utilização desses dados.

Neste projeto, foi utilizada como fonte de dados uma planilha de uma escola de idiomas contendo informações sobre alunos, professores, turmas e matrículas.

O projeto busca demonstrar como técnicas de Engenharia de Dados podem ser utilizadas para transformar esses dados brutos em informações estruturadas e indicadores úteis para a gestão.

## Arquitetura

<img width="1086" height="1448" alt="Arquitetura do projeto" src="https://github.com/user-attachments/assets/a277a10b-0ce1-41d4-aea1-91ee3928d593" />

## Tecnologias

- Python - Desenvolvimento do pipeline
- Pandas - Manipulação, limpeza e transformação dos dados
- PostgreSQL - Armazenamento dos dados
- SQL - Criação das tabelas, consultas e análise dos dados
- Psycopg - Comunicação entre Python e PostgreSQL
- Python-dotenv - Gerenciamento das variáveis de ambiente
- OpenPyXL - Leitura dos arquivos Excel
- Power BI - Visualização e criação do dashboard
- Git - Controle de versão
- GitHub - Hospedagem do código e documentação
- Visual Studio Code - Ambiente de desenvolvimento

## Ferramentas de apoio

- Notion - Organização das fases, tarefas e acompanhamento do desenvolvimento
- Inteligência Artificial - Apoio na revisão de código, explicação de conceitos, documentação e validação das etapas do projeto

## Pipeline

O pipeline foi desenvolvido seguindo as etapas de ETL:

1. Extração

Os dados são extraídos de uma planilha Excel utilizando Python e Pandas.

2. Transformação

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

3. Carga

Após o tratamento, os dados são armazenados em um banco de dados PostgreSQL estruturado nas tabelas de professores, turmas, alunos e matrículas.

4. Análise

Consultas SQL são utilizadas para validar os dados e gerar informações relevantes para a análise das matrículas e turmas.

5. Visualização

Os dados armazenados no PostgreSQL são utilizados no Power BI para criação de um dashboard com indicadores e filtros interativos.

## Dashboard

O dashboard apresenta informações relevantes para apoiar a análise das turmas e matrículas da escola.

Entre os indicadores apresentados estão:

- Matrículas ativas
- Matrículas canceladas
- Quantidade de alunos
- Quantidade de alunos ativos
- Média de alunos por turma
- Ocupação das turmas
- Alunos por professor
- Turmas por tipo
- Distribuição de matrículas por situação

## Estrutura do projeto

A estrutura do projeto está organizada da seguinte forma:

```text
small-business-data-pipeline/
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

1. Clonar o repositório

```bash
git clone https://github.com/sidnei48/Small-Business-Data-Pipeline.git
```

2. Acessar o diretório

```bash
cd Small-Business-Data-Pipeline
```

3. Criar o ambiente virtual

```bash
python -m venv .venv
```

4. Ativar o ambiente virtual

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

5. Instalar as dependências

```bash
pip install -r requirements.txt
```

6. Configurar o PostgreSQL

Criar o banco de dados e configurar as informações de conexão utilizando as variáveis de ambiente.

O arquivo `.env.example` pode ser utilizado como referência para a configuração.

7. Criar as tabelas

Executar os scripts SQL disponíveis em:

```text
sql/tables/
```

8. Executar o pipeline

```bash
python src/main.py
```

Após a execução, os dados tratados serão armazenados no PostgreSQL e estarão disponíveis para consultas SQL e visualização no Power BI.

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
- Disponibilizar as informações em um dashboard interativo no Power BI.

## Autor

Sidnei