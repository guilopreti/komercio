# Komercio Generic Views

Aplicação de gerenciamento de usuários e produtos.

Deploy da API: https://komercio-guilopreti.herokuapp.com/api/

## Endpoints do serviço:

POST /accounts/ - Cadastro de um usuário.

POST /login/ - Retorna um token de autorização validando email e senha.

GET /accounts/ - Lista todos os usuários.

GET /accounts/newest/{int:num}/  - Lista os usuários por ordem de cadastro, retornando a quantidade especificada no parâmetro.

PATCH /accounts/{account_id}/ - Atualiza uma conta, necessário estar logado e ser dono da conta.

PATCH /accounts/{account_id}/management/ - Ativa ou desativa uma conta, necessário estar logado e ser um administrador.

POST /products/ - Cadastro de um produto, necessário estar logado e ser um vendedor.

GET /products/ - Lista todos os produtos.

GET /products/{product_id}/ - Busca um produto.

PATCH /products/{product_id}/ - Atualiza um produto, necessário estar logado e ser dono do produto.
