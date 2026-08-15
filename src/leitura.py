from pathlib import Path
import logging
import json
#import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ/'data'
OUTPUT = RAIZ/'output'
GRAFICOS = OUTPUT/'graficos'
LOG_FILE = OUTPUT/'erros.log'

#Configuração básica do Log
OUTPUT.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def verificar_e_criar_diretorios() -> None:
    """Garante que as pastas data, output e output/graficos existam no projeto."""

    diretorios = [DATA, OUTPUT, GRAFICOS]

    try:
        for diretorio in diretorios:
            diretorio.mkdir(parents=True, exist_ok=True)

        logging.info('diretorios verificados')   

    except PermissionError:
        logging.error("Sem autorização do sistema para criar as pastas.")      

    except Exception as e:
        logging.error(f"Erro inesperado ao criar diretórios: {e}")



