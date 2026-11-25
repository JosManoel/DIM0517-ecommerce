"""Resultado de uma venda da camada de serviço."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class SaleItem:
    """Item vendido. O estoque é o do produto depois da venda inteira."""

    codigo: int
    quantidade: int
    subtotal: Decimal
    estoque: int


@dataclass(frozen=True)
class Sale:
    """Venda realizada: o valor total e os itens, na ordem em que foram pedidos."""

    total: Decimal
    itens: tuple[SaleItem, ...]
