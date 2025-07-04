from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.user import db
from src.models.configuracao import Configuracao
import json

configuracao_bp = Blueprint('configuracao', __name__)

@configuracao_bp.route('/configuracoes', methods=['GET'])
def listar_configuracoes():
    """Lista todas as configurações com filtros opcionais"""
    try:
        categoria = request.args.get('categoria')
        
        query = Configuracao.query
        
        if categoria:
            query = query.filter(Configuracao.categoria == categoria)
        
        configuracoes = query.order_by(Configuracao.categoria.asc(), Configuracao.chave.asc()).all()
        
        # Agrupar por categoria
        resultado = {}
        for config in configuracoes:
            if config.categoria not in resultado:
                resultado[config.categoria] = []
            resultado[config.categoria].append(config.to_dict())
        
        return jsonify({
            'configuracoes': resultado,
            'total': len(configuracoes)
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@configuracao_bp.route('/configuracoes/<categoria>', methods=['GET'])
def listar_configuracoes_categoria(categoria):
    """Lista configurações de uma categoria específica"""
    try:
        configuracoes = Configuracao.query.filter_by(categoria=categoria).order_by(Configuracao.chave.asc()).all()
        
        return jsonify({
            'categoria': categoria,
            'configuracoes': [config.to_dict() for config in configuracoes],
            'total': len(configuracoes)
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@configuracao_bp.route('/configuracoes', methods=['POST'])
def criar_configuracao():
    """Cria uma nova configuração"""
    try:
        dados = request.get_json()
        
        # Validações obrigatórias
        if 'chave' not in dados or not dados['chave']:
            return jsonify({'erro': 'Campo chave é obrigatório'}), 400
        
        # Verificar se já existe
        config_existente = Configuracao.query.filter_by(chave=dados['chave']).first()
        if config_existente:
            return jsonify({'erro': 'Configuração com esta chave já existe'}), 400
        
        # Criar configuração
        config = Configuracao(
            chave=dados['chave'],
            descricao=dados.get('descricao'),
            tipo=dados.get('tipo', 'string'),
            categoria=dados.get('categoria', 'sistema')
        )
        
        # Definir valor
        if 'valor' in dados:
            config.set_valor_tipado(dados['valor'])
        
        db.session.add(config)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Configuração criada com sucesso',
            'configuracao': config.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@configuracao_bp.route('/configuracoes/<chave>', methods=['GET'])
def obter_configuracao(chave):
    """Obtém uma configuração específica"""
    try:
        config = Configuracao.query.filter_by(chave=chave).first_or_404()
        return jsonify({'configuracao': config.to_dict()})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@configuracao_bp.route('/configuracoes/<chave>', methods=['PUT'])
def atualizar_configuracao(chave):
    """Atualiza uma configuração existente"""
    try:
        config = Configuracao.query.filter_by(chave=chave).first_or_404()
        dados = request.get_json()
        
        # Atualizar campos se fornecidos
        if 'valor' in dados:
            config.set_valor_tipado(dados['valor'])
        
        if 'descricao' in dados:
            config.descricao = dados['descricao']
        
        if 'tipo' in dados:
            config.tipo = dados['tipo']
        
        if 'categoria' in dados:
            config.categoria = dados['categoria']
        
        config.data_atualizacao = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Configuração atualizada com sucesso',
            'configuracao': config.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@configuracao_bp.route('/configuracoes/<chave>', methods=['DELETE'])
def deletar_configuracao(chave):
    """Deleta uma configuração"""
    try:
        config = Configuracao.query.filter_by(chave=chave).first_or_404()
        db.session.delete(config)
        db.session.commit()
        
        return jsonify({'mensagem': 'Configuração deletada com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@configuracao_bp.route('/configuracoes/batch', methods=['PUT'])
def atualizar_configuracoes_lote():
    """Atualiza múltiplas configurações de uma vez"""
    try:
        dados = request.get_json()
        
        if 'configuracoes' not in dados:
            return jsonify({'erro': 'Campo configuracoes é obrigatório'}), 400
        
        configuracoes_atualizadas = []
        
        for item in dados['configuracoes']:
            if 'chave' not in item:
                continue
            
            config = Configuracao.query.filter_by(chave=item['chave']).first()
            
            if not config:
                # Criar nova configuração se não existir
                config = Configuracao(
                    chave=item['chave'],
                    tipo=item.get('tipo', 'string'),
                    categoria=item.get('categoria', 'sistema'),
                    descricao=item.get('descricao')
                )
                db.session.add(config)
            
            # Atualizar valor
            if 'valor' in item:
                config.set_valor_tipado(item['valor'])
            
            # Atualizar outros campos se fornecidos
            if 'descricao' in item:
                config.descricao = item['descricao']
            
            config.data_atualizacao = datetime.utcnow()
            configuracoes_atualizadas.append(config.to_dict())
        
        db.session.commit()
        
        return jsonify({
            'mensagem': f'{len(configuracoes_atualizadas)} configurações atualizadas com sucesso',
            'configuracoes': configuracoes_atualizadas
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@configuracao_bp.route('/configuracoes/inicializar', methods=['POST'])
def inicializar_configuracoes_padrao():
    """Inicializa as configurações padrão do sistema"""
    try:
        configuracoes_padrao = [
            # Configurações do WhatsApp
            {
                'chave': 'whatsapp_ativo',
                'valor': False,
                'tipo': 'boolean',
                'categoria': 'whatsapp',
                'descricao': 'Ativar/desativar integração com WhatsApp'
            },
            {
                'chave': 'whatsapp_intervalo_mensagens',
                'valor': 5,
                'tipo': 'integer',
                'categoria': 'whatsapp',
                'descricao': 'Intervalo em segundos entre mensagens'
            },
            {
                'chave': 'whatsapp_horario_inicio',
                'valor': '08:00',
                'tipo': 'string',
                'categoria': 'whatsapp',
                'descricao': 'Horário de início para envio de mensagens'
            },
            {
                'chave': 'whatsapp_horario_fim',
                'valor': '22:00',
                'tipo': 'string',
                'categoria': 'whatsapp',
                'descricao': 'Horário de fim para envio de mensagens'
            },
            {
                'chave': 'whatsapp_dias_funcionamento',
                'valor': ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'],
                'tipo': 'json',
                'categoria': 'whatsapp',
                'descricao': 'Dias da semana para funcionamento'
            },
            
            # Configurações da IA
            {
                'chave': 'ia_ativa',
                'valor': False,
                'tipo': 'boolean',
                'categoria': 'ia',
                'descricao': 'Ativar/desativar integração com IA'
            },
            {
                'chave': 'ia_provedor',
                'valor': 'openrouter',
                'tipo': 'string',
                'categoria': 'ia',
                'descricao': 'Provedor de IA (openrouter, openai, etc.)'
            },
            {
                'chave': 'ia_api_key',
                'valor': '',
                'tipo': 'string',
                'categoria': 'ia',
                'descricao': 'Chave da API do provedor de IA'
            },
            {
                'chave': 'ia_modelo',
                'valor': 'meta-llama/llama-3.1-8b-instruct:free',
                'tipo': 'string',
                'categoria': 'ia',
                'descricao': 'Modelo de IA a ser usado'
            },
            {
                'chave': 'ia_tom_voz',
                'valor': 'profissional',
                'tipo': 'string',
                'categoria': 'ia',
                'descricao': 'Tom de voz da IA (profissional, amigável, formal)'
            },
            {
                'chave': 'ia_estilo_resposta',
                'valor': 'conciso',
                'tipo': 'string',
                'categoria': 'ia',
                'descricao': 'Estilo de resposta (conciso, detalhado, criativo)'
            },
            {
                'chave': 'ia_conhecimento_produtos',
                'valor': {
                    'IPTV': 'Serviço de televisão via internet com canais em alta definição',
                    'VPN': 'Rede privada virtual para navegação segura e anônima',
                    'OUTROS': 'Outros serviços digitais oferecidos'
                },
                'tipo': 'json',
                'categoria': 'ia',
                'descricao': 'Conhecimento específico sobre os produtos'
            },
            
            # Configurações de notificação
            {
                'chave': 'notificacao_dias_antecedencia',
                'valor': [7, 3, 1],
                'tipo': 'json',
                'categoria': 'notificacao',
                'descricao': 'Dias de antecedência para envio de notificações'
            },
            {
                'chave': 'notificacao_pos_vencimento',
                'valor': [1, 3, 7],
                'tipo': 'json',
                'categoria': 'notificacao',
                'descricao': 'Dias após vencimento para envio de notificações'
            },
            
            # Configurações do sistema
            {
                'chave': 'sistema_nome_empresa',
                'valor': 'Minha Empresa',
                'tipo': 'string',
                'categoria': 'sistema',
                'descricao': 'Nome da empresa'
            },
            {
                'chave': 'sistema_timezone',
                'valor': 'America/Sao_Paulo',
                'tipo': 'string',
                'categoria': 'sistema',
                'descricao': 'Fuso horário do sistema'
            }
        ]
        
        configuracoes_criadas = 0
        
        for config_data in configuracoes_padrao:
            # Verificar se já existe
            config_existente = Configuracao.query.filter_by(chave=config_data['chave']).first()
            
            if not config_existente:
                config = Configuracao(
                    chave=config_data['chave'],
                    tipo=config_data['tipo'],
                    categoria=config_data['categoria'],
                    descricao=config_data['descricao']
                )
                config.set_valor_tipado(config_data['valor'])
                db.session.add(config)
                configuracoes_criadas += 1
        
        db.session.commit()
        
        return jsonify({
            'mensagem': f'{configuracoes_criadas} configurações padrão inicializadas com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

