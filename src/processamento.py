import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

#Calculo de indicadores
def quantidade_total_atendimento (df: pd.DataFrame) -> int:
    """
    Calcula a quantidade total de atendimentos registrados.
    
    Args:
        df (pd.DataFrame): Data frame do Atendimento.
    
    Returns:
        Int: Quantidade total de antendimentos.

    """
    return len(df)

def quantidade_por_categoria (df: pd.DataFrame) -> dict:
    """
    Calcula a quantidade de cada categoria e retorna como um dict

    Args:
        df (pd.DataFrame): Data frame do Atendimento.
    
    Returns:
        Dict: Quantidade total de antendimentos por categoria.

    """
    return df['categoria'].value_counts().to_dict()

def quantidade_por_status (df: pd.DataFrame) -> dict:
    """
    Calcula a quantidade de cada status e retorna como um dict

    Args:
        df (pd.DataFrame): Data frame do Atendimento.
    
    Returns:
        Dict: Quantidade total de antendimentos por status.

    """
    return df['status'].value_counts().to_dict()

def tempo_medio_atendimento (df: pd.DataFrame) -> float:
    """
    Calcula o tempo médio de atendimento em minutos.

     Args:
        df (pd.DataFrame): Data frame do Atendimento.
        
    Returns:
        Float: Quantidade medio de atendimento em Minutos, arredondado em duas casas decimais.

    Example:
        >>> tempo_medio_de_atendimento(df)
        13.8  # Representa 13 minutos e 48 segundos (0.8 * 60)
    """
    media = np.mean(df["tempo_minutos"])
    return float(np.round(media, 2))

def categoria_maior_numero_solicitacoes(df: pd.DataFrame) -> str:
    """
    Identifica a categoria com o maior número de atendimentos registrados.

    Args:
        df (pd.DataFrame): DataFrame com os registros de atendimento.

    Returns:
        str: O nome da categoria mais frequente.

    Example:
        >>> categoria_com_maior_numero_de_solicitacoes(df)
        'Suporte'
    """
    return str(df["categoria"].value_counts().idxmax())

def percentual_registros_invalidos_incompletos(df: pd.DataFrame) -> float:
    """Calcula a porcentagem de registros que possuem dados ausentes ou nulos.

    Args:
        df (pd.DataFrame): DataFrame com os registros de atendimento.

    Returns:
        float: Percentual de linhas incompletas (de 0.0 a 100.0), arredondado em 2 casas.

    Example:
        >>> percentual_registros_invalidos_ou_incompletos(df)
        5.25  # Significa que 5.25% das linhas possuem algum campo em branco
    """    

    quant_linhas = len(df)

    if quant_linhas == 0:
        return 0.0

    # Conta quantas linhas têm pelo menos 1 valor ausente (NaN)
    linhas_incompletas = df.isna().any(axis=1).sum()

    percentual = np.divide(linhas_incompletas, quant_linhas) * 100

    return float(np.round(percentual, 2))




def remover_duplicados_por_protocolo(df: pd.DataFrame) -> pd.DataFrame:
    """Remove registros com protocolo duplicado

    Args:
        df (pd.DataFrame):

    Returns:
        pd.DataFrame: DataFrame com tratamento e duplicados
    """
    duplicados = df[df.duplicated(subset="protocolo", keep="first")]

    if not duplicados.empty:
        logger.warning(
            f"{len(duplicados)} registro(s) duplicado(s) removido(s): "
            f"{duplicados['protocolo'].tolist()}"
        )

    return df.drop_duplicates(subset="protocolo", keep="first").reset_index(drop=True)

    
