"""Exceções de domínio da camada de serviço.

Representam violações de regra de negócio e não dependem de HTTP.
A camada de API é quem traduz cada uma para a resposta adequada.
"""


class DomainError(Exception):
    """Base de todos os erros de regra de negócio."""


class InvalidDataError(DomainError):
    """Dado ausente, de tipo inválido ou com valor fora da regra (ex.: quantidade <= 0)."""


class ProductNotFoundError(DomainError):
    """Nenhum produto cadastrado com o código informado."""

    def __init__(self, codigo):
        super().__init__(f"Produto {codigo} não encontrado")
        self.codigo = codigo


class ProductAlreadyExistsError(DomainError):
    """Já existe um produto cadastrado com o código informado."""

    def __init__(self, codigo):
        super().__init__(f"Já existe produto com o código {codigo}")
        self.codigo = codigo


class InsufficientStockError(DomainError):
    """O estoque do produto é menor que a quantidade solicitada."""

    def __init__(self, codigo, disponivel, solicitado):
        super().__init__(
            f"Estoque insuficiente para o produto {codigo}: "
            f"disponível {disponivel}, solicitado {solicitado}"
        )
        self.codigo = codigo
        self.disponivel = disponivel
        self.solicitado = solicitado
