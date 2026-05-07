# Lista de Filmes

Uma aplicação web full-stack completa que permite aos usuários descobrir filmes, gerenciar uma lista de favoritos pessoal e compartilhá-la com o mundo.

> **A aplicação está disponível para acesso em:** [**https://movies-list-mmk6.onrender.com/**](https://movies-list-mmk6.onrender.com/)

---

## Sobre o Projeto

A aplicação permite que qualquer visitante pesquise filmes através da API do The Movie Database (TMDb). Para funcionalidades personalizadas, como criar uma lista de favoritos, o usuário pode se cadastrar e fazer login. Cada usuário possui uma lista de favoritos única, que pode ser compartilhada através de um link público.

A interface foi projetada para ser limpa e intuitiva, com um sistema de notificações dinâmicas que fornece feedback em tempo real sobre as ações do usuário.

---

## Funcionalidades

*   **Autenticação de Usuários:** Sistema seguro de Registro e Login utilizando JSON Web Tokens (JWT).
*   **Pesquisa de Filmes (Pública):** Qualquer visitante pode buscar filmes e ver detalhes como pôster, data de lançamento e nota.
*   **Lista de Favoritos Individual:** Usuários logados podem adicionar ou remover filmes da sua lista de favoritos pessoal.
*   **Persistência de Dados:** As informações de usuários e filmes favoritos são salvas em um banco de dados SQLite.
*   **Link de Compartilhamento:** Cada usuário tem um link público único para sua lista de favoritos, com um botão "Copiar" para facilitar o compartilhamento.
*   **Notificações Dinâmicas:** Feedbacks visuais (sucesso, erro, informação) substituem os alertas padrão do navegador, melhorando a experiência do usuário.
*   **Design Consistente:** O layout dos cards de filmes se mantém alinhado e consistente, independentemente do tamanho do título ou da ausência de imagem.

---

## Tecnologias Utilizadas

Este projeto é dividido em duas partes principais: o front-end (cliente) e o back-end (servidor).

#### **Front-End (Client-side)**
*   **React:** Biblioteca para construção da interface de usuário.
*   **React Router:** Para gerenciamento de rotas e navegação.
*   **Axios:** Para realizar as chamadas HTTP para o back-end.
*   **React Context:** Para gerenciamento de estado global, utilizado no sistema de notificações.

#### **Back-End (Server-side)**
*   **Node.js:** Ambiente de execução JavaScript no servidor.
*   **Express.js:** Framework para a construção da API REST.
*   **Knex.js:** Query builder para facilitar a comunicação com o banco de dados.
*   **SQLite3:** Banco de dados relacional leve e baseado em arquivo.
*   **JSON Web Token (JWT):** Para a implementação do sistema de autenticação.
*   **Bcrypt.js:** Para a criptografia (hash) das senhas dos usuários.
*   **Dotenv:** Para gerenciamento de variáveis de ambiente.

---

## Como Executar o Projeto Localmente

Siga os passos abaixo para configurar e rodar a aplicação na sua máquina.

### **Pré-requisitos**

*   **Node.js** (versão 16 ou superior) e **npm**.
*   **Git** instalado.
*   Uma **Chave de API do The Movie Database (TMDb)**. Você pode obter uma gratuitamente [aqui](https://www.themoviedb.org/signup).

### **1. Clone o Repositório**

```bash
git clone https://github.com/FredericoSRamos/Movies-List.git
cd Movies-List
```

### **2. Configure o Back-End**

Navegue até a pasta do servidor, instale as dependências e configure as variáveis de ambiente.

```bash
# Navegue para a pasta do back-end
cd backend

# Instale as dependências
npm install
```

Agora, crie um arquivo chamado `.env` na raiz da pasta `backend` e adicione as seguintes variáveis:

```
# backend/.env

# Sua chave de API v3 do TMDb | Ex: TMDB_API_KEY=CHAVE123
TMDB_API_KEY=SUA_CHAVE_DE_API_DO_TMDB_AQUI

# Um segredo qualquer para gerar os tokens JWT | Ex: JWT_SECRET=F123HE432F66E3Y
JWT_SECRET=SEU_SEGREDO_ALEATORIO_AQUI
```

Por fim, execute a migração do banco de dados para criar as tabelas necessárias:
```bash
npx knex migrate:latest --knexfile knexfile.js
```

### **3. Configure o Front-End**

Em um **novo terminal**, navegue até a pasta do cliente, instale as dependências e configure a variável de ambiente.

```bash
# Navegue para a pasta do front-end (a partir da raiz do projeto)
cd frontend

# Instale as dependências
npm install
```

### **4. Execute a Aplicação**

Você precisará de **dois terminais** abertos para rodar o back-end e o front-end simultaneamente.

*   **No terminal do Back-End (pasta `/backend`):**
    ```bash
    npm start
    ```
    *O servidor será iniciado em `http://localhost:5000`.*

*   **No terminal do Front-End (pasta `/frontend`):**
    ```bash
    npm start
    ```
    *A aplicação React será iniciada e abrirá automaticamente em `http://localhost:3000` no seu navegador.*

Pronto! Agora você pode se registrar, buscar filmes e criar sua lista de favoritos.