import unittest
from decimal import Decimal

from src.service.exceptions import InvalidDataError, ProductNotFoundError
from src.service.models.product import Product
from src.service.repositories.product_repository import InMemoryProductRepository
from src.service.services.product_service import ProductService


class GetStockTest(unittest.TestCase):
    def setUp(self):
        self.repository = InMemoryProductRepository()
        self.service = ProductService(self.repository)

    def test_returns_current_stock(self):
        product = Product(codigo=123, preco=Decimal("59.90"))
        product.estoque = 15
        self.repository.add(product)

        result = self.service.get_stock(123)

        self.assertIsInstance(result, Product)
        self.assertEqual(result.codigo, 123)
        self.assertEqual(result.estoque, 15)

    def test_new_product_has_zero_stock(self):
        self.repository.add(Product(codigo=1, preco=Decimal("10.00")))

        result = self.service.get_stock(1)

        self.assertIsInstance(result, Product)
        self.assertEqual(result.estoque, 0)

    def test_raises_when_product_does_not_exist(self):
        with self.assertRaises(ProductNotFoundError):
            self.service.get_stock(999)

    def test_raises_when_codigo_is_not_integer(self):
        for invalid in ("abc", 2.5, None, True):
            with self.subTest(codigo=invalid):
                with self.assertRaises(InvalidDataError):
                    self.service.get_stock(invalid)


if __name__ == "__main__":
    unittest.main()