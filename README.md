# Trabalho Prático 1 - API REST com Persistência em CSV usando FastAPI

*Disciplina*: Desenvolvimento de Software para Persistência  
*Dupla*:  
- Janaina Macário de Sousa - 542086 
- Jamille Bezerra Candido - 538276 

## Objetivo

Desenvolver uma API REST utilizando o framework *FastAPI* para realizar operações de CRUD (Create, Read, Update, Delete) 
em *três entidades distintas, com persistência dos dados em arquivos **CSV*. A aplicação também inclui funcionalidades 
extras como: compactação em ZIP, cálculo de hash SHA256, filtragem por atributos, geração de XML e registro de logs.

## Domínio 

[Sistema de Venda de Livros]  

## Entidades e Atributos

### Livro
Representa um livro disponível para compra.

| Atributo | Tipo  | Descrição                   |
|----------|-------|-----------------------------|
| id       | int   | Identificador único         |
| titulo   | str   | Título do livro             |
| autor    | str   | Autor do livro              |
| genero   | str   | Gênero literário            |
| preco    | float | Preço do livro              |


### Usuário
Representa o cliente que realiza a compra de livros.

| Atributo       | Tipo  | Descrição                   |
|----------------|-------|-----------------------------|
| id             | int   | Identificador do usuário    |
| nome           | str   | Nome completo               |
| email          | str   | E-mail do usuário           |
| cpf            | str   | CPF do usuário              |
| data_cadastro  | str   | Data de cadastro (YYYY-MM-DD)|


### Pedido
Representa a compra feita por um usuário.

| Atributo      | Tipo        | Descrição                                |
|---------------|-------------|--------------------------------------------|
| id            | int         | Identificador do pedido                    |
| usuario_id    | int         | ID do usuário que fez o pedido             |
| data_pedido   | str         | Data da compra (YYYY-MM-DD)                |
| livros        | List[int]   | Lista de IDs dos livros comprados          |
| status        | str         | Status do pedido (Pendente, Concluído...)  |
| valor_total   | float       | Valor total da compra                      |

## Funcionalidades da API

| Código | Funcionalidade | Descrição |
|--------|----------------|-----------|
| F1 | *CRUD completo* | Criar, listar, atualizar e deletar registros para cada entidade. |
| F2 | *Listagem completa* | Retorna todos os registros da entidade em formato JSON. |
| F3 | *Quantidade de entidades* | Retorna o total de registros da entidade. |
| F4 | *Compactação ZIP* | Compacta o arquivo CSV em .zip e disponibiliza para download. |
| F5 | *Filtros* | Permite filtrar registros com base em atributos específicos. |
| F6 | *Hash SHA256* | Gera o hash SHA256 do CSV para verificação de integridade. |
| F7 | *Sistema de Logs* | Registra todas as operações em um arquivo de log com data/hora. |
| F8 | *Conversão para XML* | Converte os dados da entidade do CSV para arquivo .xml. |


## Como executar o projeto

1. Clone o repositório e navegue até o diretório do projeto:

bash
git clone https://github.com/seuusuario/nome-do-projeto.git
cd nome-do-projeto



2. Verifique se o Python está instalado na sua máquina:

bash
python --version

Se não tiver o Python, baixe e instale a versão mais recente.


3. Instale as dependências:

bash
pip install -r requirements.txt



4. Rode a aplicação:

bash
python -m uvicorn app.main:app --reload



5. Acesse a documentação interativa (Swagger UI) em:

bash
http://127.0.0.1:8000/docs