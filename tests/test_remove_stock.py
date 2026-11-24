import unittest
from decimal import Decimal

from src.service.exceptions import (
    InsufficientStockError,
    InvalidDataError,
    ProductNotFoundError,
)
from src.service.models.product import Product
from src.service.repositories.product_repository import InMemoryProductRepository
from src.service.services.product_service import ProductService


class RemoveStockTest(unittest.TestCase):
    def setUp(self):
        self.repository = InMemoryProductRepository()
        self.service = ProductService(self.repository)

    def test_removes_quantity_from_existing_stock(self):
        self.repository.add(Product(codigo=123, preco=Decimal("59.90"), estoque=15))

        result = self.service.remove_stock(123, 10)

        self.assertIsInstance(result, Product)
        self.assertEqual(result.codigo, 123)
        self.assertEqual(result.estoque, 5)

    def test_allows_removing_exact_available_stock(self):
        self.repository.add(Product(codigo=1, preco=Decimal("10.00"), estoque=10))

        result = self.service.remove_stock(1, 10)

        self.assertEqual(result.estoque, 0)

    def test_raises_and_preserves_stock_when_stock_is_insufficient(self):
        self.repository.add(Product(codigo=123, preco=Decimal("59.90"), estoque=5))

        with self.assertRaises(InsufficientStockError) as ctx:
            self.service.remove_stock(123, 10)

        self.assertEqual(ctx.exception.codigo, 123)
        self.assertEqual(ctx.exception.disponivel, 5)
        self.assertEqual(ctx.exception.solicitado, 10)
        self.assertEqual(self.repository.get(123).estoque, 5)

    def test_raises_when_product_does_not_exist(self):
        with self.assertRaises(ProductNotFoundError):
            self.service.remove_stock(999, 10)

    def test_raises_and_preserves_stock_when_quantidade_is_invalid(self):
        self.repository.add(Product(codigo=123, preco=Decimal("59.90"), estoque=15))

        for invalid in (0, -5, "abc", 2.5, None, True, False):
            with self.subTest(quantidade=invalid):
                with self.assertRaises(InvalidDataError):
                    self.service.remove_stock(123, invalid)
                self.assertEqual(self.repository.get(123).estoque, 15)

    def test_raises_when_codigo_is_invalid(self):
        for invalid in (0, -1, "abc", 2.5, None, True, False):
            with self.subTest(codigo=invalid):
                with self.assertRaises(InvalidDataError):
                    self.service.remove_stock(invalid, 10)


if __name__ == "__main__":
    unittest.main()
