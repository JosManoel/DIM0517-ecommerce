"""Front-end console da loja.

Só lê os dados, chama a API REST e mostra o resultado. Quem valida os valores é a API.
O endereço da API pode ser trocado pela variável de ambiente LOJA_API_URL.
"""

from __future__ import annotations

import os
import re

from .api_client import DEFAULT_URL, ApiClient, ApiError


def read_text(label: str) -> str:
    """Pergunta até receber algum texto."""
    while True:
        text = input(f"{label}: ").strip()
        if text:
            return text
        print("Informe um valor.")


def read_number(label: str) -> int | float | str:
    """Lê um número (aceita vírgula). O que não for número segue como texto, e a API responde 400."""
    text = read_text(label)
    try:
        if re.fullmatch(r"-?[0-9]+", text):
            return int(text)
        if re.fullmatch(r"-?[0-9]+[.,][0-9]+", text):
            return float(text.replace(",", "."))
    except ValueError:
        pass
    return text


def register_product(client: ApiClient) -> None:
    data = client.register_product(read_number("Código"), read_number("Preço"))
    print(f"Produto {data['codigo']} cadastrado. Preço: R$ {data['preco']:.2f}. Estoque: {data['estoque']}.")


def get_stock(client: ApiClient) -> None:
    show_stock(client.get_stock(read_text("Código")))


def add_stock(client: ApiClient) -> None:
    show_stock(client.add_stock(read_text("Código"), read_number("Quantidade")))


def remove_stock(client: ApiClient) -> None:
    show_stock(client.remove_stock(read_text("Código"), read_number("Quantidade")))


def show_stock(data: dict) -> None:
    print(f"Produto {data['codigo']}. Estoque: {data['estoque']}.")


OPTIONS = {
    "1": ("Cadastrar Produto", register_product),
    "2": ("Consultar Estoque", get_stock),
    "3": ("Entrada de Estoque", add_stock),
    "4": ("Saída de Estoque", remove_stock),
}


def show_menu() -> None:
    print("\n=== Loja ===")
    for key, (title, _) in OPTIONS.items():
        print(f"{key} - {title}")
    print("0 - Sair")


def run(client: ApiClient) -> None:
    """Mostra o menu até o usuário sair. Erros da API não encerram o programa."""
    while True:
        show_menu()
        choice = input("Opção: ").strip()
        if choice == "0":
            return
        if choice not in OPTIONS:
            print("Opção inválida.")
            continue
        _, action = OPTIONS[choice]
        try:
            action(client)
        except ApiError as error:
            print(error)


def main() -> None:
    try:
        run(ApiClient(os.environ.get("LOJA_API_URL", DEFAULT_URL)))
    except (EOFError, KeyboardInterrupt):
        print()


if __name__ == "__main__":
    main()
