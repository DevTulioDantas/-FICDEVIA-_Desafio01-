from pathlib import Path
import logging
import json
import pandas as pd

#Caminhos de diretorios e arquivos
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

#Valida diretórios
def verificar_e_criar_diretorios() -> None:
    """Garante que as pastas data, output e output/graficos existam no projeto."""

    diretorios = [DATA, OUTPUT, GRAFICOS]

    try:
        for diretorio in diretorios:
            diretorio.mkdir(parents=True, exist_ok=True)

        logging.info('Diretórios verificados')   

    except PermissionError:
        logging.error("Sem autorização do sistema para criar as pastas.")      

    except Exception as e:
        logging.error(f"Erro inesperado ao criar diretórios: {e}")

# Valida e Lê um JSON
def carregar_json(caminho_arquivo: Path) -> dict | None:
    """Lê e carrega um arquivo JSON. Trata arquivos ausentes ou corrompidos."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
            logging.info(f"JSON '{caminho_arquivo.name}' carregado com sucesso!")
            return dados
    except FileNotFoundError:
        logging.error(f"Arquivo JSON não encontrado: {caminho_arquivo.name}")
        return None
    except json.JSONDecodeError:
        logging.error(f"O arquivo JSON '{caminho_arquivo.name}' está corrompido/inválido.")
        return None
    except Exception as e:
        logging.error(f"Erro inesperado ao ler JSON '{caminho_arquivo.name}': {e}")
        return None


# Valida e Lê um CSV
def carregar_csv(caminho_arquivo: Path, separador: str = ";") -> pd.DataFrame | None:
    """Lê um arquivo CSV para um DataFrame do Pandas."""
    try:
        df = pd.read_csv(caminho_arquivo, sep=separador, encoding="utf-8")
        logging.info(f"CSV '{caminho_arquivo.name}' carregado com sucesso! ({len(df)} linhas)")
        return df
    except FileNotFoundError:
        logging.error(f"Arquivo CSV não encontrado: {caminho_arquivo.name}")
        return None
    except Exception as e:
        logging.error(f"Erro inesperado ao ler CSV '{caminho_arquivo.name}': {e}")
        return None


# Valida e Lê um Excel
def carregar_excel(caminho_arquivo: Path) -> pd.DataFrame | None:
    """Lê um arquivo Excel (.xlsx) para um DataFrame do Pandas."""
    try:
        df = pd.read_excel(caminho_arquivo)
        logging.info(f"Excel '{caminho_arquivo.name}' carregado com sucesso! ({len(df)} linhas)")
        return df
    except FileNotFoundError:
        logging.error(f"Arquivo Excel não encontrado: {caminho_arquivo.name}")
        return None
    except Exception as e:
        logging.error(f"Erro inesperado ao ler Excel '{caminho_arquivo.name}': {e}")
        return None

#Valida e Lê um TXT
def carregar_txt(caminho_arquivo: Path) -> list[str] | None:
    """Lê um arquivo de texto (.txt) e retorna uma lista com suas linhas."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            logging.info(f"TXT '{caminho_arquivo.name}' carregado com sucesso! ({len(linhas)} linhas)")
            return linhas

    except FileNotFoundError:
        logging.error(f"Arquivo TXT não encontrado: {caminho_arquivo.name}")
        return None
    except UnicodeDecodeError:
        logging.error(f"Erro de codificação ao ler o TXT '{caminho_arquivo.name}'. Verifique o encoding.")
        return None
    except Exception as e:
        logging.error(f"Erro inesperado ao ler TXT '{caminho_arquivo.name}': {e}")
        return None