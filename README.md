# Apoio à gestão de pequenos negócios
 
## Sobre o projeto
O Small Business Data Pipeline é um projeto de Engenharia de Dados desenvolvido com o objetivo de organizar, processar e disponibilizar dados de pequenos negócios para apoiar a gestão e a tomada de decisões.
O projeto propõe o desenvolvimento de um pipeline capaz de realizar a coleta, transformação, armazenamento e análise dos dados, transformando informações brutas em dados estruturados e úteis para o negócio.

## Objetivo
Desenvolver um pipeline de Engenharia de Dados capaz de coletar, tratar, armazenar e disponibilizar informações gerenciais para auxiliar a tomada de decisão em um pequeno negócio.

## Contexto
Pequenos negócios frequentemente possuem dados relacionados a vendas, clientes, produtos, serviços, estoque e faturamento, porém essas informações podem estar dispersas em diferentes arquivos ou sistemas.
O projeto busca demonstrar como técnicas de Engenharia de Dados podem ser utilizadas para organizar essas informações e gerar indicadores que auxiliem o gestor na análise do negócio.

## Arquitetura
<img width="1086" height="1448" alt="image" src="https://github.com/user-attachments/assets/a277a10b-0ce1-41d4-aea1-91ee3928d593" />

## Tecnologias
- Python - Desenvolvimento do pipeline
- Pandas - Manipulação e transformação dos dados
- PostgreSQL - Armazenamento dos dados
- SQL - Consultas e análise dos dados
- Power BI - Visualização e criação do dashboard
- Git - Controle de versão
- GitHub - Hospedagem do código e documentação
- Visual Studio Code - Ambiente de desenvolvimento

## Pipeline
O pipeline foi desenvolvido seguindo as etapas de ETL:

1. Extração
Os dados serão coletados a partir das fontes definidas para o projeto, como arquivos CSV, planilhas ou APIs.

2. Transformação
Os dados serão tratados utilizando Python e Pandas, incluindo:
Remoção de dados duplicados;
Tratamento de valores nulos;
Padronização de informações;
Correção de tipos de dados;
Padronização de datas;
Criação de novas informações;
Validação dos dados.

3. Carga
Após o tratamento, os dados serão armazenados em um banco de dados PostgreSQL.

4. Análise
Consultas SQL serão utilizadas para analisar os dados e gerar informações relevantes para o negócio.

5. Visualização
Os dados serão disponibilizados no Power BI por meio de um dashboard com indicadores gerenciais.

## Dashboard
O dashboard terá como objetivo apresentar informações relevantes para apoiar a gestão do pequeno negócio.
Entre os indicadores que poderão ser apresentados estão:
- Matrículas ativas
- Matrículas canceladas
- Quantidade de alunos
- Quantidade de alunos ativos
- Média de alunos por turma
- Ocupação das turmas
- Alunos por professor
- Turmas por tipo
- Distribuição de matrículas por situação

Status: 🚧 Em desenvolvimento

## Estrutura do projeto
A estrutura do projeto será organizada da seguinte forma:

small-business-data-pipeline/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── extraction/
│   ├── transformation/
│   ├── loading/
│   └── main.py
│
├── sql/
│   ├── tables/
│   └── queries/
│
├── dashboard/
│
├── docs/
│   ├── arquitetura/
│   ├── banco-de-dados/
│   └── pipeline/
│
├── tests/
│
├── .gitignore
├── requirements.txt
└── README.md

A estrutura poderá ser ajustada durante o desenvolvimento conforme novas necessidades surgirem.

## Como executar
1. Clonar o repositório
git clone https://github.com/sidnei48/small-business-data-pipeline.git

2. Acessar o diretório
cd small-business-data-pipeline

3. Criar o ambiente virtual
python -m venv .venv

4. Ativar o ambiente virtual
Windows PowerShell:
.venv\Scripts\Activate.ps1

5. Instalar as dependências
pip install -r requirements.txt

6. Configurar o PostgreSQL
Criar o banco de dados e configurar as informações de conexão conforme a documentação do projeto.

7. Executar o pipeline
python src/main.py

Observação: os comandos e configurações poderão ser atualizados conforme o desenvolvimento do projeto.

## Resultados
O projeto resultou em um pipeline ETL funcional capaz de:

- Extrair dados de uma planilha Excel;
- Tratar e padronizar os dados utilizando Python e Pandas;
- Remover duplicidades e validar informações;
- Armazenar os dados em um banco PostgreSQL estruturado;
- Executar consultas SQL para análise;
- Gerar indicadores sobre alunos, matrículas e turmas;
- Disponibilizar as informações em um dashboard no Power BI.

## Autor
Sidnei
