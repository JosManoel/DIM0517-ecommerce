## Visão Geral do Projeto
Sistema básico de controle de produtos e estoque para e-commerce, organizado em arquitetura de 3 camadas no mesmo repositório. A stack tecnológica (linguagem e frameworks) ainda será definida e poderá variar por camada, desde que respeite os limites arquiteturais abaixo.

## Estrutura de Pastas e Isolamento de Camadas
```text
src/
├── service/      # Regras de negócio puras (100% independente de HTTP e UI)
├── api/          # API REST (apenas rotas, validação de entrada e mapeamento HTTP)
└── frontend/     # Cliente Console ou Web simples (consome exclusivamente a API REST)
tests/            # Testes unitários
```

## Regras Arquiteturais Obrigatórias
* **src/service é agnóstico de transporte:** Nunca importe frameworks web, objetos de requisição/resposta HTTP ou status codes (400, 404, etc.) dentro de src/service. Todas as operações devem ser invocáveis diretamente por código (para futuros testes unitários).
* **src/api não contém regra de negócio:** Os controllers/handlers devem apenas validar tipos de entrada, repassar a chamada para src/service e traduzir o retorno ou exceção de domínio para o status HTTP correspondente.
* **src/frontend não acessa src/service:** Toda comunicação do front-end deve ocorrer via chamadas HTTP para src/api.
* **Integridade de dados:** Nenhuma operação que resulte em erro pode alterar o estoque. A operação de venda deve ser atômica (se qualquer item da lista for inválido, nenhum estoque é alterado).

## Contrato da API REST (Obrigatório)
Embora pastas, arquivos e classes internas sejam escritos em inglês, os endpoints e chaves JSON da API REST devem permanecer estritamente em português:

 * `POST` /loja/produto → Req: {"codigo": int, "preco": decimal} | Resp: 201 {"codigo", "preco", "estoque": 0} | Erros: 400, 409

* `GET` /loja/produto/{codigo}/estoque → Resp: 200 {"codigo", "estoque"} | Erros: 400, 404

* `PUT` /loja/produto/{codigo}/entrada → Req: {"quantidade": int} | Resp: 200 {"codigo", "estoque"} | Erros: 400, 404

* `PUT` /loja/produto/{codigo}/saida → Req: {"quantidade": int} | Resp: 200 {"codigo", "estoque"} | Erros: 400, 404

* `POST` /loja/venda → Req: {"itens": [{"codigo": int, "quantidade": int}]} | Resp: 201 {"total", "itens": [{"codigo", "quantidade", "subtotal", "estoque"}]} | Erros: 400, 404

> Nota: A entidade Produto possui exclusivamente os atributos codigo (inteiro), preco (decimal) e estoque (inteiro).

## Fluxo de Git e Rastreabilidade (GitFlow)

* **Branches permanentes:** main (releases estabilizadas) e dev (integração). Nunca sugira ou execute commits diretos nessas branches durante o desenvolvimento de funcionalidades.
* **Branches auxiliares:** Toda branch deve partir de dev (ou release/* para bugfixes) e conter o ID da issue: feature/issue-<ID>-<descricao-curta> ou bugfix/issue-<ID>-<descricao-curta>.
* **Proibição de exclusão:** NUNCA exclua nenhuma branch remota, mesmo após o merge.
* **Commits:** Utilize Conventional Commits (feat:, fix:, chore:, docs:, test:) e sempre referencie a issue correspondente no final da mensagem (_ex.: feat: implementa cadastro de produto na camada de servico (Refs #4)_).
