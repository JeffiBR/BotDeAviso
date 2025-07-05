#!/bin/bash

echo "🚀 Iniciando Sistema de Aviso de Vencimento"
echo "=========================================="

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instale o Python 3.11 ou superior."
    exit 1
fi

# Verifica se o Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Instale o Node.js 20 ou superior."
    exit 1
fi

# Cria ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual Python..."
    python3 -m venv venv
fi

# Ativa ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Instala dependências do backend
echo "📦 Instalando dependências do backend..."
pip install -r requirements.txt

# Instala dependências do frontend
echo "📦 Instalando dependências do frontend..."
cd frontend
npm install
cd ..

# Cria diretório do banco de dados se não existir
if [ ! -d "src/database" ]; then
    echo "📁 Criando diretório do banco de dados..."
    mkdir -p src/database
fi

echo "✅ Setup concluído!"
echo ""
echo "Para iniciar o desenvolvimento:"
echo "1. Backend: cd src && python main.py"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo "URLs locais:"
echo "- Backend: http://localhost:5000"
echo "- Frontend: http://localhost:5173"
echo ""
echo "Para deploy, siga as instruções em DEPLOY.md"