import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)



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
    "%d/%m/%Y",   
    "%Y-%m-%d",   
    "%d-%m-%Y",   
    "%Y/%m/%d",   
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

def padronizar_telefone(telefone_bruto: str) -> str:
    """Verifica o formato do telefone

    Args:
        telefone_bruto (str): Telefone a ser validado

    Returns:
        str: True se for um numero de telefone válido, falso se for vazio ou fora do padrão esperado
    """
    padrao_telefone = re.compile(
    r"\(?\d{2}\)?[\s.-]?9?[\s.-]?\d{4}[\s.-]?\d{4}"
    )
    if not telefone_bruto:
        return False

    return bool(padrao_telefone.fullmatch(telefone_bruto.strip()))

def construir_mapa_categorias(categorias_json: dict) -> dict:
    """Inverte o mapa de categorias, Transforma {categoria_padrao: [aliases]} em {alias: categoria_padrao}
    

    Args:
        categorias_json: Dicionário no formato original do categorias.json
            
    Returns:
        Dicionário invertido
    """
    mapa_invertido = {}
    for categoria_padrao, aliases in categorias_json.items():
        for alias in aliases:
            mapa_invertido[alias.strip().lower()] = categoria_padrao        
        mapa_invertido[categoria_padrao.strip().lower()] = categoria_padrao
    return mapa_invertido


def categoria_valida(categoria: str, mapa_categorias: dict) -> str | None:
    """Normaliza uma categoria o mapa já invertido

    Args:
        categoria: Texto bruto da categoria, como veio do CSV
        mapa_categorias: Mapa após construir_mapa_categorias()            

    Returns:
        A categoria padronizada, se reconhecida. None se a categoria
        estiver ausente ou não for reconhecida 
    """
    if not categoria:
        return None

    chave = categoria.strip().lower()
    return mapa_categorias.get(chave)

def tempo_atendimento_valido(tempo: float | str) -> bool:
    """Verifica se o tempo de atendimento é um número positivo dentro de um intervalo

    Args:
        tempo: Tempo de atendimento em minutos.

    Returns:
        True se o tempo for um número entre 0 (exclusivo) e 600
        minutos, False caso contrário ou valores ausentes ou não numéricos.
    """
    if tempo is None or tempo == '':
        return False

    try:
        valor = float(tempo)
    except (ValueError, TypeError):
        return False

    return 0 < valor <= 600

def normalizar_status(status: str) -> str | None:
    """Padroniza o texto de status 
    Args:
        status: Texto bruto do status, como veio do CSV

    Returns:
        Status normalizado (minúsculo) se reconhecido em status_validos
        ou None se ausente ou não reconhecido.
    """
    status_validos = {"aberto", "em andamento", "resolvido"}
    if not status:
        return None

    status_normalizado = status.strip().lower()
    return status_normalizado if status_normalizado in status_validos else None


padrao_protocolotxt = re.compile(r"(?:SUP-)?(\d{4}-\d{4})")

def extrair_contatos_txt(texto: str) -> dict[str, str]:
    """Extrai a associação protocolo 

    Args:
        texto: Conteúdo bruto do observacoes.txt.

    Returns:
        Dicionário {núcleo_do_protocolo: telefone}
    """
    
    padrao_telefone = re.compile(r"\(?\d{2}\)?[\s.-]?9?[\s.-]?\d{4}[\s.-]?\d{4}")
    contatos = {}

    for linha in texto.splitlines():
        protocolo_encontrado = padrao_protocolotxt.search(linha)
        telefone_encontrado = padrao_telefone.search(linha)

        if protocolo_encontrado and telefone_encontrado:
            nucleo = protocolo_encontrado.group(1)  # ex: "2026-0042"
            contatos[nucleo] = telefone_encontrado.group()

    return contatos

def nucleo_protocolo(protocolo: str) -> str | None:
    """Extrai o núcleo AAAA-NNNN de um protocolo

    Args:
        protocolo: Protocolo completo, como veio do CSV           

    Returns:
        Núcleo no formato AAAA-NNNN ou None se o protocolo não
        seguir esse padrão
    """
    if not protocolo:
        return None
    encontrado = padrao_protocolotxt.search(protocolo)
    return encontrado.group(1) if encontrado else None

#Para testes
#categorias_json = {
# "Acesso ao AVA": ["ava", "acesso ava", "ambiente virtual", "acesso ao ambiente virtual"],
#"Instalação de programas": ["instalacao", "instalação", "instalar programa", "software"],}
#mapa = construir_mapa_categorias(categorias_json)
#mapa["ambiente virtual"]  
#mapa["software"]           
#mapa["config python"]      
#mapa.get("categoria inexistente")  

def validar_registro(registro: dict, num_linha: int, mapa_categorias: dict) -> list[str]:
    """

    Args:
        registro: Dicionário com os dados de uma linha do CSV            
        num_linha: Número da linha no arquivo de origem
        mapa_categorias: Mapa invertido de categorias

    Returns:
        Lista de strings descrevendo os erros encontrados
        Lista vazia se o registro for válido
    """
    erros = []

    if not registro.get('protocolo'):
        erros.append('Campo obrigatório ausente: protocolo')

    if not email_valido(registro.get('email')):
        erros.append(f"E-mail inválido: {registro.get('email')}")

    if padronizar_data(registro.get('data')) is None:
        erros.append(f"Data inválida: {registro.get('data')}")

    if not tempo_atendimento_valido(registro.get('tempo_minutos')):
        erros.append(f"Tempo de atendimento inválido: {registro.get('tempo_minutos')}")

    if categoria_valida(registro.get('categoria'), mapa_categorias) is None:
        erros.append(f"Categoria não reconhecida: {registro.get('categoria')}")

    if erros:
        logger.warning(f"Linha {num_linha}: {len(erros)} erro(s) — {erros}")
    else:
        logger.debug(f"Linha {num_linha}: registro válido")

    return erros
