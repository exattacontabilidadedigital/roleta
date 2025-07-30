# 🎰 Roleta da Sorte

Sistema completo de captura de dados e roleta da sorte para eventos empresariais.

## 🚀 Funcionalidades

- ✅ **Formulário de captura** com validação
- ✅ **Roleta animada** com 6 prêmios diferentes
- ✅ **Banco de dados SQLite** para armazenar dados
- ✅ **API REST** completa
- ✅ **Interface responsiva** para mobile e desktop
- ✅ **Sistema de confetes** para prêmios ganhos

## 📋 Pré-requisitos

- Python 3.7+
- pip

## 🛠️ Instalação Local

```bash
# Clonar o repositório
git clone <seu-repositorio>
cd bot-zap-semana-empresarial

# Instalar dependências
pip install -r requirements.txt

# Executar
python app.py
```

Acesse: http://localhost:5000

## 🌐 Hospedagem

### 1. Coolify (Recomendado - Self-hosted)

1. **Instalar Coolify** em seu servidor
2. **Criar novo projeto** no painel do Coolify
3. **Conectar repositório:** `https://github.com/exattacontabilidadedigital/roleta.git`
4. **Configurar:**
   - **Build Pack:** Dockerfile
   - **Port:** 8000
   - **Health Check Path:** /
5. **Deploy automático**

**Vantagens:**
- ✅ **Controle total** do servidor
- ✅ **Deploy automático** do GitHub
- ✅ **SSL automático**
- ✅ **Logs em tempo real**
- ✅ **Backup automático**

### 2. Render (Gratuito)

1. **Criar conta** em [render.com](https://render.com)
2. **Conectar repositório** GitHub/GitLab
3. **Criar novo Web Service**
4. **Configurar:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. **Deploy automático**

### 2. Railway

1. **Criar conta** em [railway.app](https://railway.app)
2. **Conectar repositório**
3. **Deploy automático** (detecta Python)

### 3. Vercel

1. **Criar conta** em [vercel.com](https://vercel.com)
2. **Conectar repositório**
3. **Deploy automático**

### 4. Heroku

```bash
# Instalar Heroku CLI
heroku create roleta-sorte
git push heroku main
```

### 5. PythonAnywhere

1. **Criar conta** em [pythonanywhere.com](https://pythonanywhere.com)
2. **Upload dos arquivos**
3. **Configurar WSGI**

## 📊 Banco de Dados

O sistema usa SQLite localmente. Para produção, considere:

- **PostgreSQL** (Render, Railway)
- **MySQL** (PythonAnywhere)
- **MongoDB** (Vercel)

## 🔧 Configuração de Produção

### Variáveis de Ambiente

```bash
FLASK_ENV=production
PORT=5000
```

### Banco de Dados

Para produção, modifique `app.py`:

```python
# PostgreSQL
DATABASE_URL = os.environ.get('DATABASE_URL')
# ou
# MySQL
# MongoDB
```

## 📱 Uso

1. **Acesse** a URL da aplicação
2. **Preencha** o formulário com dados do visitante
3. **Clique START** para girar a roleta
4. **Veja o resultado** e confetes
5. **Clique "Limpar e Novo Participante"** para próximo visitante

## 🎯 API Endpoints

- `POST /api/salvar-participante` - Salva dados do formulário
- `POST /api/atualizar-resultado` - Salva resultado da roleta
- `GET /api/participantes` - Lista todos os participantes

## 📈 Monitoramento

- **Logs** no console do servidor
- **Dados salvos** no banco SQLite
- **Console do navegador** para debug

## 🔒 Segurança

- ✅ **Validação** de dados no frontend e backend
- ✅ **Sanitização** de inputs
- ✅ **CORS** configurado
- ✅ **Tratamento de erros**

## 🎨 Personalização

- **Cores:** Modificar CSS no `roleta.html`
- **Prêmios:** Alterar array `prizes` no JavaScript
- **Validações:** Ajustar funções de validação
- **Banco:** Trocar SQLite por outro banco

## 📞 Suporte

Para dúvidas ou problemas:
- Verificar logs do servidor
- Console do navegador (F12)
- Banco de dados SQLite local

---

**Desenvolvido para eventos empresariais** 🎉 