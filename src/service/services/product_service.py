"""Operações de negócio sobre produtos."""

from __future__ import annotations

from ..models.product import Product
from ..repositories.product_repository import InMemoryProductRepository
from ..validators import validate_codigo, validate_preco


class ProductService:
    """Ponto de entrada da camada de serviço para as operações com produtos.

    Não depende da API: pode ser chamado direto, por exemplo em testes.
    """

    def __init__(self, repository: InMemoryProductRepository | None = None) -> None:
        self._repository = repository if repository is not None else InMemoryProductRepository()

    def register_product(self, codigo, preco) -> Product:
        """Cadastrar Produto: registra um produto novo com estoque 0.

        Lança InvalidDataError se o código ou o preço forem inválidos e
        ProductAlreadyExistsError se o código já estiver cadastrado.
        Nos dois casos, nada é alterado.
        """
        codigo = validate_codigo(codigo)
        preco = validate_preco(preco)
        product = Product(codigo=codigo, preco=preco, estoque=0)
        self._repository.add(product)
        return product
