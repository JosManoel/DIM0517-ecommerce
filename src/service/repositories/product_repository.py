"""Repositório de produtos em memória."""

from __future__ import annotations

from ..exceptions import ProductAlreadyExistsError, ProductNotFoundError
from ..models.product import Product


class InMemoryProductRepository:
    """Guarda os produtos num dicionário indexado pelo código, sem limite de cadastros."""

    def __init__(self) -> None:
        self._products: dict[int, Product] = {}

    def add(self, product: Product) -> None:
        """Cadastra um produto novo. Falha se o código já existir."""
        if product.codigo in self._products:
            raise ProductAlreadyExistsError(product.codigo)
        self._products[product.codigo] = product

    def exists(self, codigo: int) -> bool:
        return codigo in self._products

    def find(self, codigo: int) -> Product | None:
        """Devolve o produto ou None, sem lançar exceção."""
        return self._products.get(codigo)

    def get(self, codigo: int) -> Product:
        """Devolve o produto ou lança ProductNotFoundError."""
        product = self.find(codigo)
        if product is None:
            raise ProductNotFoundError(codigo)
        return product

    def list_all(self) -> list[Product]:
        return list(self._products.values())
