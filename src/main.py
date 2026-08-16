from src import *
import pandas as pd
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ /"data"
CONFIG = DATA / "config.json"


def main():

    config = carregar_json(CONFIG)
    atendimento = carregar_csv(config['arquivo_atendimentos'])

    ATENDIMENTO_FILE = RAIZ/ config['arquivo_atendimentos']
    CATEGORIA_FILE = RAIZ/ config['arquivo_categorias']
    OBSERVACAO_FILE = RAIZ/ config['arquivo_observacoes']
    SAIDA = RAIZ/config['diretorio_saida']
    SEPARADOR = config['separador_csv']

    df_atendimentos = carregar_csv(ATENDIMENTO_FILE, SEPARADOR)
    dict_categorias = carregar_json(CATEGORIA_FILE)
    txt_observacoes = carregar_txt(OBSERVACAO_FILE)

    

if __name__ == "__main__":
    main()