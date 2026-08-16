"""Pacote de análise de atendimentos de suporte técnico.

Expõe as funções de leitura e validação como API pública do pacote,
permitindo importação direta via `from src import funcao_x`.
"""

from .leitura import (
    carregar_csv,
    carregar_excel,
    carregar_json,
    carregar_txt,
    verificar_e_criar_diretorios,
)

from .validacao import (
    email_valido,
    padronizar_telefone,
    padronizar_data,
    tempo_atendimento_valido,
    categoria_valida,
    normalizar_status,
    construir_mapa_categorias,
    extrair_contatos_txt,
    nucleo_protocolo,
    validar_registro,
)

from .processamento import(
    quantidade_total_atendimento,
    quantidade_por_categoria,
    quantidade_por_status,
    tempo_medio_atendimento,
    categoria_maior_numero_solicitacoes,
    percentual_registros_invalidos_incompletos,
)


__all__ = [
    # Funções de leitura
    "carregar_csv",
    "carregar_excel",
    "carregar_json",
    "carregar_txt",
    "verificar_e_criar_diretorios",

    # Funções de calculo de indicadores
    "quantidade_total_atendimento",
    "quantidade_por_categoria",
    "quantidade_por_status",
    "tempo_medio_atendimento",
    "categoria_maior_numero_solicitacoes",
    "percentual_registros_invalidos_incompletos",

    # Funções de validação individuais
    "email_valido",
    "padronizar_telefone",
    "padronizar_data",
    "tempo_atendimento_valido",
    "categoria_valida",
    "normalizar_status",

    # Funções auxiliares de estrutura/mapeamento
    "construir_mapa_categorias",
    "extrair_contatos_txt",
    "nucleo_protocolo",

    # Orquestradora
    "validar_registro",
]

__version__ = "1.0.0"
