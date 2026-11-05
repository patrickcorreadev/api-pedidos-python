# 🚀 Order Management RESTful API (Python / FastAPI)

Uma API RESTful escalável, segura e pronta para produção construída com **FastAPI**, **SQLModel**, e totalmente conteinerizada com **Docker**. Este projeto adota uma arquitetura modular inspirada no padrão MVC do Laravel (separação estrita entre Rotas, Controllers e Models), garantindo alta manutenibilidade.

## ✨ Funcionalidades
- **Autenticação Segura**: Sistema completo de login baseado em Bearer Tokens JWT e criptografia de senhas com `bcrypt`.
- **Proteção de Rotas**: Endpoints de pedidos protegidos por dependências de validação de token em tempo real.
- **Persistência de Dados**: Integração nativa com SQLite (com volumes espelhados no Docker) e suporte nativo para migração para MySQL.
- **Operações CRUD Completas**: Gerenciamento completo de Usuários e Pedidos seguindo os padrões do `apiResource`.
- **Documentação Automática**: Swagger UI interativo gerado nativamente pelo FastAPI para testes rápidos.
- **Conteinerização**: Ambiente 100% isolado com Docker e Docker Compose, garantindo paridade entre desenvolvimento e produção.

## 📁 Estrutura da Arquitetura (Padrão MVC)
```text
meu_projeto/
├── app/
│   ├── controllers/      # Lógica de negócio (Auth, Users, Orders)
│   ├── database/         # Configurações de conexão e sessões do banco
│   ├── models/           # Modelagem de tabelas e esquemas de validação (SQLModel)
│   ├── routes/           # Mapeamento e declaração dos endpoints (Roteador HTTP)
│   └── main.py           # Ponto de entrada e ciclo de vida da aplicação
├── Dockerfile            # Instruções de build da imagem Docker
├── docker-compose.yml    # Orquestração do ambiente de execução
└── requirements.txt      # Gerenciamento de dependências do Python
```

## 🛠️ Tecnologias Utilizadas
- **Python 3.11**
- **FastAPI**
- **SQLModel (SQLAlchemy + Pydantic)**
- **JWT (python-jose & passlib)**
- **Docker & Docker Compose**
- **SQLite / MySQL**

## 🚦 Como Executar o Projeto

### 🐳 Via Docker (Recomendado)
Certifique-se de ter o Docker e o Docker Compose instalados na sua máquina.

1. Clone o repositório e navegue até a pasta:
   ```bash
   git clone https://github.com
   cd api-pedidos-python
   ```

2. Suba o container com o comando:
   ```bash
   docker-compose up --build
   ```

3. Acesse a API e a documentação interativa no seu navegador:
   - **Swagger UI (Testar Rotas):** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Status da API:** [http://localhost:8000/](http://localhost:8000/)

*Nota: Ao rodar o container, um arquivo `database.db` será gerado automaticamente na raiz do seu projeto local graças ao mapeamento de volumes, garantindo que nenhum dado seja perdido ao reiniciar o Docker.*

### 💻 Via Localhost (Desenvolvimento)
Caso prefira rodar fora do Docker:

1. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Inicie o servidor de desenvolvimento:
   ```bash
   uvicorn app.main:app --reload
   ```