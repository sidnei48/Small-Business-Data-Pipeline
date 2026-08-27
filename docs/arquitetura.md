# Arquitetura do Projeto

O Small Business Data Pipeline utiliza uma arquitetura ETL para transformar dados brutos de uma planilha em informações estruturadas e disponíveis para análise.

O fluxo do projeto é composto pelas seguintes etapas:

Excel
↓
Python / Pandas
↓
PostgreSQL
↓
SQL
↓
Power BI

## Fonte de dados

Os dados são extraídos de uma planilha Excel contendo informações relacionadas a alunos, professores, turmas e matrículas.

## Extração

A etapa de extração utiliza Python e Pandas para realizar a leitura dos dados da planilha original.

## Transformação

Durante a transformação, os dados passam por processos de limpeza, padronização e validação, incluindo:

- remoção de registros duplicados;
- tratamento de valores nulos;
- padronização de nomes;
- correção dos tipos de dados;
- identificação de turmas;
- identificação de professores;
- classificação do tipo de turma;
- padronização de dias e horários;
- validação das matrículas.

## Armazenamento

Após o tratamento, os dados são armazenados em um banco PostgreSQL organizado nas tabelas:

- professor;
- turma;
- aluno;
- matricula.

## Análise

Consultas SQL são utilizadas para validar os dados e gerar informações relacionadas às matrículas, alunos e ocupação das turmas.

## Visualização

O Power BI se conecta ao banco PostgreSQL e apresenta os dados através de indicadores, gráficos, tabelas e filtros interativos.