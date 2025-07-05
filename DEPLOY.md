# 🚀 Guia de Deploy - Sistema de Aviso de Vencimento

Este guia explica como fazer o deploy completo do sistema, com **frontend no Netlify** e **backend no Render**.

## 📋 Pré-requisitos

1. Conta no [Netlify](https://netlify.com) (gratuita)
2. Conta no [Render](https://render.com) (gratuita)
3. Repositório no GitHub com o código

## 🔧 Parte 1: Deploy do Backend (Render)

### 1. Acesse o Render
1. Vá para [render.com](https://render.com)
2. Faça login ou crie uma conta
3. Clique em "New +" → "Web Service"

### 2. Conecte o Repositório
1. Conecte sua conta do GitHub
2. Selecione o repositório do projeto
3. Clique em "Connect"

### 3. Configure o Serviço
**Configurações principais:**
- **Name**: `sistema-vencimento-backend`
- **Region**: `Oregon (US West)`
- **Branch**: `main`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python src/main.py`

**Variáveis de Ambiente:**
- `FLASK_ENV`: `production`
- `PORT`: `5000`
- `SECRET_KEY`: `seu-secret-key-aqui`

### 4. Deploy
1. Clique em "Create Web Service"
2. Aguarde o deploy (pode levar alguns minutos)
3. Anote a URL gerada (ex: `https://sistema-vencimento-backend.onrender.com`)

## 🎨 Parte 2: Deploy do Frontend (Netlify)

### 1. Acesse o Netlify
1. Vá para [netlify.com](https://netlify.com)
2. Faça login ou crie uma conta
3. Clique em "Add new site" → "Import an existing project"

### 2. Conecte o Repositório
1. Conecte sua conta do GitHub
2. Selecione o repositório do projeto
3. Clique em "Deploy site"

### 3. Configure o Build
**Configurações automáticas pelo `netlify.toml`:**
- **Base directory**: `frontend`
- **Build command**: `npm run build`
- **Publish directory**: `dist`

### 4. Configure as Variáveis de Ambiente
1. Vá para "Site settings" → "Environment variables"
2. Adicione:
   - `VITE_API_URL`: `https://SUA-URL-DO-RENDER.onrender.com/api`

### 5. Redeploy
1. Vá para "Deploys"
2. Clique em "Trigger deploy" → "Deploy site"

## 🔄 Parte 3: Conectar Frontend e Backend

### 1. Atualize o netlify.toml
Substitua `seu-backend.onrender.com` pela sua URL real do Render:

```toml
[[redirects]]
  from = "/api/*"
  to = "https://SUA-URL-DO-RENDER.onrender.com/api/:splat"
  status = 200
  force = true
```

### 2. Atualize o .env.production
```env
VITE_API_URL=https://SUA-URL-DO-RENDER.onrender.com/api
```

### 3. Commit e Push
```bash
git add .
git commit -m "Configuração de deploy atualizada"
git push origin main
```

## ✅ Verificação

### 1. Teste o Backend
Acesse: `https://SUA-URL-DO-RENDER.onrender.com/health`

Deve retornar:
```json
{
  "status": "OK",
  "message": "API está funcionando!"
}
```

### 2. Teste o Frontend
Acesse sua URL do Netlify e verifique se:
- A página carrega corretamente
- As requisições para a API funcionam
- Não há erros no console

## 🚨 Troubleshooting

### Backend não inicia no Render
1. Verifique os logs no Render
2. Confirme se o `requirements.txt` está correto
3. Verifique se o caminho do `main.py` está correto

### Frontend não conecta com Backend
1. Verifique se a URL da API está correta
2. Confirme se as variáveis de ambiente estão definidas
3. Verifique se o backend está rodando

### Erro de CORS
O backend já está configurado para aceitar requisições de qualquer origem.

## 📝 Notas Importantes

1. **Render gratuito**: O serviço "dorme" após 15 minutos de inatividade
2. **Primeiro acesso**: Pode levar 30-60 segundos para "acordar"
3. **Banco de dados**: Usando SQLite (dados serão perdidos em redeploys)
4. **Para produção**: Considere usar PostgreSQL no Render

## 🔄 Atualizações Futuras

Para atualizar o sistema:
1. Faça as mudanças no código
2. Commit e push para o GitHub
3. Render e Netlify irão fazer redeploy automaticamente

---

**💡 Dica**: Salve as URLs do frontend e backend para referência futura!

- **Frontend**: `https://SEU-SITE.netlify.app`
- **Backend**: `https://SEU-BACKEND.onrender.com`