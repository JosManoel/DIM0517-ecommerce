import unittest
from decimal import Decimal

from src.service import (
    InMemoryProductRepository,
    InsufficientStockError,
    InvalidDataError,
    Product,
    ProductNotFoundError,
    ProductService,
    Sale,
)


class RegisterSaleTest(unittest.TestCase):
    def setUp(self):
        self.repository = InMemoryProductRepository()
        self.service = ProductService(self.repository)
        self.repository.add(Product(codigo=123, preco=Decimal("59.90"), estoque=15))
        self.repository.add(Product(codigo=456, preco=Decimal("69.90"), estoque=8))

    def assert_stock_unchanged(self):
        self.assertEqual(self.repository.get(123).estoque, 15)
        self.assertEqual(self.repository.get(456).estoque, 8)

    def test_sells_items_and_returns_total_and_details(self):
        sale = self.service.register_sale(
            [{"codigo": 123, "quantidade": 2}, {"codigo": 456, "quantidade": 1}]
        )

        self.assertIsInstance(sale, Sale)
        self.assertEqual(sale.total, Decimal("189.70"))
        self.assertEqual(
            [(i.codigo, i.quantidade, i.subtotal, i.estoque) for i in sale.itens],
            [(123, 2, Decimal("119.80"), 13), (456, 1, Decimal("69.90"), 7)],
        )
        self.assertEqual(self.repository.get(123).estoque, 13)
        self.assertEqual(self.repository.get(456).estoque, 7)

    def test_allows_selling_exact_available_stock(self):
        sale = self.service.register_sale([{"codigo": 456, "quantidade": 8}])

        self.assertEqual(sale.itens[0].estoque, 0)
        self.assertEqual(self.repository.get(456).estoque, 0)

    def test_accepts_repeated_codigo_and_reports_final_stock(self):
        sale = self.service.register_sale(
            [{"codigo": 123, "quantidade": 10}, {"codigo": 123, "quantidade": 5}]
        )

        self.assertEqual([i.quantidade for i in sale.itens], [10, 5])
        self.assertEqual([i.estoque for i in sale.itens], [0, 0])
        self.assertEqual(sale.total, Decimal("898.50"))
        self.assertEqual(self.repository.get(123).estoque, 0)

    def test_sums_repeated_codigo_when_checking_stock(self):
        with self.assertRaises(InsufficientStockError) as ctx:
            self.service.register_sale(
                [{"codigo": 123, "quantidade": 10}, {"codigo": 123, "quantidade": 6}]
            )

        self.assertEqual(ctx.exception.disponivel, 15)
        self.assertEqual(ctx.exception.solicitado, 16)
        self.assert_stock_unchanged()

    def test_preserves_all_stock_when_one_item_has_insufficient_stock(self):
        with self.assertRaises(InsufficientStockError) as ctx:
            self.service.register_sale(
                [{"codigo": 123, "quantidade": 2}, {"codigo": 456, "quantidade": 9}]
            )

        self.assertEqual(ctx.exception.codigo, 456)
        self.assert_stock_unchanged()

    def test_preserves_all_stock_when_one_product_does_not_exist(self):
        with self.assertRaises(ProductNotFoundError):
            self.service.register_sale(
                [{"codigo": 123, "quantidade": 2}, {"codigo": 999, "quantidade": 1}]
            )

        self.assert_stock_unchanged()

    def test_invalid_data_takes_priority_over_missing_product(self):
        with self.assertRaises(InvalidDataError):
            self.service.register_sale(
                [{"codigo": 999, "quantidade": 1}, {"codigo": 123, "quantidade": "abc"}]
            )

        self.assert_stock_unchanged()

    def test_raises_when_list_is_missing_empty_or_not_a_list(self):
        for invalid in (None, [], {}, "abc", 1, {"codigo": 123, "quantidade": 1}):
            with self.subTest(itens=invalid):
                with self.assertRaises(InvalidDataError):
                    self.service.register_sale(invalid)

    def test_raises_and_preserves_stock_when_an_item_is_invalid(self):
        invalid_items = [None, "abc", 1, [], {}, {"codigo": 456}, {"quantidade": 1}]
        invalid_items += [{"codigo": 456, "quantidade": q} for q in (0, -5, "abc", 2.5, None, True)]
        invalid_items += [{"codigo": c, "quantidade": 1} for c in (0, -1, "abc", 2.5, None, True)]

        for invalid in invalid_items:
            with self.subTest(item=invalid):
                with self.assertRaises(InvalidDataError):
                    self.service.register_sale([{"codigo": 123, "quantidade": 1}, invalid])
                self.assert_stock_unchanged()


if __name__ == "__main__":
    unittest.main()
