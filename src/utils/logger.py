import logging
from pathlib import Path


# Define onde o arquivo de log será salvo
RAIZ_PROJETO = Path(__file__).resolve().parents[2]
PASTA_LOGS = RAIZ_PROJETO / "logs"
ARQUIVO_LOG = PASTA_LOGS / "pipeline.log"

# Cria a pasta de logs caso ela ainda não exista
PASTA_LOGS.mkdir(
    parents=True,
    exist_ok=True
)

# Cria o logger principal do pipeline
logger = logging.getLogger("pipeline")
logger.setLevel(logging.INFO)

# Define o formato das mensagens registradas
formatador = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Salva os logs no arquivo pipeline.log
arquivo_handler = logging.FileHandler(
    ARQUIVO_LOG,
    encoding="utf-8"
)

arquivo_handler.setFormatter(formatador)

# Mostra os mesmos logs também no terminal
terminal_handler = logging.StreamHandler()
terminal_handler.setFormatter(formatador)

# Evita adicionar os mesmos handlers mais de uma vez
if not logger.handlers:
    logger.addHandler(arquivo_handler)
    logger.addHandler(terminal_handler)

# Evita duplicação das mensagens em outros loggers
logger.propagate = False