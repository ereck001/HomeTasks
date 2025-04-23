# Backend do app HomeTasks

API para gerenciamento de tarefas e compras com autenticação jwt

## Funcionalidades
- **Gerenciar Lista de Compras**: CRUD completo dos produtos.
- **Gerenciar Lista de Tarefas**: CRUD completo das tarefas.
- **Authentication**: Todos os endpoints exigem um token válido.
- **Banco de Dados**: Usa Postgresql para persistência dos dados.
- **Health Check**: Verifica status API.

## Dependências
1. Docker
2. Docker-compose

## Instalação
1. Clone o repositório:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
2. Inicie o docker-compose:
    ```bash
    sudo docker-compose up
