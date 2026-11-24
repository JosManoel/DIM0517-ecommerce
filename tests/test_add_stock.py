import unittest
from decimal import Decimal

from src.service.exceptions import InvalidDataError, ProductNotFoundError
from src.service.models.product import Product
from src.service.repositories.product_repository import InMemoryProductRepository
from src.service.services.product_service import ProductService


class AddStockTest(unittest.TestCase):
    def setUp(self):
        self.repository = InMemoryProductRepository()
        self.service = ProductService(self.repository)

    def test_adds_quantity_to_existing_stock(self):
        product = Product(codigo=123, preco=Decimal("59.90"), estoque=15)
        self.repository.add(product)

        result = self.service.add_stock(123, 10)

        self.assertIsInstance(result, Product)
        self.assertEqual(result.codigo, 123)
        self.assertEqual(result.estoque, 25)

    def test_adds_quantity_to_zero_stock(self):
        self.service.register_product(1, Decimal("10.00"))

        result = self.service.add_stock(1, 5)

        self.assertEqual(result.estoque, 5)

    def test_raises_when_product_does_not_exist(self):
        with self.assertRaises(ProductNotFoundError):
            self.service.add_stock(999, 10)

    def test_raises_and_preserves_stock_when_quantidade_is_invalid(self):
        self.repository.add(Product(codigo=123, preco=Decimal("59.90"), estoque=15))

        for invalid in (0, -5, "abc", 2.5, None, True, False):
            with self.subTest(quantidade=invalid):
                with self.assertRaises(InvalidDataError):
                    self.service.add_stock(123, invalid)
                self.assertEqual(self.repository.get(123).estoque, 15)

    def test_raises_when_codigo_is_invalid(self):
        for invalid in (0, -1, "abc", 2.5, None, True, False):
            with self.subTest(codigo=invalid):
                with self.assertRaises(InvalidDataError):
                    self.service.add_stock(invalid, 10)


if __name__ == "__main__":
    unittest.main()
