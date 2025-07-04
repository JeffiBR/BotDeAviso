# Sistema de Aviso de Vencimento

Sistema completo para gerenciamento de clientes e avisos de vencimento via WhatsApp, desenvolvido para negócios de IPTV, VPN e outros serviços digitais.

## 🚀 Funcionalidades

### 📋 Gestão de Clientes
- Cadastro completo de clientes com dados pessoais e planos
- Suporte para três tipos de produtos: **IPTV**, **VPN** e **OUTROS**
- Controle de datas de vencimento e valores
- Sistema de ativação/desativação de clientes

### 📱 Integração WhatsApp
- Conexão via QR code
- Envio automático de mensagens de vencimento
- Configuração de horários e intervalos de funcionamento
- Logs completos de mensagens enviadas

### 🎨 Templates de Mensagem
- Templates personalizáveis por tipo de produto
- Variáveis dinâmicas: `{nome}`, `{plano}`, `{valor}`, `{dias}`
- Sistema de templates padrão e personalizados
- Preview de mensagens antes do envio

### 🔄 Sistema de Renovação
- Renovação por períodos: 30, 60, 90, 180 ou 365 dias
- Histórico completo de renovações
- Cálculo automático de novas datas de vencimento
- Controle de valores pagos

### 📊 Dashboards Dinâmicos
- Dashboards separados por tipo de produto
- Métricas de clientes ativos, vencidos e renovações
- Gráficos de crescimento e receita
- Estatísticas em tempo real

### 🤖 Integração com IA
- Configuração para OpenRouter e outros provedores
- Geração automática de mensagens personalizadas
- Configuração de tom de voz e estilo
- Conhecimento específico sobre produtos

### 📈 Logs e Relatórios
- Histórico completo de mensagens enviadas
- Filtros por status, data e tipo
- Estatísticas de sucesso e falhas
- Sistema de reenvio de mensagens

## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados
- **Flask-CORS** - Suporte a CORS

### Frontend (Em desenvolvimento)
- **React** - Biblioteca JavaScript
- **Material-UI** - Componentes visuais
- **Axios** - Cliente HTTP
- **Chart.js** - Gráficos e visualizações

## 📦 Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- Node.js 20+
- Git

### Backend

1. Clone o repositório:
```bash
git clone https://github.com/JeffiBR/BotDeAviso.git
cd BotDeAviso
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o servidor:
```bash
cd src
python main.py
```

O servidor estará disponível em `http://localhost:5000`

### Inicialização dos Dados

Para criar templates padrão de mensagem:
```bash
cd src
python init_templates.py
```

## 🔧 Configuração

### Configurações do Sistema

O sistema possui configurações organizadas por categoria:

#### WhatsApp
- `whatsapp_ativo`: Ativar/desativar integração
- `whatsapp_intervalo_mensagens`: Intervalo entre mensagens (segundos)
- `whatsapp_horario_inicio`: Horário de início (HH:MM)
- `whatsapp_horario_fim`: Horário de fim (HH:MM)

#### IA (OpenRouter)
- `ia_ativa`: Ativar/desativar IA
- `ia_provedor`: Provedor (openrouter, openai, etc.)
- `ia_api_key`: Chave da API
- `ia_modelo`: Modelo a ser usado
- `ia_tom_voz`: Tom de voz (profissional, amigável, formal)

#### Sistema
- `sistema_nome_empresa`: Nome da empresa
- `sistema_timezone`: Fuso horário

## 📚 API Endpoints

### Clientes
- `GET /api/clientes` - Listar clientes
- `POST /api/clientes` - Criar cliente
- `GET /api/clientes/{id}` - Obter cliente
- `PUT /api/clientes/{id}` - Atualizar cliente
- `DELETE /api/clientes/{id}` - Deletar cliente
- `POST /api/clientes/{id}/renovar` - Renovar cliente

### Templates
- `GET /api/templates` - Listar templates
- `POST /api/templates` - Criar template
- `GET /api/templates/{id}` - Obter template
- `PUT /api/templates/{id}` - Atualizar template
- `DELETE /api/templates/{id}` - Deletar template

### Configurações
- `GET /api/configuracoes` - Listar configurações
- `GET /api/configuracoes/{categoria}` - Configurações por categoria
- `PUT /api/configuracoes/{chave}` - Atualizar configuração

### Logs
- `GET /api/logs` - Listar logs de mensagem
- `POST /api/logs` - Criar log
- `GET /api/logs/estatisticas` - Estatísticas de envio

### Renovações
- `GET /api/renovacoes` - Listar renovações
- `GET /api/renovacoes/estatisticas` - Estatísticas de renovação
- `GET /api/renovacoes/cliente/{id}` - Histórico do cliente

## 🎯 Tipos de Produtos Suportados

### IPTV
- Templates específicos para televisão via internet
- Foco em canais e qualidade de transmissão
- Mensagens personalizadas para o segmento

### VPN
- Templates específicos para redes privadas virtuais
- Foco em segurança e privacidade
- Mensagens sobre proteção online

### OUTROS
- Templates genéricos para outros serviços
- Flexibilidade para diferentes tipos de negócio
- Personalização completa

## 🔄 Fluxo de Renovação

1. **Detecção de Vencimento**: Sistema identifica clientes próximos ao vencimento
2. **Envio de Avisos**: Mensagens automáticas nos dias configurados
3. **Processo de Renovação**: Cliente renova por 30, 60, 90, 180 ou 365 dias
4. **Atualização Automática**: Nova data de vencimento calculada automaticamente
5. **Histórico**: Registro completo da renovação no sistema

## 📊 Dashboards

### Métricas Principais
- Clientes ativos por produto
- Clientes vencidos
- Renovações pendentes
- Receita total e por produto
- Taxa de renovação

### Gráficos
- Crescimento mensal de clientes
- Receita por período
- Distribuição por tipo de produto
- Performance de envio de mensagens

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Entre em contato através do sistema

---

**Desenvolvido com ❤️ para automatizar e otimizar seu negócio digital**

