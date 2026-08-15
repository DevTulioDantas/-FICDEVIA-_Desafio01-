class TransacaoErro(Exception):
    """Base para erros de transações"""

class SaldoInsuficiente(TransacaoErro):
    def __init__(self, saldo_atual, valor_tentado):
        self.saldo_atual = saldo_atual
        self.valor_tentado = valor_tentado
        super().__init__(
            f"Saldo insuficiente: disponivel: {saldo_atual}"
            f"Tentativa de {valor_tentado}"
        )

class ContaInvalidaErro(TransacaoErro):
    def __init__(self, conta: str):
        self.conta = conta
        super().__init__(f"A conta '{conta}' é inválida ou não existe.")

contas_validas = ["1234-5", "6789-0"]

def trasferir(origem, destino, valor, saldo):
    if destino not in contas_validas:
        raise ContaInvalidaErro(destino)

    if valor > saldo:
        raise SaldoInsuficiente(saldo_atual=saldo, valor_tentado=valor)

saldo_cliente = 500
conta_destino = 9999-9
valor_pix = 100

try:
    novo_saldo = trasferir("1234-5, conta_destino, valor_pix, saldo_cliente")
    