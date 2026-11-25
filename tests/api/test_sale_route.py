import unittest
from decimal import Decimal

from src.api.app import create_app
from src.service.models.product import Product
from src.service.repositories.product_repository import InMemoryProductRepository
from src.service.services.product_service import ProductService


class SaleRouteTest(unittest.TestCase):
    """Prepara 123 (preço 59.90, estoque 15) e 456 (preço 69.90, estoque 8)."""

    def setUp(self):
        self.repository = InMemoryProductRepository()
        self.repository.add(Product(codigo=123, preco=Decimal("59.90"), estoque=15))
        self.repository.add(Product(codigo=456, preco=Decimal("69.90"), estoque=8))
        self.client = create_app(ProductService(self.repository)).test_client()

    def stocks(self):
        return (self.repository.get(123).estoque, self.repository.get(456).estoque)

    def sell(self, itens):
        return self.client.post("/loja/venda", json={"itens": itens})

    def test_example_from_spec_returns_201(self):
        response = self.sell(
            [{"codigo": 123, "quantidade": 2}, {"codigo": 456, "quantidade": 1}]
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json(),
            {
                "total": 189.70,
                "itens": [
                    {"codigo": 123, "quantidade": 2, "subtotal": 119.80, "estoque": 13},
                    {"codigo": 456, "quantidade": 1, "subtotal": 69.90, "estoque": 7},
                ],
            },
        )

    def test_total_and_subtotal_are_numbers_in_json(self):
        body = self.sell([{"codigo": 123, "quantidade": 2}]).get_json()

        self.assertIsInstance(body["total"], float)
        self.assertIsInstance(body["itens"][0]["subtotal"], float)

    def test_sale_updates_stock(self):
        self.sell([{"codigo": 123, "quantidade": 2}, {"codigo": 456, "quantidade": 1}])

        self.assertEqual(self.stocks(), (13, 7))

    def test_invalid_list_or_item_returns_400_and_keeps_stock(self):
        invalid_bodies = [
            {},
            {"itens": []},
            {"itens": "abc"},
            {"itens": [123]},
            {"itens": [{"codigo": 123}]},
            {"itens": [{"quantidade": 1}]},
            {"itens": [{"codigo": "abc", "quantidade": 1}]},
            {"itens": [{"codigo": 123, "quantidade": 2.5}]},
            {"itens": [{"codigo": 123, "quantidade": 0}]},
        ]
        for body in invalid_bodies:
            with self.subTest(body=body):
                response = self.client.post("/loja/venda", json=body)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(self.stocks(), (15, 8))

    def test_missing_body_returns_400(self):
        response = self.client.post("/loja/venda")

        self.assertEqual(response.status_code, 400)

    def test_unknown_product_returns_404_and_keeps_stock(self):
        response = self.sell(
            [{"codigo": 123, "quantidade": 2}, {"codigo": 999, "quantidade": 1}]
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.stocks(), (15, 8))

    def test_insufficient_stock_returns_400_and_keeps_stock(self):
        response = self.sell(
            [{"codigo": 123, "quantidade": 2}, {"codigo": 456, "quantidade": 9}]
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.stocks(), (15, 8))


if __name__ == "__main__":
    unittest.main()