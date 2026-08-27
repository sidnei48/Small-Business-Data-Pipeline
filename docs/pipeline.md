# Pipeline ETL

O projeto utiliza um pipeline ETL para extrair, transformar e carregar os dados da escola.

## Extração

Os dados são lidos a partir de uma planilha Excel utilizando Python e Pandas.

Nesta etapa, o pipeline identifica as linhas que representam alunos e associa cada registro à sua turma correspondente.

## Transformação

Durante a transformação, os dados passam por diferentes etapas de limpeza e padronização.

Entre os principais tratamentos realizados estão:

- remoção de registros duplicados;
- tratamento de valores nulos;
- padronização de nomes;
- correção de tipos de dados;
- identificação da turma de cada aluno;
- separação de nível, idioma, tipo de turma e professor;
- padronização de dias e horários;
- identificação da capacidade máxima das turmas;
- validação das situações de matrícula.

Quando existem registros duplicados para o mesmo aluno e turma, a matrícula ativa recebe prioridade sobre a matrícula cancelada.

## Carga

Após o tratamento, os dados são enviados para o PostgreSQL.

A carga é realizada seguindo a ordem necessária para manter os relacionamentos do banco:

1. Professores
2. Turmas
3. Alunos
4. Matrículas

Durante a carga, o pipeline também verifica registros que já existem no banco.

Professores já cadastrados não são inseridos novamente.

Turmas existentes podem ter sua capacidade máxima atualizada.

Alunos existentes podem ter seus nomes atualizados.

Matrículas existentes podem ter sua situação atualizada.

## Validações

Antes de enviar os dados para o banco, o pipeline realiza validações para evitar inconsistências.

São verificados:

- campos obrigatórios vazios;
- situações de matrícula inválidas;
- capacidades máximas inválidas;
- professores sem identificação;
- turmas duplicadas;
- alunos duplicados;
- matrículas duplicadas;
- registros sem turma correspondente.

Caso algum problema seja encontrado, a execução é interrompida e o erro é registrado.

## Logs

O pipeline possui um sistema de logs que registra informações sobre cada execução.

Os logs apresentam informações como:

- início do pipeline;
- quantidade de registros transformados;
- professores processados;
- turmas processadas;
- alunos processados;
- matrículas processadas;
- finalização do pipeline;
- erros encontrados durante a execução.

Os registros são exibidos no terminal e também armazenados no arquivo:

`logs/pipeline.log`

## Execução

O pipeline principal pode ser executado com:

```bash
python src/main.py
```

Ao final de uma execução sem erros, os dados tratados estarão armazenados no PostgreSQL e disponíveis para consultas SQL e análise no Power BI.