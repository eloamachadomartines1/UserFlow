# UserFlow

Sistema de CRUD (Criar, Listar, Editar, Excluir) de usuários desenvolvido em Django, com autenticação, tema claro/escuro e upload de foto de perfil.

## Funcionalidades

- Cadastro e login de contas (usando o sistema de autenticação nativo do Django)
- Listagem de usuários com foto, nome, CPF, data de nascimento e sexo
- Máscara automática de CPF (formato `000.000.000-00`) com validação de 11 dígitos
- Upload de foto de perfil, exibida como avatar circular
- Edição e exclusão de usuários (somente para usuários autenticados)
- Exclusão reversível: ao excluir, uma mensagem permite desfazer a ação
- Alternância entre tema claro e escuro, com preferência salva no navegador
- Visualização de usuários cadastrados liberada mesmo sem login (somente leitura)

## Tecnologias usadas

- Python
- Django
- SQLite (banco de dados)
- Pillow (manipulação de imagens)
- HTML, CSS e JavaScript (sem frameworks externos)

## Como rodar o projeto localmente

### Pré-requisitos
- Python instalado
- Git instalado

### Passo a passo

1. Clone o repositório:
```bash
   git clone <url-do-repositorio>
   cd UserFlow
```

2. Crie e ative o ambiente virtual:
```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Linux/Mac
```

3. Instale as dependências:
```bash
   pip install -r requirements.txt
```

4. Aplique as migrações do banco de dados:
```bash
   python manage.py migrate
```

5. (Opcional) Crie um superusuário para acessar o admin:
```bash
   python manage.py createsuperuser
```

6. Rode o servidor:
```bash
   python manage.py runserver
```

7. Acesse no navegador:

http://127.0.0.1:8000/usuarios/


## Estrutura do projeto

UserFlow/
├── app/ # Configurações principais do projeto (settings, urls)
├── usuarios/ # App principal: models, views, forms, templates
│ ├── templates/
│ │ ├── base.html
│ │ └── usuarios/
│ ├── templatetags/ # Filtro customizado para formatar CPF
│ ├── models.py
│ ├── forms.py
│ ├── views.py
│ └── urls.py
├── media/ # Fotos de perfil enviadas pelos usuários
├── requirements.txt
└── manage.py


## Modelo de dados (Usuario)

| Campo | Tipo | Descrição |
|---|---|---|
| nome | Texto | Nome do usuário |
| cpf | Texto (11 dígitos) | CPF, único, validado |
| data_nascimento | Data | Data de nascimento |
| sexo | Escolha (M/F/O) | Masculino, Feminino ou Outro |
| foto | Imagem | Foto de perfil (opcional) |
| ativo | Booleano | Controla exclusão reversível (soft delete) |

## Capturas de tela

### Tela de login
![Login](docs/screenshots/login.png)

### Tela de cadastro
![Cadastro](docs/screenshots/cadastro.png)

### Listagem de usuários
![Listagem](docs/screenshots/listagem.png)

### Modo escuro
![Modo escuro](docs/screenshots/modo-escuro.png)