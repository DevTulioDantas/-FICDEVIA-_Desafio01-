import json
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
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
def gerar_dicionario_indicadores(df: pd.DataFrame, percentual_invalidos: float) -> dict:
    """Consolida todos os indicadores processados do DataFrame em um dicionário.

    Args:
        df (pd.DataFrame): DataFrame já validado, sem duplicados e padronizado.
        percentual_invalidos (float): Percentual de registros rejeitados na
            validação, calculado sobre o TOTAL ORIGINAL do CSV (não sobre
            este df, que já contém só os registros válidos).
    """
    return {
        "quantidade_total_atendimentos": quantidade_total_atendimento(df),
        "quantidade_por_categoria": quantidade_por_categoria(df),
        "quantidade_por_status": quantidade_por_status(df),
        "tempo_medio_atendimento": tempo_medio_atendimento(df),
        "categoria_mais_solicitada": categoria_maior_numero_solicitacoes(df),
        "percentual_registros_invalidos": percentual_invalidos,
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
        plt.rcParams["savefig.dpi"] = 150  # imagens mais nítidas

        # 1. Gráfico: Atendimentos por Categoria (Barras)
        plt.figure(figsize=(10, 6))
        contagem_categoria = df["categoria"].value_counts()

        # Cor fixa POR NOME de categoria, não por posição — assim a cor
        # de cada categoria não muda de execução para execução, mesmo
        # que a ordem de frequência entre elas mude com novos dados
        mapa_cores_categoria = {
            "Acesso ao AVA": "#08519c",
            "Instalação de programas": "#3182bd",
            "Execução de atividades": "#6baed6",
            "Senha": "#9ecae1",
            "Configuração do Python": "#c6dbef",
        }
        cores_categoria = [mapa_cores_categoria.get(c, "lightgray") for c in contagem_categoria.index]

        eixo = contagem_categoria.plot(kind="bar", color=cores_categoria, edgecolor="black")

        eixo.bar_label(eixo.containers[0], padding=3, fontsize=10)  # valor em cima da barra
        plt.title("Volume de Atendimentos por Categoria", fontsize=14, fontweight="bold")
        plt.xlabel("Categoria")
        plt.ylabel("Quantidade")
        plt.xticks(rotation=45, ha="right")
        plt.grid(axis="y", linestyle="--", alpha=0.4)
        plt.margins(y=0.1)  # espaço extra no topo para o rótulo não cortar
        plt.tight_layout()

        plt.savefig(GRAFICOS / "1_atendimentos_por_categoria.png")
        plt.close()


        # 2. Gráfico: Distribuição do Tempo de Atendimento (Histograma)
        plt.figure(figsize=(10, 6))

        media_tempo = df["tempo_minutos"].mean()
        mediana_tempo = df["tempo_minutos"].median()

        df["tempo_minutos"].plot(kind="hist", bins=20, color="lightcoral", edgecolor="black", alpha=0.85)
        plt.axvline(media_tempo, color="darkred", linestyle="--", linewidth=2,
                    label=f"Média: {media_tempo:.1f} min")
        plt.axvline(mediana_tempo, color="steelblue", linestyle=":", linewidth=2,
                    label=f"Mediana: {mediana_tempo:.1f} min")

        plt.title("Distribuição dos Tempos de Atendimento", fontsize=14, fontweight="bold")
        plt.xlabel("Tempo (minutos)")
        plt.ylabel("Frequência (Quantidade de Chamados)")
        plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(10))
        plt.grid(axis="y", linestyle="--", alpha=0.4)
        plt.legend()
        plt.tight_layout()

        plt.savefig(GRAFICOS / "2_distribuicao_tempo.png")
        plt.close()


        # 3. Gráfico: Proporção de Status (Pizza)
        plt.figure(figsize=(8, 8))
        contagem_status = df["status"].value_counts()

        # Cor fixa POR NOME de status, não por posição — assim a cor de
        # "resolvido" nunca muda de um gráfico para o outro, mesmo que a
        # ordem de frequência mude entre execuções
        mapa_cores_status = {
            "resolvido": "mediumseagreen",
            "em andamento": "gold",
            "aberto": "tomato",
        }
        cores_status = [mapa_cores_status.get(s, "lightgray") for s in contagem_status.index]

        contagem_status.plot(
            kind="pie",
            autopct="%1.1f%%",
            startangle=90,
            colors=cores_status,
            textprops={"fontsize": 11},
            wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        )
        plt.title("Proporção de Atendimentos por Status", fontsize=14, fontweight="bold")
        plt.ylabel("")
        plt.legend(
            contagem_status.index, title="Status", loc="center left",
            bbox_to_anchor=(1.0, 0.5),
        )
        plt.tight_layout()

        plt.savefig(GRAFICOS / "3_proporcao_status.png", bbox_inches="tight")
        plt.close()

        # 4. Gráfico: Evolução de Atendimentos por Dia (Linha)
        plt.figure(figsize=(12, 5))

        # As datas estão como texto DD/MM/AAAA — convertemos para
        # datetime só para agrupar/ordenar corretamente (senão o
        # Pandas ordena as strings alfabeticamente, não por data real)
        datas_ordenaveis = pd.to_datetime(df["data"], format="%d/%m/%Y")
        contagem_data = df.groupby(datas_ordenaveis).size()
        contagem_data.index = contagem_data.index.strftime("%d/%m/%Y")

        contagem_data.plot(kind="line", marker="o", color="darkorange", linewidth=2)
        plt.fill_between(range(len(contagem_data)), contagem_data.values, alpha=0.15, color="darkorange")
        plt.title("Evolução do Volume de Atendimentos por Dia", fontsize=14, fontweight="bold")
        plt.xlabel("Data")
        plt.ylabel("Quantidade de Chamados")
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        plt.savefig(GRAFICOS / "4_evolucao_por_dia.png")
        plt.close()

        logging.info(" Todos os 4 gráficos foram gerados com sucesso na pasta 'output/graficos'.")

    except Exception as e:
        logging.error(f" Erro ao gerar gráficos: {e}")

def exportar_csv_tratado(
    df: pd.DataFrame, caminho: Path = OUTPUT / "atendimentos_processados.csv"
) -> None:
    """Exporta o DataFrame de atendimentos

    Args:
        df (pd.DataFrame): DataFrame contendo os registros já validados,
            padronizados e sem duplicados.
        caminho (Path): Caminho onde o CSV será salvo padrão é
            'output/atendimentos_processados.csv'    
    """
    try:
        caminho.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(caminho, index=False, sep=";", encoding="utf-8")

        logging.info(f"CSV tratado salvo com sucesso em: {caminho} ({len(df)} linhas)")

    except Exception as e:
        logging.error(f"Erro ao tentar salvar o CSV tratado '{caminho}': {e}")