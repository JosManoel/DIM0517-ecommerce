"""Entidade Produto da camada de serviço."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Product:
    """Produto da loja.

    Tem apenas os atributos exigidos pela especificação: código, preço e estoque.
    Os nomes dos atributos seguem os campos da API (codigo, preco, estoque).
    """

    codigo: int
    preco: Decimal
    estoque: int = 0
