import unittest
from decimal import Decimal

from src.service import (
    InMemoryProductRepository,
    InvalidDataError,
    Product,
    ProductAlreadyExistsError,
    ProductService,
)


class RegisterProductTest(unittest.TestCase):
    def setUp(self):
        self.repository = InMemoryProductRepository()
        self.service = ProductService(self.repository)

    def test_registers_product_with_zero_stock(self):
        result = self.service.register_product(123, Decimal("59.90"))

        self.assertIsInstance(result, Product)
        self.assertEqual(result.codigo, 123)
        self.assertEqual(result.preco, Decimal("59.90"))
        self.assertEqual(result.estoque, 0)
        self.assertIs(self.repository.get(123), result)

    def test_converts_float_and_int_preco_to_decimal(self):
        from_float = self.service.register_product(1, 59.90)
        from_int = self.service.register_product(2, 100)

        self.assertIsInstance(from_float.preco, Decimal)
        self.assertEqual(from_float.preco, Decimal("59.9"))
        self.assertIsInstance(from_int.preco, Decimal)
        self.assertEqual(from_int.preco, Decimal("100"))

    def test_raises_and_preserves_existing_product_when_codigo_already_exists(self):
        self.service.register_product(123, Decimal("59.90"))
        self.service.add_stock(123, 10)

        with self.assertRaises(ProductAlreadyExistsError) as ctx:
            self.service.register_product(123, Decimal("99.90"))

        self.assertEqual(ctx.exception.codigo, 123)
        existing = self.repository.get(123)
        self.assertEqual(existing.preco, Decimal("59.90"))
        self.assertEqual(existing.estoque, 10)

    def test_raises_when_codigo_is_invalid(self):
        for invalid in (0, -1, "abc", 2.5, None, True, False):
            with self.subTest(codigo=invalid):
                with self.assertRaises(InvalidDataError):
                    self.service.register_product(invalid, Decimal("59.90"))
        self.assertEqual(self.repository.list_all(), [])

    def test_raises_when_preco_is_invalid(self):
        invalid_prices = (
            0,
            -10,
            -0.01,
            Decimal("0"),
            Decimal("-5.00"),
            float("nan"),
            float("inf"),
            float("-inf"),
            Decimal("NaN"),
            Decimal("Infinity"),
            "59.90",
            None,
            True,
            False,
        )
        for invalid in invalid_prices:
            with self.subTest(preco=invalid):
                with self.assertRaises(InvalidDataError):
                    self.service.register_product(123, invalid)
        self.assertEqual(self.repository.list_all(), [])


if __name__ == "__main__":
    unittest.main()
