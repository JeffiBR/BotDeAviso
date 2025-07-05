import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.cliente import cliente_bp
from src.routes.template_mensagem import template_mensagem_bp
from src.routes.configuracao import configuracao_bp
from src.routes.log_mensagem import log_mensagem_bp
from src.routes.renovacao import renovacao_bp
from src.routes.whatsapp import whatsapp_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

# Configurar CORS para permitir requisições do frontend
CORS(app, origins=['*'])

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(cliente_bp, url_prefix='/api')
app.register_blueprint(template_mensagem_bp, url_prefix='/api')
app.register_blueprint(configuracao_bp, url_prefix='/api')
app.register_blueprint(log_mensagem_bp, url_prefix='/api')
app.register_blueprint(renovacao_bp, url_prefix='/api')
app.register_blueprint(whatsapp_bp, url_prefix='/api')

# Configuração do banco de dados
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Importar todos os modelos para garantir que sejam criados
from src.models.cliente import Cliente
from src.models.renovacao import Renovacao
from src.models.log_mensagem import LogMensagem
from src.models.template_mensagem import TemplateMensagem
from src.models.configuracao import Configuracao

with app.app_context():
    db.create_all()
    
    # Inicializar configurações padrão se não existirem
    if Configuracao.query.count() == 0:
        from src.routes.configuracao import inicializar_configuracoes_padrao
        try:
            # Criar configurações padrão programaticamente
            configuracoes_padrao = [
                ('whatsapp_ativo', False, 'boolean', 'whatsapp', 'Ativar/desativar integração com WhatsApp'),
                ('whatsapp_intervalo_mensagens', 5, 'integer', 'whatsapp', 'Intervalo em segundos entre mensagens'),
                ('whatsapp_horario_inicio', '08:00', 'string', 'whatsapp', 'Horário de início para envio de mensagens'),
                ('whatsapp_horario_fim', '22:00', 'string', 'whatsapp', 'Horário de fim para envio de mensagens'),
                ('ia_ativa', False, 'boolean', 'ia', 'Ativar/desativar integração com IA'),
                ('ia_provedor', 'openrouter', 'string', 'ia', 'Provedor de IA (openrouter, openai, etc.)'),
                ('ia_api_key', '', 'string', 'ia', 'Chave da API do provedor de IA'),
                ('ia_modelo', 'meta-llama/llama-3.1-8b-instruct:free', 'string', 'ia', 'Modelo de IA a ser usado'),
                ('ia_tom_voz', 'profissional', 'string', 'ia', 'Tom de voz da IA'),
                ('sistema_nome_empresa', 'Minha Empresa', 'string', 'sistema', 'Nome da empresa'),
            ]
            
            for chave, valor, tipo, categoria, descricao in configuracoes_padrao:
                config = Configuracao(
                    chave=chave,
                    tipo=tipo,
                    categoria=categoria,
                    descricao=descricao
                )
                config.set_valor_tipado(valor)
                db.session.add(config)
            
            db.session.commit()
            print("Configurações padrão inicializadas com sucesso!")
        except Exception as e:
            print(f"Erro ao inicializar configurações: {e}")
            db.session.rollback()

# Rota para verificar se a API está funcionando
@app.route('/health')
def health_check():
    return {'status': 'OK', 'message': 'API está funcionando!'}

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') != 'production')
