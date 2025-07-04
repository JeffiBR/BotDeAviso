from flask import Blueprint, request, jsonify
from datetime import datetime, date, time
from src.models.user import db
from src.models.cliente import Cliente
from src.models.template_mensagem import TemplateMensagem
from src.models.renovacao import Renovacao
from sqlalchemy import or_, and_

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    """Lista todos os clientes com filtros opcionais"""
    try:
        # Parâmetros de filtro
        tipo_produto = request.args.get('tipo_produto')
        ativo = request.args.get('ativo')
        vencimento_ate = request.args.get('vencimento_ate')
        
        # Query base
        query = Cliente.query
        
        # Aplicar filtros
        if tipo_produto:
            query = query.filter(Cliente.tipo_produto == tipo_produto.upper())
        
        if ativo is not None:
            ativo_bool = ativo.lower() in ('true', '1', 'yes')
            query = query.filter(Cliente.ativo == ativo_bool)
        
        if vencimento_ate:
            try:
                data_limite = datetime.strptime(vencimento_ate, '%Y-%m-%d').date()
                query = query.filter(Cliente.data_vencimento <= data_limite)
            except ValueError:
                return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        
        clientes = query.order_by(Cliente.data_vencimento.asc()).all()
        
        return jsonify({
            'clientes': [cliente.to_dict() for cliente in clientes],
            'total': len(clientes)
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    """Cria um novo cliente"""
    try:
        dados = request.get_json()
        
        # Validações obrigatórias
        campos_obrigatorios = ['nome_completo', 'telefone', 'tipo_produto', 
                              'plano_contratado', 'valor_plano', 'data_vencimento', 'horario_envio']
        
        for campo in campos_obrigatorios:
            if campo not in dados or not dados[campo]:
                return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
        
        # Validar tipo de produto
        if dados['tipo_produto'].upper() not in ['IPTV', 'VPN', 'OUTROS']:
            return jsonify({'erro': 'Tipo de produto deve ser IPTV, VPN ou OUTROS'}), 400
        
        # Converter datas
        try:
            data_vencimento = datetime.strptime(dados['data_vencimento'], '%Y-%m-%d').date()
            horario_envio = datetime.strptime(dados['horario_envio'], '%H:%M').time()
            
            # Horário de aviso (opcional)
            horario_aviso = None
            if dados.get('horario_aviso'):
                horario_aviso = datetime.strptime(dados['horario_aviso'], '%H:%M').time()
                
        except ValueError:
            return jsonify({'erro': 'Formato de data/hora inválido'}), 400
        
        # Validar template de mensagem se fornecido
        template_mensagem_id = dados.get('template_mensagem_id')
        if template_mensagem_id:
            template = TemplateMensagem.query.get(template_mensagem_id)
            if not template:
                return jsonify({'erro': 'Template de mensagem não encontrado'}), 400
        
        # Criar cliente
        cliente = Cliente(
            nome_completo=dados['nome_completo'],
            telefone=dados['telefone'],
            tipo_produto=dados['tipo_produto'].upper(),
            plano_contratado=dados['plano_contratado'],
            valor_plano=float(dados['valor_plano']),
            data_vencimento=data_vencimento,
            horario_envio=horario_envio,
            template_mensagem_id=template_mensagem_id,
            mensagem_personalizada=dados.get('mensagem_personalizada'),
            aviso_ativo=dados.get('aviso_ativo', True),
            dias_aviso_antecedencia=dados.get('dias_aviso_antecedencia', 3),
            horario_aviso=horario_aviso,
            comentarios=dados.get('comentarios'),
            ativo=dados.get('ativo', True)
        )
        
        # Atualizar data do comentário se fornecido
        if dados.get('comentarios'):
            cliente.data_ultimo_comentario = datetime.utcnow()
        
        db.session.add(cliente)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Cliente criado com sucesso',
            'cliente': cliente.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['GET'])
def obter_cliente(cliente_id):
    """Obtém um cliente específico"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        return jsonify({'cliente': cliente.to_dict()})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['PUT'])
def atualizar_cliente(cliente_id):
    """Atualiza um cliente existente"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        dados = request.get_json()
        
        # Atualizar campos se fornecidos
        if 'nome_completo' in dados:
            cliente.nome_completo = dados['nome_completo']
        
        if 'telefone' in dados:
            cliente.telefone = dados['telefone']
        
        if 'tipo_produto' in dados:
            if dados['tipo_produto'].upper() not in ['IPTV', 'VPN', 'OUTROS']:
                return jsonify({'erro': 'Tipo de produto deve ser IPTV, VPN ou OUTROS'}), 400
            cliente.tipo_produto = dados['tipo_produto'].upper()
        
        if 'plano_contratado' in dados:
            cliente.plano_contratado = dados['plano_contratado']
        
        if 'valor_plano' in dados:
            cliente.valor_plano = float(dados['valor_plano'])
        
        if 'data_vencimento' in dados:
            try:
                cliente.data_vencimento = datetime.strptime(dados['data_vencimento'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'erro': 'Formato de data inválido'}), 400
        
        if 'horario_envio' in dados:
            try:
                cliente.horario_envio = datetime.strptime(dados['horario_envio'], '%H:%M').time()
            except ValueError:
                return jsonify({'erro': 'Formato de horário inválido'}), 400
        
        if 'template_mensagem_id' in dados:
            template_mensagem_id = dados['template_mensagem_id']
            if template_mensagem_id:
                template = TemplateMensagem.query.get(template_mensagem_id)
                if not template:
                    return jsonify({'erro': 'Template de mensagem não encontrado'}), 400
            cliente.template_mensagem_id = template_mensagem_id
        
        if 'mensagem_personalizada' in dados:
            cliente.mensagem_personalizada = dados['mensagem_personalizada']
        
        if 'ativo' in dados:
            cliente.ativo = dados['ativo']
        
        # Atualizar configurações de aviso
        if 'aviso_ativo' in dados:
            cliente.aviso_ativo = dados['aviso_ativo']
        
        if 'dias_aviso_antecedencia' in dados:
            cliente.dias_aviso_antecedencia = dados['dias_aviso_antecedencia']
        
        if 'horario_aviso' in dados:
            if dados['horario_aviso']:
                try:
                    cliente.horario_aviso = datetime.strptime(dados['horario_aviso'], '%H:%M').time()
                except ValueError:
                    return jsonify({'erro': 'Formato de horário de aviso inválido'}), 400
            else:
                cliente.horario_aviso = None
        
        # Atualizar comentários
        if 'comentarios' in dados:
            cliente.atualizar_comentario(dados['comentarios'])
        
        cliente.data_atualizacao = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Cliente atualizado com sucesso',
            'cliente': cliente.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def deletar_cliente(cliente_id):
    """Deleta um cliente"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        db.session.delete(cliente)
        db.session.commit()
        
        return jsonify({'mensagem': 'Cliente deletado com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>/renovar', methods=['POST'])
def renovar_cliente(cliente_id):
    """Renova um cliente por um período específico"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        dados = request.get_json()
        
        # Validar dias de renovação
        dias_renovacao = dados.get('dias_renovacao')
        if dias_renovacao not in [30, 60, 90, 180, 365]:
            return jsonify({'erro': 'Dias de renovação deve ser 30, 60, 90, 180 ou 365'}), 400
        
        valor_pago = dados.get('valor_pago', cliente.valor_plano)
        observacoes = dados.get('observacoes', '')
        
        # Salvar data de vencimento anterior
        data_vencimento_anterior = cliente.data_vencimento
        
        # Calcular nova data de vencimento
        from datetime import timedelta
        if cliente.data_vencimento < date.today():
            # Se já vencido, renovar a partir de hoje
            nova_data_vencimento = date.today() + timedelta(days=dias_renovacao)
        else:
            # Se ainda não vencido, renovar a partir da data atual de vencimento
            nova_data_vencimento = cliente.data_vencimento + timedelta(days=dias_renovacao)
        
        # Atualizar cliente
        cliente.data_vencimento = nova_data_vencimento
        cliente.ativo = True
        cliente.data_atualizacao = datetime.utcnow()
        
        # Criar registro de renovação
        renovacao = Renovacao(
            cliente_id=cliente.id,
            data_vencimento_anterior=data_vencimento_anterior,
            data_vencimento_nova=nova_data_vencimento,
            dias_renovados=dias_renovacao,
            valor_pago=valor_pago,
            observacoes=observacoes
        )
        
        db.session.add(renovacao)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Cliente renovado com sucesso',
            'cliente': cliente.to_dict(),
            'renovacao': renovacao.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/dashboard/<tipo_produto>', methods=['GET'])
def dashboard_clientes(tipo_produto):
    """Retorna dados do dashboard para um tipo de produto específico"""
    try:
        if tipo_produto.upper() not in ['IPTV', 'VPN', 'OUTROS']:
            return jsonify({'erro': 'Tipo de produto inválido'}), 400
        
        # Clientes ativos
        clientes_ativos = Cliente.query.filter_by(
            tipo_produto=tipo_produto.upper(), 
            ativo=True
        ).count()
        
        # Clientes vencidos (data de vencimento < hoje)
        clientes_vencidos = Cliente.query.filter(
            and_(
                Cliente.tipo_produto == tipo_produto.upper(),
                Cliente.ativo == True,
                Cliente.data_vencimento < date.today()
            )
        ).count()
        
        # Clientes que vencem nos próximos 7 dias
        from datetime import timedelta
        data_limite = date.today() + timedelta(days=7)
        clientes_vencendo = Cliente.query.filter(
            and_(
                Cliente.tipo_produto == tipo_produto.upper(),
                Cliente.ativo == True,
                Cliente.data_vencimento >= date.today(),
                Cliente.data_vencimento <= data_limite
            )
        ).count()
        
        # Receita total
        receita_total = db.session.query(db.func.sum(Cliente.valor_plano)).filter(
            and_(
                Cliente.tipo_produto == tipo_produto.upper(),
                Cliente.ativo == True
            )
        ).scalar() or 0
        
        # Renovações do mês atual
        primeiro_dia_mes = date.today().replace(day=1)
        renovacoes_mes = Renovacao.query.join(Cliente).filter(
            and_(
                Cliente.tipo_produto == tipo_produto.upper(),
                Renovacao.data_renovacao >= primeiro_dia_mes
            )
        ).count()
        
        return jsonify({
            'tipo_produto': tipo_produto.upper(),
            'clientes_ativos': clientes_ativos,
            'clientes_vencidos': clientes_vencidos,
            'clientes_vencendo': clientes_vencendo,
            'receita_total': receita_total,
            'renovacoes_mes': renovacoes_mes
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>/comentarios', methods=['PUT'])
def atualizar_comentario_cliente(cliente_id):
    """Atualiza apenas o comentário de um cliente"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        dados = request.get_json()
        
        if 'comentarios' not in dados:
            return jsonify({'erro': 'Campo comentarios é obrigatório'}), 400
        
        cliente.atualizar_comentario(dados['comentarios'])
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Comentário atualizado com sucesso',
            'comentarios': cliente.comentarios,
            'data_ultimo_comentario': cliente.data_ultimo_comentario.isoformat() if cliente.data_ultimo_comentario else None
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>/comentarios', methods=['DELETE'])
def deletar_comentario_cliente(cliente_id):
    """Remove o comentário de um cliente"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        
        cliente.comentarios = None
        cliente.data_ultimo_comentario = None
        cliente.data_atualizacao = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'mensagem': 'Comentário removido com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/avisos-pendentes', methods=['GET'])
def clientes_avisos_pendentes():
    """Retorna clientes que precisam receber avisos hoje"""
    try:
        from datetime import date, time
        
        hoje = date.today()
        clientes_para_aviso = []
        
        # Buscar todos os clientes ativos
        clientes = Cliente.query.filter_by(ativo=True).all()
        
        for cliente in clientes:
            # Verificar se precisa de aviso de antecedência
            if cliente.precisa_aviso_antecedencia() and not cliente.foi_renovado_recentemente():
                if cliente.pode_enviar_mensagem():
                    clientes_para_aviso.append({
                        'cliente': cliente.to_dict(),
                        'tipo_aviso': 'antecedencia',
                        'dias_restantes': cliente.dias_para_vencimento(),
                        'horario_envio': cliente.horario_aviso.strftime('%H:%M') if cliente.horario_aviso else cliente.horario_envio.strftime('%H:%M')
                    })
            
            # Verificar se vence hoje
            elif cliente.vence_hoje() and not cliente.foi_renovado_recentemente():
                if cliente.pode_enviar_mensagem():
                    clientes_para_aviso.append({
                        'cliente': cliente.to_dict(),
                        'tipo_aviso': 'vencimento',
                        'dias_restantes': 0,
                        'horario_envio': cliente.horario_envio.strftime('%H:%M')
                    })
        
        # Ordenar por horário de envio
        clientes_para_aviso.sort(key=lambda x: x['horario_envio'])
        
        return jsonify({
            'clientes_para_aviso': clientes_para_aviso,
            'total': len(clientes_para_aviso),
            'data_processamento': hoje.isoformat()
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/marcar-mensagem-enviada/<int:cliente_id>', methods=['POST'])
def marcar_mensagem_enviada(cliente_id):
    """Marca que uma mensagem foi enviada para o cliente"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        
        cliente.ultima_mensagem_enviada = datetime.utcnow()
        cliente.data_atualizacao = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Mensagem marcada como enviada',
            'ultima_mensagem_enviada': cliente.ultima_mensagem_enviada.isoformat()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

