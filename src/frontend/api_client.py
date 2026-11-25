"""Cliente HTTP da API REST da loja."""

from __future__ import annotations

from urllib.parse import quote

import requests

DEFAULT_URL = "http://127.0.0.1:5000"


class ApiError(Exception):
    """A API respondeu com erro ou não pôde ser acessada."""


class ApiClient:
    """Chama as rotas da API e devolve o corpo da resposta como dicionário."""

    def __init__(self, base_url: str = DEFAULT_URL, timeout: float = 5) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def register_product(self, codigo, preco) -> dict:
        return self._request("POST", "/loja/produto", {"codigo": codigo, "preco": preco})

    def get_stock(self, codigo) -> dict:
        return self._request("GET", f"{self._product_path(codigo)}/estoque")

    def add_stock(self, codigo, quantidade) -> dict:
        return self._request("PUT", f"{self._product_path(codigo)}/entrada", {"quantidade": quantidade})

    def remove_stock(self, codigo, quantidade) -> dict:
        return self._request("PUT", f"{self._product_path(codigo)}/saida", {"quantidade": quantidade})

    def _product_path(self, codigo) -> str:
        return f"/loja/produto/{quote(str(codigo), safe='')}"

    def _request(self, method: str, path: str, body: dict | None = None) -> dict:
        try:
            response = requests.request(method, self._base_url + path, json=body, timeout=self._timeout)
        except requests.RequestException as error:
            raise ApiError(f"Não foi possível acessar a API em {self._base_url}.") from error

        try:
            data = response.json()
        except ValueError:
            data = None

        if response.ok and isinstance(data, dict):
            return data
        message = data.get("erro") if isinstance(data, dict) else None
        raise ApiError(f"Erro {response.status_code}: {message or 'resposta inesperada da API'}")
