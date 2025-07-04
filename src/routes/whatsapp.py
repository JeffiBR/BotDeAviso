from flask import Blueprint, request, jsonify
from src.services.whatsapp_service import whatsapp_service
from src.models.configuracao import Configuracao
from src.models.user import db

whatsapp_bp = Blueprint('whatsapp', __name__)

@whatsapp_bp.route('/whatsapp/status', methods=['GET'])
def status_whatsapp():
    """Retorna o status do serviço WhatsApp"""
    try:
        conectado = whatsapp_service.verificar_conexao()
        executando = whatsapp_service.executando
        
        return jsonify({
            'executando': executando,
            'conectado': conectado,
            'qr_disponivel': whatsapp_service.qr_code is not None,
            'porta': whatsapp_service.porta
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@whatsapp_bp.route('/whatsapp/iniciar', methods=['POST'])
def iniciar_whatsapp():
    """Inicia o serviço WhatsApp"""
    try:
        if whatsapp_service.executando:
            return jsonify({'mensagem': 'Serviço já está executando'}), 200
        
        sucesso = whatsapp_service.iniciar_servico()
        
        if sucesso:
            # Atualizar configuração
            Configuracao.set_configuracao('whatsapp_ativo', True, 
                                        'Serviço WhatsApp ativo', 'boolean', 'whatsapp')
            
            return jsonify({'mensagem': 'Serviço WhatsApp iniciado com sucesso'})
        else:
            return jsonify({'erro': 'Falha ao iniciar serviço WhatsApp'}), 500
            
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@whatsapp_bp.route('/whatsapp/parar', methods=['POST'])
def parar_whatsapp():
    """Para o serviço WhatsApp"""
    try:
        sucesso = whatsapp_service.parar_servico()
        
        if sucesso:
            # Atualizar configuração
            Configuracao.set_configuracao('whatsapp_ativo', False, 
                                        'Serviço WhatsApp inativo', 'boolean', 'whatsapp')
            
            return jsonify({'mensagem': 'Serviço WhatsApp parado com sucesso'})
        else:
            return jsonify({'erro': 'Falha ao parar serviço WhatsApp'}), 500
            
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@whatsapp_bp.route('/whatsapp/qr', methods=['GET'])
def obter_qr_code():
    """Obtém o QR code para conexão"""
    try:
        qr_code = whatsapp_service.obter_qr_code()
        
        if qr_code:
            return jsonify({
                'qr_code': qr_code,
                'instrucoes': 'Escaneie este QR code com seu WhatsApp para conectar'
            })
        else:
            return jsonify({'erro': 'QR code não disponível'}), 404
            
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@whatsapp_bp.route('/whatsapp/enviar-teste', methods=['POST'])
def enviar_mensagem_teste():
    """Envia uma mensagem de teste"""
    try:
        dados = request.get_json()
        
        if 'numero' not in dados or 'mensagem' not in dados:
            return jsonify({'erro': 'Número e mensagem são obrigatórios'}), 400
        
        if not whatsapp_service.conectado:
            return jsonify({'erro': 'WhatsApp não está conectado'}), 400
        
        sucesso = whatsapp_service.enviar_mensagem(
            dados['numero'], 
            dados['mensagem']
        )
        
        if sucesso:
            return jsonify({'mensagem': 'Mensagem de teste enviada com sucesso'})
        else:
            return jsonify({'erro': 'Falha ao enviar mensagem de teste'}), 500
            
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@whatsapp_bp.route('/whatsapp/processar-avisos', methods=['POST'])
def processar_avisos_manual():
    """Processa avisos manualmente"""
    try:
        if not whatsapp_service.conectado:
            return jsonify({'erro': 'WhatsApp não está conectado'}), 400
        
        # Executar processamento em thread separada para não bloquear
        import threading
        
        def processar():
            whatsapp_service.processar_avisos_automaticos()
        
        thread = threading.Thread(target=processar)
        thread.start()
        
        return jsonify({'mensagem': 'Processamento de avisos iniciado'})
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@whatsapp_bp.route('/whatsapp/configuracoes', methods=['GET'])
def obter_configuracoes_whatsapp():
    """Obtém configurações do WhatsApp"""
    try:
        configuracoes = {
            'ativo': Configuracao.get_configuracao('whatsapp_ativo', False),
            'intervalo_mensagens': Configuracao.get_configuracao('whatsapp_intervalo_mensagens', 60),
            'horario_inicio': Configuracao.get_configuracao('whatsapp_horario_inicio', '08:00'),
            'horario_fim': Configuracao.get_configuracao('whatsapp_horario_fim', '22:00'),
            'dias_funcionamento': Configuracao.get_configuracao('whatsapp_dias_funcionamento', 
                ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'])
        }
        
        return jsonify({'configuracoes': configuracoes})
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@whatsapp_bp.route('/whatsapp/configuracoes', methods=['PUT'])
def atualizar_configuracoes_whatsapp():
    """Atualiza configurações do WhatsApp"""
    try:
        dados = request.get_json()
        
        configuracoes_atualizadas = []
        
        # Atualizar cada configuração se fornecida
        if 'intervalo_mensagens' in dados:
            config = Configuracao.set_configuracao(
                'whatsapp_intervalo_mensagens', 
                dados['intervalo_mensagens'],
                'Intervalo em segundos entre mensagens',
                'integer',
                'whatsapp'
            )
            configuracoes_atualizadas.append(config.to_dict())
        
        if 'horario_inicio' in dados:
            config = Configuracao.set_configuracao(
                'whatsapp_horario_inicio',
                dados['horario_inicio'],
                'Horário de início para envio de mensagens',
                'string',
                'whatsapp'
            )
            configuracoes_atualizadas.append(config.to_dict())
        
        if 'horario_fim' in dados:
            config = Configuracao.set_configuracao(
                'whatsapp_horario_fim',
                dados['horario_fim'],
                'Horário de fim para envio de mensagens',
                'string',
                'whatsapp'
            )
            configuracoes_atualizadas.append(config.to_dict())
        
        if 'dias_funcionamento' in dados:
            config = Configuracao.set_configuracao(
                'whatsapp_dias_funcionamento',
                dados['dias_funcionamento'],
                'Dias da semana para funcionamento',
                'json',
                'whatsapp'
            )
            configuracoes_atualizadas.append(config.to_dict())
        
        return jsonify({
            'mensagem': f'{len(configuracoes_atualizadas)} configurações atualizadas',
            'configuracoes': configuracoes_atualizadas
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@whatsapp_bp.route('/whatsapp/logs', methods=['GET'])
def obter_logs_whatsapp():
    """Obtém logs do serviço WhatsApp"""
    try:
        import os
        
        log_file = os.path.join(
            os.path.dirname(__file__), '..', '..', 'logs', 'whatsapp.log'
        )
        
        if not os.path.exists(log_file):
            return jsonify({'logs': [], 'total': 0})
        
        # Ler últimas 100 linhas do log
        with open(log_file, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        
        # Pegar últimas linhas
        ultimas_linhas = linhas[-100:] if len(linhas) > 100 else linhas
        
        logs = []
        for linha in ultimas_linhas:
            linha = linha.strip()
            if linha:
                logs.append(linha)
        
        return jsonify({
            'logs': logs,
            'total': len(logs),
            'arquivo': log_file
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@whatsapp_bp.route('/whatsapp/limpar-logs', methods=['DELETE'])
def limpar_logs_whatsapp():
    """Limpa os logs do WhatsApp"""
    try:
        import os
        
        log_file = os.path.join(
            os.path.dirname(__file__), '..', '..', 'logs', 'whatsapp.log'
        )
        
        if os.path.exists(log_file):
            os.remove(log_file)
        
        return jsonify({'mensagem': 'Logs limpos com sucesso'})
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

