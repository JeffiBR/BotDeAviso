from flask import Blueprint, request, jsonify
from datetime import datetime, date
from src.models.user import db
from src.models.log_mensagem import LogMensagem
from src.models.cliente import Cliente
from sqlalchemy import and_, or_

log_mensagem_bp = Blueprint('log_mensagem', __name__)

@log_mensagem_bp.route('/logs', methods=['GET'])
def listar_logs():
    """Lista todos os logs de mensagem com filtros opcionais"""
    try:
        # Parâmetros de filtro
        cliente_id = request.args.get('cliente_id', type=int)
        status = request.args.get('status')
        tipo_notificacao = request.args.get('tipo_notificacao')
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # Query base
        query = LogMensagem.query
        
        # Aplicar filtros
        if cliente_id:
            query = query.filter(LogMensagem.cliente_id == cliente_id)
        
        if status:
            query = query.filter(LogMensagem.status == status)
        
        if tipo_notificacao:
            query = query.filter(LogMensagem.tipo_notificacao == tipo_notificacao)
        
        if data_inicio:
            try:
                data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d')
                query = query.filter(LogMensagem.data_criacao >= data_inicio_obj)
            except ValueError:
                return jsonify({'erro': 'Formato de data_inicio inválido. Use YYYY-MM-DD'}), 400
        
        if data_fim:
            try:
                data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d')
                # Adicionar 23:59:59 para incluir todo o dia
                data_fim_obj = data_fim_obj.replace(hour=23, minute=59, second=59)
                query = query.filter(LogMensagem.data_criacao <= data_fim_obj)
            except ValueError:
                return jsonify({'erro': 'Formato de data_fim inválido. Use YYYY-MM-DD'}), 400
        
        # Ordenar por data de criação (mais recentes primeiro)
        query = query.order_by(LogMensagem.data_criacao.desc())
        
        # Paginação
        logs_paginados = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Incluir dados do cliente nos logs
        logs_com_cliente = []
        for log in logs_paginados.items:
            log_dict = log.to_dict()
            cliente = Cliente.query.get(log.cliente_id)
            if cliente:
                log_dict['cliente_nome'] = cliente.nome_completo
                log_dict['cliente_tipo_produto'] = cliente.tipo_produto
            logs_com_cliente.append(log_dict)
        
        return jsonify({
            'logs': logs_com_cliente,
            'total': logs_paginados.total,
            'pages': logs_paginados.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': logs_paginados.has_next,
            'has_prev': logs_paginados.has_prev
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@log_mensagem_bp.route('/logs', methods=['POST'])
def criar_log():
    """Cria um novo log de mensagem"""
    try:
        dados = request.get_json()
        
        # Validações obrigatórias
        campos_obrigatorios = ['cliente_id', 'telefone_destino', 'mensagem', 'status']
        
        for campo in campos_obrigatorios:
            if campo not in dados or not dados[campo]:
                return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
        
        # Verificar se cliente existe
        cliente = Cliente.query.get(dados['cliente_id'])
        if not cliente:
            return jsonify({'erro': 'Cliente não encontrado'}), 404
        
        # Validar status
        if dados['status'] not in ['enviada', 'falha', 'pendente']:
            return jsonify({'erro': 'Status deve ser enviada, falha ou pendente'}), 400
        
        # Criar log
        log = LogMensagem(
            cliente_id=dados['cliente_id'],
            telefone_destino=dados['telefone_destino'],
            mensagem=dados['mensagem'],
            status=dados['status'],
            tipo_notificacao=dados.get('tipo_notificacao'),
            data_agendamento=datetime.fromisoformat(dados['data_agendamento']) if dados.get('data_agendamento') else None,
            data_envio=datetime.fromisoformat(dados['data_envio']) if dados.get('data_envio') else None,
            erro_detalhes=dados.get('erro_detalhes'),
            tentativas=dados.get('tentativas', 0)
        )
        
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Log criado com sucesso',
            'log': log.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@log_mensagem_bp.route('/logs/<int:log_id>', methods=['GET'])
def obter_log(log_id):
    """Obtém um log específico"""
    try:
        log = LogMensagem.query.get_or_404(log_id)
        log_dict = log.to_dict()
        
        # Incluir dados do cliente
        cliente = Cliente.query.get(log.cliente_id)
        if cliente:
            log_dict['cliente'] = cliente.to_dict()
        
        return jsonify({'log': log_dict})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@log_mensagem_bp.route('/logs/<int:log_id>', methods=['PUT'])
def atualizar_log(log_id):
    """Atualiza um log existente"""
    try:
        log = LogMensagem.query.get_or_404(log_id)
        dados = request.get_json()
        
        # Atualizar campos se fornecidos
        if 'status' in dados:
            if dados['status'] not in ['enviada', 'falha', 'pendente']:
                return jsonify({'erro': 'Status deve ser enviada, falha ou pendente'}), 400
            log.status = dados['status']
        
        if 'data_envio' in dados:
            if dados['data_envio']:
                log.data_envio = datetime.fromisoformat(dados['data_envio'])
            else:
                log.data_envio = None
        
        if 'erro_detalhes' in dados:
            log.erro_detalhes = dados['erro_detalhes']
        
        if 'tentativas' in dados:
            log.tentativas = dados['tentativas']
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Log atualizado com sucesso',
            'log': log.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@log_mensagem_bp.route('/logs/estatisticas', methods=['GET'])
def estatisticas_logs():
    """Retorna estatísticas dos logs de mensagem"""
    try:
        # Parâmetros de filtro
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        tipo_produto = request.args.get('tipo_produto')
        
        # Query base
        query = LogMensagem.query
        
        # Aplicar filtros de data
        if data_inicio:
            try:
                data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d')
                query = query.filter(LogMensagem.data_criacao >= data_inicio_obj)
            except ValueError:
                return jsonify({'erro': 'Formato de data_inicio inválido'}), 400
        
        if data_fim:
            try:
                data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d')
                data_fim_obj = data_fim_obj.replace(hour=23, minute=59, second=59)
                query = query.filter(LogMensagem.data_criacao <= data_fim_obj)
            except ValueError:
                return jsonify({'erro': 'Formato de data_fim inválido'}), 400
        
        # Filtrar por tipo de produto se especificado
        if tipo_produto:
            query = query.join(Cliente).filter(Cliente.tipo_produto == tipo_produto.upper())
        
        # Estatísticas por status
        total_mensagens = query.count()
        mensagens_enviadas = query.filter(LogMensagem.status == 'enviada').count()
        mensagens_falha = query.filter(LogMensagem.status == 'falha').count()
        mensagens_pendentes = query.filter(LogMensagem.status == 'pendente').count()
        
        # Estatísticas por tipo de notificação
        stats_tipo = {}
        tipos_notificacao = db.session.query(LogMensagem.tipo_notificacao).distinct().all()
        for (tipo,) in tipos_notificacao:
            if tipo:
                stats_tipo[tipo] = query.filter(LogMensagem.tipo_notificacao == tipo).count()
        
        # Estatísticas por produto
        stats_produto = {}
        if not tipo_produto:  # Se não filtrou por produto, mostrar todos
            produtos = db.session.query(Cliente.tipo_produto).distinct().all()
            for (produto,) in produtos:
                count = query.join(Cliente).filter(Cliente.tipo_produto == produto).count()
                stats_produto[produto] = count
        
        # Taxa de sucesso
        taxa_sucesso = (mensagens_enviadas / total_mensagens * 100) if total_mensagens > 0 else 0
        
        return jsonify({
            'total_mensagens': total_mensagens,
            'mensagens_enviadas': mensagens_enviadas,
            'mensagens_falha': mensagens_falha,
            'mensagens_pendentes': mensagens_pendentes,
            'taxa_sucesso': round(taxa_sucesso, 2),
            'estatisticas_por_tipo': stats_tipo,
            'estatisticas_por_produto': stats_produto
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@log_mensagem_bp.route('/logs/reenviar/<int:log_id>', methods=['POST'])
def reenviar_mensagem(log_id):
    """Marca uma mensagem para reenvio"""
    try:
        log = LogMensagem.query.get_or_404(log_id)
        
        # Só pode reenviar mensagens com falha
        if log.status != 'falha':
            return jsonify({'erro': 'Só é possível reenviar mensagens com falha'}), 400
        
        # Atualizar status para pendente
        log.status = 'pendente'
        log.tentativas += 1
        log.erro_detalhes = None
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Mensagem marcada para reenvio',
            'log': log.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

