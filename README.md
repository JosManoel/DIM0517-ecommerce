<h1 align="center">
  DIM0517-ecommerce
  <p>Sistema básico de controle de produtos e estoque para e-commerce</p>
</h1>

<p align="center">
  <a href="#sobre-este-projeto">🔍 Sobre este projeto</a> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#estrutura-do-projeto">📁 Estrutura do projeto</a> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#como-executar">🚀 Como executar</a> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#consideracoes">📑 Considerações</a> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#licenca">📝 Licença</a>
</p>

<hr>

<h2 id="sobre-este-projeto">🔍 Sobre este projeto</h2>

O **DIM0517-ecommerce** é um sistema básico de controle de produtos e estoque para uma loja virtual, estruturado em **três camadas** (serviço, API REST e front-end) e desenvolvido seguindo o padrão **GitFlow** com rastreabilidade entre tarefas (issues) e alterações no código.

O sistema contempla cinco operações principais:
* **Cadastrar Produto**
* **Consultar Estoque**
* **Entrada de Estoque**
* **Saída de Estoque**
* **Venda**

<hr>

<h2 id="estrutura-do-projeto">📁 Estrutura do projeto</h2>

```text
DIM0517-ecommerce/
├── .github/          # Templates de issues, pull requests e workflows
├── docs/             # Documentação do projeto
├── src/
│   ├── service/      # Camada de serviço (regras de negócio independentes de HTTP e UI)
│   ├── api/          # API REST (rotas, validação de entrada e mapeamento HTTP)
│   └── frontend/     # Cliente simples (console ou web) que consome a API REST
└── tests/            # Testes unitários
```

<hr>

<h2 id="como-executar">🚀 Como executar</h2>

Requer **Python 3.10 ou mais novo**. Rode os comandos na raiz do repositório.

### Instalar as dependências

```bash
python3 -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Subir a API

```bash
flask --app src.api.app run
```

A API fica em `http://127.0.0.1:5000`. Os dados ficam em memória e somem quando ela é encerrada.

### Abrir o console

Com a API rodando, em outro terminal:

```bash
source .venv/bin/activate
python -m src.frontend.console
```

### Trocar a porta

No macOS, o AirPlay pode ocupar a porta 5000. Nesse caso, suba a API em outra porta e informe o endereço ao console pela variável `LOJA_API_URL`:

```bash
flask --app src.api.app run --port 5001
LOJA_API_URL=http://127.0.0.1:5001 python -m src.frontend.console
```

### Rodar os testes

```bash
python -m unittest discover -s tests -t .
```

### Exemplos de chamadas

Os exemplos seguem esta ordem, com a API recém-iniciada.

Cadastrar Produto: responde `201`

```bash
curl -X POST http://127.0.0.1:5000/loja/produto -H "Content-Type: application/json" -d '{"codigo": 123, "preco": 59.90}'
# {"codigo":123,"estoque":0,"preco":59.9}
```

Entrada de Estoque: responde `200`

```bash
curl -X PUT http://127.0.0.1:5000/loja/produto/123/entrada -H "Content-Type: application/json" -d '{"quantidade": 15}'
# {"codigo":123,"estoque":15}
```

Consultar Estoque: responde `200`

```bash
curl http://127.0.0.1:5000/loja/produto/123/estoque
# {"codigo":123,"estoque":15}
```

Saída de Estoque: responde `200`

```bash
curl -X PUT http://127.0.0.1:5000/loja/produto/123/saida -H "Content-Type: application/json" -d '{"quantidade": 5}'
# {"codigo":123,"estoque":10}
```

Venda: responde `201`

```bash
curl -X POST http://127.0.0.1:5000/loja/venda -H "Content-Type: application/json" -d '{"itens": [{"codigo": 123, "quantidade": 2}]}'
# {"itens":[{"codigo":123,"estoque":8,"quantidade":2,"subtotal":119.8}],"total":119.8}
```

Em caso de erro, a resposta traz `{"erro": "<mensagem>"}`:

| Situação | Status |
| --- | --- |
| Dado ausente ou inválido | 400 |
| Estoque insuficiente | 400 |
| Produto não encontrado | 404 |
| Produto já cadastrado | 409 |

<hr>

<h2 id="consideracoes">📑 Considerações</h2>

Este projeto está sendo desenvolvido como **projeto final da disciplina de Gerência de Configuração e Mudanças (DIM0517)**, ministrada no curso de **Bacharelado em Tecnologia da Informação**, no **[Instituto Metrópole Digital](https://www.metropoledigital.ufrn.br/portal/)/[UFRN](https://ufrn.br)**.

* José Manoel Freitas da Silva | [JosManoel](https://github.com/JosManoel)
* Guilherme Augusto Pondofe Santana  | [pondof](https://github.com/pondof)
* Carlos Henrique da Silva Guimaraes | [chenrique29](https://github.com/chenrique29)

<hr>

<h2 id="licenca">📝 Licença</h2>

- Este projeto está sob a licença [MIT](LICENSE).

<hr>

<div align="center">

  👋🏾 Feito com ☕ ☕ ☕ ☕ ☕ , 🎧 e 💻.
</div>
