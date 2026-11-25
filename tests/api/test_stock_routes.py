import unittest
from decimal import Decimal

from src.api.app import create_app
from src.service import InMemoryProductRepository, Product, ProductService


class _StockMovementRouteMixin:
    """Casos comuns às rotas PUT /loja/produto/<codigo>/entrada e /saida."""

    endpoint_suffix: str

    def setUp(self):
        self.repository = InMemoryProductRepository()
        self.repository.add(Product(codigo=123, preco=Decimal("59.90"), estoque=15))
        self.client = create_app(ProductService(self.repository)).test_client()

    def _url(self, codigo=123) -> str:
        return f"/loja/produto/{codigo}/{self.endpoint_suffix}"

    def test_unknown_product_returns_404(self):
        response = self.client.put(self._url(999), json={"quantidade": 10})

        self.assertEqual(response.status_code, 404)

    def test_missing_quantidade_returns_400_and_preserves_stock(self):
        response = self.client.put(self._url(123), json={})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.repository.get(123).estoque, 15)

    def test_invalid_quantidade_returns_400_and_preserves_stock(self):
        for invalid in ("abc", 2.5, 0, -5, True, False, None):
            with self.subTest(quantidade=invalid):
                response = self.client.put(self._url(123), json={"quantidade": invalid})
                self.assertEqual(response.status_code, 400)
                self.assertEqual(self.repository.get(123).estoque, 15)

    def test_invalid_codigo_in_url_returns_400_and_preserves_stock(self):
        for codigo in ("abc", "2.5", "0", "-1"):
            with self.subTest(codigo=codigo):
                response = self.client.put(self._url(codigo), json={"quantidade": 10})
                self.assertEqual(response.status_code, 400)
                self.assertEqual(self.repository.get(123).estoque, 15)

    def test_missing_or_malformed_body_returns_400_and_preserves_stock(self):
        missing = self.client.put(self._url(123))
        malformed = self.client.put(
            self._url(123), data="{json invalido", content_type="application/json"
        )

        self.assertEqual(missing.status_code, 400)
        self.assertEqual(malformed.status_code, 400)
        self.assertEqual(self.repository.get(123).estoque, 15)


class AddStockRouteTest(_StockMovementRouteMixin, unittest.TestCase):
    endpoint_suffix = "entrada"

    def test_returns_200_with_updated_stock(self):
        response = self.client.put(self._url(123), json={"quantidade": 10})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"codigo": 123, "estoque": 25})


class RemoveStockRouteTest(_StockMovementRouteMixin, unittest.TestCase):
    endpoint_suffix = "saida"

    def test_returns_200_with_updated_stock(self):
        response = self.client.put(self._url(123), json={"quantidade": 10})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"codigo": 123, "estoque": 5})

    def test_allows_removing_exact_available_stock(self):
        response = self.client.put(self._url(123), json={"quantidade": 15})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"codigo": 123, "estoque": 0})

    def test_insufficient_stock_returns_400_and_preserves_stock(self):
        response = self.client.put(self._url(123), json={"quantidade": 16})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.repository.get(123).estoque, 15)


if __name__ == "__main__":
    unittest.main()
