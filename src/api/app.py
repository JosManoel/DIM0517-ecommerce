"""API REST da loja (Flask).

Esta camada só confere o formato do corpo, repassa a chamada para o
ProductService e traduz o resultado (ou a exceção de domínio) para HTTP.
Nenhuma regra de negócio fica aqui: a validação dos valores é do serviço.
"""

from __future__ import annotations

from flask import Flask, jsonify, request

from src.service.exceptions import (
    DomainError,
    InsufficientStockError,
    InvalidDataError,
    ProductAlreadyExistsError,
    ProductNotFoundError,
)
from src.service.services.product_service import ProductService

# Mapeamento único: exceção de domínio -> status HTTP.
ERROR_STATUS = {
    InvalidDataError: 400,
    ProductNotFoundError: 404,
    ProductAlreadyExistsError: 409,
    InsufficientStockError: 400,
}


def _read_json_object() -> dict:
    """Lê o corpo da requisição e garante que é um objeto JSON."""
    data = request.get_json(force=True, silent=True)
    if not isinstance(data, dict):
        raise InvalidDataError("Corpo da requisição ausente ou JSON inválido")
    return data


def _product_to_json(product) -> dict:
    # preco sai como número no JSON (e não como texto).
    return {
        "codigo": product.codigo,
        "preco": float(product.preco),
        "estoque": product.estoque,
    }


def create_app(service: ProductService | None = None) -> Flask:
    """Cria a aplicação Flask, com uma única instância de ProductService."""
    app = Flask(__name__)
    product_service = service if service is not None else ProductService()

    @app.errorhandler(DomainError)
    def handle_domain_error(error: DomainError):
        status = ERROR_STATUS.get(type(error), 400)
        return jsonify({"erro": str(error)}), status

    @app.post("/loja/produto")
    def register_product():
        data = _read_json_object()
        product = product_service.register_product(data.get("codigo"), data.get("preco"))
        return jsonify(_product_to_json(product)), 201

    @app.get("/loja/produto/<codigo>/estoque")
    def get_stock(codigo: str):
        # O código chega como texto e é convertido aqui: com <int:codigo>
        # o Flask responderia 404 em vez de 400 para valores inválidos.
        try:
            codigo_int = int(codigo)
        except ValueError:
            raise InvalidDataError("O código do produto deve ser um número inteiro") from None
        product = product_service.get_stock(codigo_int)
        return jsonify({"codigo": product.codigo, "estoque": product.estoque}), 200

    return app


if __name__ == "__main__":
    create_app().run(debug=True)