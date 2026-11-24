"""Validação dos dados de entrada da camada de serviço.

Fica num módulo próprio porque todas as operações validam os mesmos dados
(código, preço, quantidade e itens de venda).
"""

from decimal import Decimal

from .exceptions import InvalidDataError


def _validate_positive_int(value, invalid_prefix: str, non_positive_subject: str) -> int:
    """Aceita só inteiro maior que zero. bool é rejeitado (em Python, True é um int)."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise InvalidDataError(f"{invalid_prefix}: {value!r}. Informe um número inteiro.")
    if value <= 0:
        raise InvalidDataError(f"{invalid_prefix}: {value}. {non_positive_subject} deve ser maior que zero.")
    return value


def validate_codigo(codigo) -> int:
    """Aceita só inteiro maior que zero. bool é rejeitado (em Python, True é um int)."""
    return _validate_positive_int(codigo, "Código inválido", "O código")


def validate_quantidade(quantidade) -> int:
    """Aceita só inteiro maior que zero. bool é rejeitado (em Python, True é um int)."""
    return _validate_positive_int(quantidade, "Quantidade inválida", "A quantidade")


def validate_preco(preco) -> Decimal:
    """Aceita int, float ou Decimal maior que zero e devolve como Decimal.

    O float passa por str() para 59.90 virar Decimal('59.9') em vez de Decimal ('59.988~').
    """
    if isinstance(preco, bool) or not isinstance(preco, (int, float, Decimal)):
        raise InvalidDataError(f"Preço inválido: {preco!r}. Informe um número.")
    valor = Decimal(str(preco))
    if not valor.is_finite() or valor <= 0:
        raise InvalidDataError(f"Preço inválido: {preco}. O preço deve ser maior que zero.")
    return valor


def validate_itens(itens) -> list[tuple[int, int]]:
    """Aceita só lista não vazia de dicionários com codigo e quantidade.

    Devolve os pares (codigo, quantidade) na mesma ordem.
    """
    if not isinstance(itens, list) or not itens:
        raise InvalidDataError("Itens inválidos. Informe uma lista com pelo menos um item.")
    pares = []
    for item in itens:
        if not isinstance(item, dict):
            raise InvalidDataError(f"Item inválido: {item!r}. Informe codigo e quantidade.")
        pares.append((validate_codigo(item.get("codigo")), validate_quantidade(item.get("quantidade"))))
    return pares
