import json
import os
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import logging

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

#nota:precisa importar desse jeito as funções src para garantir que não dar erro ao rodar o main
from .processamento import (
    categoria_maior_numero_solicitacoes,
    percentual_registros_invalidos_incompletos,
    quantidade_por_categoria,
    quantidade_por_status,
    quantidade_total_atendimento,
    tempo_medio_atendimento,
)

#cria um dict para todos os indicadores pedido no Desafio
def gerar_dicionario_indicadores(df: pd.DataFrame) -> dict:
    """Consolida todos os indicadores processados do DataFrame em um dicionário."""
    return {
        "quantidade_total_atendimentos": quantidade_total_atendimento(df),
        "quantidade_por_categoria": quantidade_por_categoria(df),
        "quantidade_por_status": quantidade_por_status(df),
        "tempo_medio_atendimento": tempo_medio_atendimento(df),
        "categoria_mais_solicitada": categoria_maior_numero_solicitacoes(df),
        "percentual_registros_invalidos": percentual_registros_invalidos_incompletos(df),
    }

#exporta o dict feito anteriomente para um resumo.json por padrão ou outra rota 
def exportar_resumo_json(  indicadores: dict, caminho: Path = OUTPUT / "resumo.json") -> None:
    """
    Recebe um dicionário com os indicadores e salva em um arquivo JSON.
    
    Args:
        indicadores (dict): Dicionário contendo os indicadores já calculados.
        caminho (str): Caminho onde o arquivo JSON será salvo. Padrão é 'output/resumo.json'.
        
    Example:
        >>> meu_dicionario = {"total_atendimentos": 150}
        >>> exportar_resumo_json(meu_dicionario)
    """
    try:
        caminho.parent.mkdir(parents=True, exist_ok=True)

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(indicadores, arquivo, indent=4, ensure_ascii=False)
            
        logging.info(f"Arquivo salvo com sucesso em: {caminho}")

    except Exception as e:
        # Registra o erro no output/erros.log silenciosamente, sem quebrar o programa
        logging.error(f"Erro ao tentar salvar o arquivo JSON '{caminho}': {e}")
 
