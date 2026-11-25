import unittest
from decimal import Decimal

from src.api.app import create_app
from src.service.models.product import Product
from src.service.repositories.product_repository import InMemoryProductRepository
from src.service.services.product_service import ProductService


class RegisterProductRouteTest(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def _register(self, codigo=123, preco=59.90):
        return self.client.post("/loja/produto", json={"codigo": codigo, "preco": preco})

    def test_returns_201_with_zero_stock(self):
        response = self._register()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json(), {"codigo": 123, "preco": 59.90, "estoque": 0}
        )

    def test_preco_is_a_number_in_json(self):
        body = self._register().get_json()

        self.assertIsInstance(body["preco"], float)

    def test_duplicate_code_returns_409(self):
        self._register()

        self.assertEqual(self._register().status_code, 409)

    def test_missing_field_returns_400(self):
        response = self.client.post("/loja/produto", json={"codigo": 123})

        self.assertEqual(response.status_code, 400)

    def test_invalid_values_return_400(self):
        invalid_bodies = [
            {"codigo": "abc", "preco": 10.0},
            {"codigo": 2.5, "preco": 10.0},
            {"codigo": True, "preco": 10.0},
            {"codigo": 0, "preco": 10.0},
            {"codigo": 1, "preco": "abc"},
            {"codigo": 1, "preco": True},
            {"codigo": 1, "preco": 0},
            {"codigo": 1, "preco": -5},
        ]
        for body in invalid_bodies:
            with self.subTest(body=body):
                response = self.client.post("/loja/produto", json=body)
                self.assertEqual(response.status_code, 400)

    def test_missing_body_returns_400(self):
        response = self.client.post("/loja/produto")

        self.assertEqual(response.status_code, 400)

    def test_malformed_json_returns_400(self):
        response = self.client.post(
            "/loja/produto", data="{isso nao e json", content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)


class GetStockRouteTest(unittest.TestCase):
    def test_returns_200_with_current_stock(self):
        repository = InMemoryProductRepository()
        repository.add(Product(codigo=123, preco=Decimal("59.90"), estoque=15))
        client = create_app(ProductService(repository)).test_client()

        response = client.get("/loja/produto/123/estoque")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"codigo": 123, "estoque": 15})

    def test_registered_product_has_zero_stock(self):
        client = create_app().test_client()
        client.post("/loja/produto", json={"codigo": 7, "preco": 10.0})

        response = client.get("/loja/produto/7/estoque")

        self.assertEqual(response.get_json(), {"codigo": 7, "estoque": 0})

    def test_unknown_product_returns_404(self):
        client = create_app().test_client()

        self.assertEqual(client.get("/loja/produto/999/estoque").status_code, 404)

    def test_invalid_code_returns_400(self):
        client = create_app().test_client()

        for codigo in ("abc", "2.5", "0"):
            with self.subTest(codigo=codigo):
                response = client.get(f"/loja/produto/{codigo}/estoque")
                self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()