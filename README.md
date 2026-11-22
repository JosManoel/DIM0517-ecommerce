<h1 align="center">
  DIM0517-ecommerce
  <p>Sistema básico de controle de produtos e estoque para e-commerce</p>
</h1>

<p align="center">
  <a href="#sobre-este-projeto">🔍 Sobre este projeto</a> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#estrutura-do-projeto">📁 Estrutura do projeto</a> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
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

<h2 id="consideracoes">📑 Considerações</h2>

Este projeto está sendo desenvolvido como **projeto final da disciplina de Gerência de Configuração e Mudanças (DIM0517)**, ministrada no curso de **Bacharelado em Tecnologia da Informação**, no **[Instituto Metrópole Digital](https://www.metropoledigital.ufrn.br/portal/)/[UFRN](https://ufrn.br)**.

* José Manoel Freitas da Silva | [JosManoel](https://github.com/JosManoel)
* Guilherme Augusto Pondofe Santana  | [pondof](https://github.com/pondof)
* Carlos Henrique da Silva Guimaraes |

<hr>

<h2 id="licenca">📝 Licença</h2>

- Este projeto está sob a licença [MIT](LICENSE).

<hr>

<div align="center">

  👋🏾 Feito com ☕ ☕ ☕ ☕ ☕ , 🎧 e 💻.
</div>
