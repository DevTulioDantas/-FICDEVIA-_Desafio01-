import re

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




