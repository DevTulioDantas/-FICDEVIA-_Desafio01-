
#leitura.py
from .leitura import (
    carregar_csv,
    carregar_excel,
    carregar_json,
    carregar_txt,
    verificar_e_criar_diretorios,
)

from .validacao import (
    email_valido,
    padronizar_data,
    padronizar_telefone,
)


# Para importar como " from src import * "
__all__ = [
    # Funções de leitura
    "carregar_csv",
    "carregar_excel",
    "carregar_json",
    "carregar_txt",
    "verificar_e_criar_diretorios",
    
    #Funções de validação
    "email_valido",
    "padronizar_data",
    "padronizar_telefone",

]

__version__= "1.0.0"
