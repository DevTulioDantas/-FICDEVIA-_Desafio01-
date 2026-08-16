"""Testes unitários para o módulo src.validacao.

Executar com: python -m pytest (a partir da raiz do projeto)
"""
from src.validacao import (
    email_valido,
    padronizar_data,
    padronizar_telefone,
    tempo_atendimento_valido,
    categoria_valida,
    construir_mapa_categorias,
    normalizar_status,
    extrair_contatos_txt,
    nucleo_protocolo,
    validar_registro,
)

# Mapa reduzido independente do categorias.json 
CATEGORIAS = construir_mapa_categorias({
    "Acesso ao AVA": ["ava", "ambiente virtual"],
    "Instalação de programas": ["instalacao", "software"],
})

TEXTO_TXT = (
    "O protocolo SUP-2026-0100 solicitou retorno pelo telefone (65) 98888-1111.\n"
    "O aluno do protocolo 2026-0200 informou o telefone 65 3333-2222.\n"
)


def test_email_valido():
    assert email_valido("maria@example.com") is True
    assert email_valido("email-sem-arroba") is False
    assert email_valido("usuario@dominio") is False
    assert email_valido("") is False
    assert email_valido(None) is False


def test_padronizar_data():
    assert padronizar_data("10/05/2026") == "10/05/2026"
    assert padronizar_data("2026-05-10") == "10/05/2026"
    assert padronizar_data("2026/05/10") == "10/05/2026"
    assert padronizar_data("10-05-2026") == "10/05/2026"
    assert padronizar_data("31/04/2026") is None 
    assert padronizar_data("") is None
    assert padronizar_data(None) is None


def test_padronizar_telefone():
    assert padronizar_telefone("(65) 98888-1111") is True
    assert padronizar_telefone("65 3333-2222") is True
    assert padronizar_telefone("123") is False
    assert padronizar_telefone("") is False
    assert padronizar_telefone(None) is False


def test_tempo_atendimento_valido():
    assert tempo_atendimento_valido(50) is True
    assert tempo_atendimento_valido(600) is True
    assert tempo_atendimento_valido("-10") is False
    assert tempo_atendimento_valido("abc") is False
    assert tempo_atendimento_valido("999") is False
    assert tempo_atendimento_valido("") is False
    assert tempo_atendimento_valido(None) is False


def test_categoria_valida():
    assert categoria_valida("software", CATEGORIAS) == "Instalação de programas"
    assert categoria_valida("  Ambiente Virtual  ", CATEGORIAS) == "Acesso ao AVA"
    assert categoria_valida("categoria desconhecida", CATEGORIAS) is None
    assert categoria_valida("", CATEGORIAS) is None
    assert categoria_valida(None, CATEGORIAS) is None


def test_normalizar_status():
    assert normalizar_status("aberto") == "aberto"
    assert normalizar_status("RESOLVIDO") == "resolvido"
    assert normalizar_status("cancelado") is None
    assert normalizar_status("") is None
    assert normalizar_status(None) is None


def test_extrair_contatos_e_nucleo_protocolo():
    contatos = extrair_contatos_txt(TEXTO_TXT)
    assert contatos["2026-0100"] == "(65) 98888-1111"
    assert contatos["2026-0200"] == "65 3333-2222"  

    assert nucleo_protocolo("SUP-2026-0100") == "2026-0100"
    assert nucleo_protocolo("PROTOCOLO-X") is None

    # Integração: núcleo do protocolo bate com a chave gerada no TXT
    assert contatos.get(nucleo_protocolo("SUP-2026-0100")) == "(65) 98888-1111"


def test_validar_registro():
    registro_valido = {
        "protocolo": "SUP-2026-0001", "email": "aluno@example.com",
        "data": "10/05/2026", "categoria": "Ambiente Virtual",
        "tempo_minutos": "50", "status": "aberto",
    }
    assert validar_registro(registro_valido, 2, CATEGORIAS) == []

    registro_invalido = {
        "protocolo": "", "email": "invalido", "data": "31/04/2026",
        "categoria": "categoria desconhecida", "tempo_minutos": "-10",
        "status": "aberto",
    }
    erros = validar_registro(registro_invalido, 99, CATEGORIAS)
    assert len(erros) == 5