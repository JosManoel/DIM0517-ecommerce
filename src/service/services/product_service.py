"""Serviço de produtos: casos de uso da camada de negócio."""

from __future__ import annotations

from ..exceptions import InvalidDataError, ProductNotFoundError
from ..repositories.product_repository import InMemoryProductRepository


class ProductService:
    """Casos de uso relacionados a produtos e estoque."""

    def __init__(self, repository: InMemoryProductRepository) -> None:
        self._repository = repository

    def get_stock(self, codigo: int) -> dict:
        """Consulta o estoque atual de um produto.

        Retorna {"codigo": <int>, "estoque": <int>}.
        Lança InvalidDataError se o código não for um inteiro.
        Lança ProductNotFoundError se o produto não existir.
        """
        if isinstance(codigo, bool) or not isinstance(codigo, int):
            raise InvalidDataError("O código do produto deve ser um número inteiro")

        product = self._repository.find(codigo)
        if product is None:
            raise ProductNotFoundError(codigo)

        return {"codigo": product.codigo, "estoque": product.estoque}