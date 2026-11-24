"""Interface pública da camada de serviço."""

from .exceptions import (
    DomainError,
    InsufficientStockError,
    InvalidDataError,
    ProductAlreadyExistsError,
    ProductNotFoundError,
)
from .models.product import Product
from .models.sale import Sale, SaleItem
from .repositories.product_repository import InMemoryProductRepository
from .services.product_service import ProductService

__all__ = [
    "DomainError",
    "InsufficientStockError",
    "InvalidDataError",
    "ProductAlreadyExistsError",
    "ProductNotFoundError",
    "Product",
    "Sale",
    "SaleItem",
    "InMemoryProductRepository",
    "ProductService",
]
