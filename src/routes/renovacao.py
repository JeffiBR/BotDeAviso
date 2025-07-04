from flask import Blueprint, request, jsonify
from datetime import datetime, date
from src.models.user import db
from src.models.renovacao import Renovacao
from src.models.cliente import Cliente
from sqlalchemy import and_, func

renovacao_bp = Blueprint('renovacao', __name__)

@renovacao_bp.route('/renovacoes', methods=['GET'])
def listar_renovacoes():
    """Lista todas as renovações com filtros opcionais"""
    try:
        # Parâmetros de filtro
        cliente_id = request.args.get('cliente_id', type=int)
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        dias_renovados = request.args.get('dias_renovados', type=int)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # Query base
        query = Renovacao.query
        
        # Aplicar filtros
        if cliente_id:
            query = query.filter(Renovacao.cliente_id == cliente_id)
        
        if data_inicio:
            try:
                data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                query = query.filter(Renovacao.data_renovacao >= data_inicio_obj)
            except ValueError:
                return jsonify({'erro': 'Formato de data_inicio inválido. Use YYYY-MM-DD'}), 400
        
        if data_fim:
            try:
                data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
                query = query.filter(Renovacao.data_renovacao <= data_fim_obj)
            except ValueError:
                return jsonify({'erro': 'Formato de data_fim inválido. Use YYYY-MM-DD'}), 400
        
        if dias_renovados:
            query = query.filter(Renovacao.dias_renovados == dias_renovados)
        
        # Ordenar por data de renovação (mais recentes primeiro)
        query = query.order_by(Renovacao.data_renovacao.desc())
        
        # Paginação
        renovacoes_paginadas = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Incluir dados do cliente nas renovações
        renovacoes_com_cliente = []
        for renovacao in renovacoes_paginadas.items:
            renovacao_dict = renovacao.to_dict()
            cliente = Cliente.query.get(renovacao.cliente_id)
            if cliente:
                renovacao_dict['cliente_nome'] = cliente.nome_completo
                renovacao_dict['cliente_tipo_produto'] = cliente.tipo_produto
                renovacao_dict['cliente_plano'] = cliente.plano_contratado
            renovacoes_com_cliente.append(renovacao_dict)
        
        return jsonify({
            'renovacoes': renovacoes_com_cliente,
            'total': renovacoes_paginadas.total,
            'pages': renovacoes_paginadas.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': renovacoes_paginadas.has_next,
            'has_prev': renovacoes_paginadas.has_prev
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@renovacao_bp.route('/renovacoes/<int:renovacao_id>', methods=['GET'])
def obter_renovacao(renovacao_id):
    """Obtém uma renovação específica"""
    try:
        renovacao = Renovacao.query.get_or_404(renovacao_id)
        renovacao_dict = renovacao.to_dict()
        
        # Incluir dados do cliente
        cliente = Cliente.query.get(renovacao.cliente_id)
        if cliente:
            renovacao_dict['cliente'] = cliente.to_dict()
        
        return jsonify({'renovacao': renovacao_dict})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@renovacao_bp.route('/renovacoes/<int:renovacao_id>', methods=['PUT'])
def atualizar_renovacao(renovacao_id):
    """Atualiza uma renovação existente"""
    try:
        renovacao = Renovacao.query.get_or_404(renovacao_id)
        dados = request.get_json()
        
        # Atualizar campos se fornecidos
        if 'valor_pago' in dados:
            renovacao.valor_pago = float(dados['valor_pago'])
        
        if 'observacoes' in dados:
            renovacao.observacoes = dados['observacoes']
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Renovação atualizada com sucesso',
            'renovacao': renovacao.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@renovacao_bp.route('/renovacoes/<int:renovacao_id>', methods=['DELETE'])
def deletar_renovacao(renovacao_id):
    """Deleta uma renovação (cuidado: isso pode afetar o histórico)"""
    try:
        renovacao = Renovacao.query.get_or_404(renovacao_id)
        
        # Verificar se é a renovação mais recente do cliente
        renovacao_mais_recente = Renovacao.query.filter_by(
            cliente_id=renovacao.cliente_id
        ).order_by(Renovacao.data_renovacao.desc()).first()
        
        if renovacao_mais_recente and renovacao_mais_recente.id == renovacao.id:
            # Se for a mais recente, reverter a data de vencimento do cliente
            cliente = Cliente.query.get(renovacao.cliente_id)
            if cliente:
                cliente.data_vencimento = renovacao.data_vencimento_anterior
                cliente.data_atualizacao = datetime.utcnow()
        
        db.session.delete(renovacao)
        db.session.commit()
        
        return jsonify({'mensagem': 'Renovação deletada com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@renovacao_bp.route('/renovacoes/estatisticas', methods=['GET'])
def estatisticas_renovacoes():
    """Retorna estatísticas das renovações"""
    try:
        # Parâmetros de filtro
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        tipo_produto = request.args.get('tipo_produto')
        
        # Query base
        query = Renovacao.query
        
        # Aplicar filtros de data
        if data_inicio:
            try:
                data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                query = query.filter(Renovacao.data_renovacao >= data_inicio_obj)
            except ValueError:
                return jsonify({'erro': 'Formato de data_inicio inválido'}), 400
        
        if data_fim:
            try:
                data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
                query = query.filter(Renovacao.data_renovacao <= data_fim_obj)
            except ValueError:
                return jsonify({'erro': 'Formato de data_fim inválido'}), 400
        
        # Filtrar por tipo de produto se especificado
        if tipo_produto:
            query = query.join(Cliente).filter(Cliente.tipo_produto == tipo_produto.upper())
        
        # Estatísticas gerais
        total_renovacoes = query.count()
        receita_total = query.with_entities(func.sum(Renovacao.valor_pago)).scalar() or 0
        
        # Estatísticas por período de renovação
        stats_periodo = {}
        periodos = [30, 60, 90, 180, 365]
        for periodo in periodos:
            count = query.filter(Renovacao.dias_renovados == periodo).count()
            receita = query.filter(Renovacao.dias_renovados == periodo).with_entities(func.sum(Renovacao.valor_pago)).scalar() or 0
            stats_periodo[f'{periodo}_dias'] = {
                'quantidade': count,
                'receita': float(receita)
            }
        
        # Estatísticas por produto
        stats_produto = {}
        if not tipo_produto:  # Se não filtrou por produto, mostrar todos
            produtos = db.session.query(Cliente.tipo_produto).distinct().all()
            for (produto,) in produtos:
                count = query.join(Cliente).filter(Cliente.tipo_produto == produto).count()
                receita = query.join(Cliente).filter(Cliente.tipo_produto == produto).with_entities(func.sum(Renovacao.valor_pago)).scalar() or 0
                stats_produto[produto] = {
                    'quantidade': count,
                    'receita': float(receita)
                }
        
        # Renovações por mês (últimos 12 meses)
        from datetime import timedelta
        from dateutil.relativedelta import relativedelta
        
        renovacoes_por_mes = []
        data_atual = date.today()
        
        for i in range(12):
            inicio_mes = (data_atual - relativedelta(months=i)).replace(day=1)
            if i == 0:
                fim_mes = data_atual
            else:
                fim_mes = inicio_mes.replace(day=28) + timedelta(days=4)
                fim_mes = fim_mes - timedelta(days=fim_mes.day)
            
            count = query.filter(
                and_(
                    Renovacao.data_renovacao >= inicio_mes,
                    Renovacao.data_renovacao <= fim_mes
                )
            ).count()
            
            receita = query.filter(
                and_(
                    Renovacao.data_renovacao >= inicio_mes,
                    Renovacao.data_renovacao <= fim_mes
                )
            ).with_entities(func.sum(Renovacao.valor_pago)).scalar() or 0
            
            renovacoes_por_mes.append({
                'mes': inicio_mes.strftime('%Y-%m'),
                'mes_nome': inicio_mes.strftime('%B %Y'),
                'quantidade': count,
                'receita': float(receita)
            })
        
        # Reverter para ordem cronológica
        renovacoes_por_mes.reverse()
        
        # Ticket médio
        ticket_medio = (receita_total / total_renovacoes) if total_renovacoes > 0 else 0
        
        return jsonify({
            'total_renovacoes': total_renovacoes,
            'receita_total': float(receita_total),
            'ticket_medio': round(float(ticket_medio), 2),
            'estatisticas_por_periodo': stats_periodo,
            'estatisticas_por_produto': stats_produto,
            'renovacoes_por_mes': renovacoes_por_mes
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@renovacao_bp.route('/renovacoes/cliente/<int:cliente_id>', methods=['GET'])
def historico_renovacoes_cliente(cliente_id):
    """Retorna o histórico de renovações de um cliente específico"""
    try:
        # Verificar se cliente existe
        cliente = Cliente.query.get_or_404(cliente_id)
        
        # Buscar renovações do cliente
        renovacoes = Renovacao.query.filter_by(
            cliente_id=cliente_id
        ).order_by(Renovacao.data_renovacao.desc()).all()
        
        # Calcular estatísticas do cliente
        total_renovacoes = len(renovacoes)
        total_pago = sum(r.valor_pago for r in renovacoes)
        
        # Período de renovação mais comum
        if renovacoes:
            periodos = [r.dias_renovados for r in renovacoes]
            periodo_mais_comum = max(set(periodos), key=periodos.count)
        else:
            periodo_mais_comum = None
        
        return jsonify({
            'cliente': cliente.to_dict(),
            'renovacoes': [r.to_dict() for r in renovacoes],
            'estatisticas': {
                'total_renovacoes': total_renovacoes,
                'total_pago': float(total_pago),
                'periodo_mais_comum': periodo_mais_comum,
                'ticket_medio': round(float(total_pago / total_renovacoes), 2) if total_renovacoes > 0 else 0
            }
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

