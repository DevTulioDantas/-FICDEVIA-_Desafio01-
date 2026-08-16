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
 
def exportar_graficos(df: pd.DataFrame) -> None:
    """
    Gera 4 gráficos analíticos e salva cada um como um arquivo PNG separado.

    Esta função utiliza a biblioteca Matplotlib para criar visualizações
    baseadas no DataFrame fornecido e as salva no diretório configurado.

    Args:
        df (pd.DataFrame): O DataFrame contendo os dados já limpos e processados.
                           Deve conter obrigatoriamente as colunas 'categoria', 
                           'tempo_minutos', 'status' e 'data'.

    Returns:
        None: A função não retorna dados na memória. Seu objetivo final é 
              salvar os arquivos físicos (.png) no disco.

    Example:
        >>> import pandas as pd
        >>> dados = {
        ...     "categoria": ["python", "senha", "software"],
        ...     "tempo_minutos": [40, 15, 120],
        ...     "status": ["aberto", "resolvido", "em andamento"],
        ...     "data": ["2026-07-01", "2026-07-02", "2026-07-02"]
        ... }
        >>> df_exemplo = pd.DataFrame(dados)
        >>> exportar_graficos(df_exemplo)
        # O terminal registrará o log de sucesso e as 4 imagens PNG 
        # aparecerão na pasta 'output/graficos/'.
    """
    
    try:
        # Garante que a pasta 'output/graficos' exista
        GRAFICOS.mkdir(parents=True, exist_ok=True)

        # 1. Gráfico: Atendimentos por Categoria (Barras)
        plt.figure(figsize=(10, 6)) # Cria uma "folha" nova
        contagem_categoria = df["categoria"].value_counts()
        
        contagem_categoria.plot(kind="bar", color="cornflowerblue", edgecolor="black")
        plt.title("Volume de Atendimentos por Categoria", fontsize=14)
        plt.xlabel("Categoria")
        plt.ylabel("Quantidade")
        plt.xticks(rotation=45, ha="right") # Inclina os textos para não sobrepor
        plt.tight_layout() # Ajusta as margens
        
        plt.savefig(GRAFICOS / "1_atendimentos_por_categoria.png")
        plt.close() 

        
        # 2. Gráfico: Distribuição do Tempo de Atendimento (Histograma)
        plt.figure(figsize=(10, 6))
        
        df["tempo_minutos"].plot(kind="hist", bins=15, color="lightcoral", edgecolor="black")
        plt.title("Distribuição dos Tempos de Atendimento", fontsize=14)
        plt.xlabel("Tempo (minutos)")
        plt.ylabel("Frequência (Quantidade de Chamados)")
        plt.tight_layout()
        
        plt.savefig(GRAFICOS / "2_distribuicao_tempo.png")
        plt.close()


        # 3. Gráfico: Proporção de Status (Pizza)
        plt.figure(figsize=(8, 8))
        contagem_status = df["status"].value_counts()
        
        # Cores para cada status padrão
        cores = ["mediumseagreen", "gold", "tomato"] 
        contagem_status.plot(
            kind="pie", 
            autopct="%1.1f%%", # Mostra a porcentagem no gráfico
            startangle=90, 
            colors=cores[:len(contagem_status)]
        )
        plt.title("Proporção de Atendimentos por Status", fontsize=14)
        plt.ylabel("")
        plt.tight_layout()
        
        plt.savefig(GRAFICOS / "3_proporcao_status.png")
        plt.close()

        # 4. Gráfico: Evolução de Atendimentos por Dia (Linha)
        plt.figure(figsize=(12, 5))
        
        # Agrupa contando quantos chamados ocorreram em cada data
        contagem_data = df.groupby("data").size()
        
        contagem_data.plot(kind="line", marker="o", color="darkorange", linewidth=2)
        plt.title("Evolução do Volume de Atendimentos por Dia", fontsize=14)
        plt.xlabel("Data")
        plt.ylabel("Quantidade de Chamados")
        plt.grid(True, linestyle="--", alpha=0.7) # Adiciona linhas de grade no fundo
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        
        plt.savefig(GRAFICOS / "4_evolucao_por_dia.png")
        plt.close()

        logging.info(" Todos os 4 gráficos foram gerados com sucesso na pasta 'output/graficos'.")

    except Exception as e:
        logging.error(f" Erro ao gerar gráficos: {e}")