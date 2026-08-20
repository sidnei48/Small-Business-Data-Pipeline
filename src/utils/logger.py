import logging
from pathlib import Path


RAIZ_PROJETO = Path(__file__).resolve().parents[2]
PASTA_LOGS = RAIZ_PROJETO / "logs"
ARQUIVO_LOG = PASTA_LOGS / "pipeline.log"

PASTA_LOGS.mkdir(
    parents=True,
    exist_ok=True
)

logger = logging.getLogger("pipeline")
logger.setLevel(logging.INFO)

formatador = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

arquivo_handler = logging.FileHandler(
    ARQUIVO_LOG,
    encoding="utf-8"
)

arquivo_handler.setFormatter(formatador)

terminal_handler = logging.StreamHandler()
terminal_handler.setFormatter(formatador)

if not logger.handlers:
    logger.addHandler(arquivo_handler)
    logger.addHandler(terminal_handler)

logger.propagate = False