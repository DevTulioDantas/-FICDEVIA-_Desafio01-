from pathlib import Path
import pandas as pd
from src import *

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
CONFIG = DATA / "config.json"


def main():
  # 1. Carrega as configurações do config.json
  config = carregar_json(CONFIG)

  ATENDIMENTO_FILE = RAIZ / config["arquivo_atendimentos"]
  CATEGORIA_FILE = RAIZ / config["arquivo_categorias"]
  OBSERVACAO_FILE = RAIZ / config["arquivo_observacoes"]
  SAIDA = RAIZ / config["diretorio_saida"]
  SEPARADOR = config.get("separador_csv", ",")

  # 2. Carrega os arquivos
  df_atendimentos = carregar_csv(ATENDIMENTO_FILE, SEPARADOR)
  dict_categorias = carregar_json(CATEGORIA_FILE)
  txt_observacoes = carregar_txt(OBSERVACAO_FILE)

  # 3. Prepara o mapa de categorias
  mapa_categorias = construir_mapa_categorias(dict_categorias)

  # 4. Converte o DataFrame/lista para registros dict para validação
  if isinstance(df_atendimentos, pd.DataFrame):
    registros = df_atendimentos.to_dict(orient="records")
  else:
    registros = df_atendimentos

  registros_validos = []
  registros_com_erros = []

  # 5. Valida linha por linha
  for num_linha, registro in enumerate(registros, start=2):
    erros = validar_registro(
        registro=registro,
        num_linha=num_linha,
        mapa_categorias=mapa_categorias,
    )

    if not erros:
      registros_validos.append(registro)
    else:
      item_erro = registro.copy()
      item_erro["linha_csv"] = num_linha
      item_erro["erros"] = " | ".join(erros)
      registros_com_erros.append(item_erro)

  # 6. Converte os resultados para DataFrames
  df_validos = pd.DataFrame(registros_validos)
  df_erros = pd.DataFrame(registros_com_erros)

  # Garante que a pasta de saída existe e salva se necessário
  verificar_e_criar_diretorios()

  df_validos.info()
  df_erros.info()
  print(df_validos)
  
  



if __name__ == "__main__":
  main()

