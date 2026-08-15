import re
from datetime import datetime


def email_valido(email:str) -> bool:
    """_summary_

    Args:
        email (str): endereço de email do aluno

    Returns:
        bool: True se o campo for um email e false se não for
    """
    padrao_email = re.compile(
    r'[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[a-zA-Z]{2,}',
    re.IGNORECASE
    )

    if not email:
        return False

    return bool (padrao_email.fullmatch(email))


def padronizar_data(data_bruta:str) -> str:
    """Verifica o formato que a data foi lançada e retorna no padrão DD/MM/AAAA

    Args:
        data_bruta (str): Data sem o tratamento

    Returns:
        str: Data no formato DD/MM/AAAA ou none se a data for invalida ou não corresponder a nenhum formato conhecido previsto
    """
    formatos_data_aceito = [
        "%d/%m/%Y",   # 
        "%Y-%m-%d",   
        "%d-%m-%Y",   
    ]

    if not data_bruta:
        return None

    for formato in formatos_data_aceito :
        try:
            data_convertida = datetime.strptime(data_bruta.strip(), formato)
            return data_convertida.strftime("%d/%m/%Y") #String format time
        except ValueError:
            continue

    return None

      



