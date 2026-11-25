from __future__ import annotations

from decimal import Decimal

from ..exceptions import InsufficientStockError
from ..models.product import Product
from ..models.sale import Sale, SaleItem
from ..repositories.product_repository import InMemoryProductRepository
from ..validators import validate_codigo, validate_itens, validate_preco, validate_quantidade


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

    def get_stock(self, codigo) -> Product:
        """Consultar Estoque: retorna o produto com o estoque atual.

        Lança InvalidDataError se o código for inválido e
        ProductNotFoundError se o produto não estiver cadastrado.
        """
        codigo = validate_codigo(codigo)
        return self._repository.get(codigo)

    def add_stock(self, codigo, quantidade) -> Product:
        """Entrada de Estoque: acrescenta uma quantidade ao estoque do produto.

        Lança InvalidDataError se o código ou a quantidade forem inválidos e
        ProductNotFoundError se o produto não estiver cadastrado.
        Nos dois casos, nada é alterado.
        """
        codigo = validate_codigo(codigo)
        quantidade = validate_quantidade(quantidade)
        product = self._repository.get(codigo)
        product.estoque += quantidade
        return product

    def remove_stock(self, codigo, quantidade) -> Product:
        """Saída de Estoque: subtrai uma quantidade do estoque do produto.

        Lança InvalidDataError se o código ou a quantidade forem inválidos,
        ProductNotFoundError se o produto não estiver cadastrado e
        InsufficientStockError se o estoque disponível for menor que a quantidade.
        Em qualquer caso de erro, nada é alterado.
        """
        codigo = validate_codigo(codigo)
        quantidade = validate_quantidade(quantidade)
        product = self._repository.get(codigo)
        if product.estoque < quantidade:
            raise InsufficientStockError(product.codigo, product.estoque, quantidade)
        product.estoque -= quantidade
        return product

    def register_sale(self, itens) -> Sale:
        """Venda: baixa o estoque de todos os itens e calcula o total, de forma atômica.

        Recebe uma lista de dicionários com codigo e quantidade. Códigos repetidos
        são aceitos, e o saldo é conferido pela soma das quantidades.

        Lança InvalidDataError se a lista ou algum item for inválido,
        ProductNotFoundError se algum produto não estiver cadastrado e
        InsufficientStockError se faltar estoque para algum produto.
        Em qualquer caso de erro, nada é alterado.
        """
        pares = validate_itens(itens)

        solicitado: dict[int, int] = {}
        for codigo, quantidade in pares:
            solicitado[codigo] = solicitado.get(codigo, 0) + quantidade

        products = {codigo: self._repository.get(codigo) for codigo in solicitado}
        for codigo, quantidade in solicitado.items():
            if products[codigo].estoque < quantidade:
                raise InsufficientStockError(codigo, products[codigo].estoque, quantidade)

        # O resultado é montado antes da baixa: daqui em diante nada pode falhar.
        sale_items = tuple(
            SaleItem(
                codigo=codigo,
                quantidade=quantidade,
                subtotal=products[codigo].preco * quantidade,
                estoque=products[codigo].estoque - solicitado[codigo],
            )
            for codigo, quantidade in pares
        )
        sale = Sale(total=sum((item.subtotal for item in sale_items), Decimal("0")), itens=sale_items)

        for codigo, quantidade in solicitado.items():
            products[codigo].estoque -= quantidade
        return sale
