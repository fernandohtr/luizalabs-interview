# Luizalabs

O presente projeto visa aplicação em vaga na Luizalabs.

## Cenário

O desafio consiste na criação de uma funcionalidade de Produtos Favoritos dos Clientes da empresa.
O aplicativo da empresa enviará requisições HTTP para um novo backend que deverá gerenciar os clientes e seus
produtos favoritos.

Esta nova API REST terá um grande volume de requisições, sendo necessário preocupação 
com performance.

### Requisitos do desafio

- Deve ser possível criar, atualizar, visualizar e remover Clientes
    - O cadastro dos clientes deve conter apenas seu nome e endereço de e-mail
    - Um cliente não pode se registrar duas vezes com o mesmo endereço de e-mail
- Cada cliente só deverá ter uma única lista de produtos favoritos
- Em uma lista de produtos favoritos podem existir uma quantidade ilimitada de produtos
    - Um produto não pode ser adicionado em uma lista caso ele não exista
    - Um produto não pode estar duplicado na lista de produtos favoritos de um cliente
    - A documentação da API de produtos pode ser visualizada neste [link](https://gist.github.com/Bgouveia/9e043a3eba439489a35e70d1b5ea08ec)
- O dispositivo que irá renderizar a resposta fornecida por essa nova API irá apresentar o
Título, Imagem, Preço e irá utilizar o ID do produto para formatar o link que ele irá acessar.
Quando existir um review para o produto, o mesmo será exibido por este dispositivo. Não é
necessário criar um frontend para simular essa renderização (foque no desenvolvimento da
API).
- O acesso à api deve ser aberto ao mundo, porém deve possuir autenticação e autorização.

## Modelagem do banco de dados

Pensando em otimização optou-se em criar uma tabela para produtos a fim de diminuir a carga sobre 
as requisições realizadas para API externa.

![model](./docs/images/luizalabs-model.drawio.png)

## Requisitos

- Docker e Docker Compose

Para contribuição no desenvolvimento recomenda-se, também:
- Python 3.12
- Poetry

## Execução do projeto

Estando na raiz do projeto execute:
```bash
make up
```

Com isso o projeto será iniciado no container, instalando todas as dependências e migrações necessárias.

O Projeto poderá ser acessado em [http://127.0.0.1:8080/api/schema/swagger/](http://127.0.0.1:8080/api/schema/swagger/).

## Usando a aplicação

Para usar a aplicação é necessário criar um usuário administrador.
Com a aplicação rodando, execute:
```bash
make createsuperuser
```

### Login

Após o cadastro, faça o login no endpoint [http://127.0.0.1:8080/api/v1/users/auth/login/](http://127.0.0.1:8080/api/v1/users/auth/login/).

Você receberá os tokens de acesso. Exemplo:
```bash
curl --location 'localhost:8080/api/v1/users/auth/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "admin@example.com",
    "password": "abc123"
}'
```

Resposta:
```json
{
    "id": 1,
    "email": "admin@example.com",
    "tokens": {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyOTAyNzI1OCwiaWF0IjoxNzI4OTQwODU4LCJqdGkiOiI2ZWQ5OTkzNTc3MzQ0MzVmYTdlYTU5MDM2ZmJiNTE0NSIsInVzZXJfaWQiOjF9.heQWe4oXSCHxhCibj9GfO-Y0k7cmGDbUcSrTATkOH2U",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4OTQ0NDU4LCJpYXQiOjE3Mjg5NDA4NTgsImp0aSI6ImE4MzZhOTIyZjEwMzQ5NmVhYTMyOGMzZTcxYmZiM2U5IiwidXNlcl9pZCI6MX0.yteVjzWdH8zUZ-DBss81QEy2Q2XO_dUA0yy6NT10zbo"
    }
}
```

### Criando Cliente

Após realizar o login é possível interagir com os demais endpoints.
Exemplo de como criar um cliente na API:
```bash
curl --location 'localhost:8080/api/v1/customers/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4OTQ0NDU4LCJpYXQiOjE3Mjg5NDA4NTgsImp0aSI6ImE4MzZhOTIyZjEwMzQ5NmVhYTMyOGMzZTcxYmZiM2U5IiwidXNlcl9pZCI6MX0.yteVjzWdH8zUZ-DBss81QEy2Q2XO_dUA0yy6NT10zbo' \
--data-raw '{
    "name": "John",
    "email": "john@example.com"
}'
```

Resposta:
```json
{
    "id": 1,
    "name": "John",
    "email": "john@example.com",
    "favorite": {
        "id": 1,
        "favorite_products": []
    }
}
```

Como mostrado na [modelagem do banco de dados](#modelagem-do-banco-de-dados), todo cliente tem uma lista de produtos
favoritos que é criada juntamente com a criação do usuário.

Acesse [aqui](#endpoints) para interagir com os demais endpoints.

## Fluxo para adicionar novos produtos

Um ponto fundamental na otimização da aplicação é o fluxo para adicionar novos 
produtos aos clientes, pois a consulta a todo momento ao endpoint `http://challenge-api.luizalabs.com/api/product/<ID>/`
é custosa e lenta.

Assim, faz sentido criar uma tabela de produtos na aplicação e utilizar cache.

Para o endpoint `/api/v1/favorites/customers/<customer_id>/` adicionar novos
produtos ao cliente, ele segue a seguinte lógica:

![flow](./docs/images/luizalabs-fluxo.drawio.png)

### Mostrar os logs

Para ver os logs da aplicação, execute:
```bash
make logs
```

### Execução dos testes unitários

Estando com o projeto rodando, execute:
```bash
make test
```

## Endpoints

A aplicação conta com documentação na própria API. Dessa forma, com a aplicação 
rodando, acesse um dos seguintes endpoints:

[http://127.0.0.1:8080/api/schema/swagger/](http://127.0.0.1:8080/api/schema/swagger/)

[http://127.0.0.1:8080/api/schema/redoc/](http://127.0.0.1:8080/api/schema/redoc/)
