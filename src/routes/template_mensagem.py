from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.user import db
from src.models.template_mensagem import TemplateMensagem
import json

template_mensagem_bp = Blueprint('template_mensagem', __name__)

@template_mensagem_bp.route('/templates', methods=['GET'])
def listar_templates():
    """Lista todos os templates de mensagem com filtros opcionais"""
    try:
        # Parâmetros de filtro
        tipo_produto = request.args.get('tipo_produto')
        tipo_template = request.args.get('tipo_template')
        ativo = request.args.get('ativo')
        
        # Query base
        query = TemplateMensagem.query
        
        # Aplicar filtros
        if tipo_produto:
            query = query.filter(TemplateMensagem.tipo_produto == tipo_produto.upper())
        
        if tipo_template:
            query = query.filter(TemplateMensagem.tipo_template == tipo_template)
        
        if ativo is not None:
            ativo_bool = ativo.lower() in ('true', '1', 'yes')
            query = query.filter(TemplateMensagem.ativo == ativo_bool)
        
        templates = query.order_by(TemplateMensagem.nome.asc()).all()
        
        return jsonify({
            'templates': [template.to_dict() for template in templates],
            'total': len(templates)
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@template_mensagem_bp.route('/templates', methods=['POST'])
def criar_template():
    """Cria um novo template de mensagem"""
    try:
        dados = request.get_json()
        
        # Validações obrigatórias
        campos_obrigatorios = ['nome', 'tipo_produto', 'tipo_template', 'conteudo']
        
        for campo in campos_obrigatorios:
            if campo not in dados or not dados[campo]:
                return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
        
        # Validar tipo de produto
        if dados['tipo_produto'].upper() not in ['IPTV', 'VPN', 'OUTROS', 'GERAL']:
            return jsonify({'erro': 'Tipo de produto deve ser IPTV, VPN, OUTROS ou GERAL'}), 400
        
        # Validar tipo de template
        if dados['tipo_template'] not in ['vencimento', 'renovacao', 'personalizada']:
            return jsonify({'erro': 'Tipo de template deve ser vencimento, renovacao ou personalizada'}), 400
        
        # Processar variáveis disponíveis
        variaveis_disponiveis = dados.get('variaveis_disponiveis', ['nome', 'plano', 'valor', 'dias'])
        if isinstance(variaveis_disponiveis, list):
            variaveis_disponiveis = json.dumps(variaveis_disponiveis)
        
        # Criar template
        template = TemplateMensagem(
            nome=dados['nome'],
            tipo_produto=dados['tipo_produto'].upper(),
            tipo_template=dados['tipo_template'],
            conteudo=dados['conteudo'],
            variaveis_disponiveis=variaveis_disponiveis,
            ativo=dados.get('ativo', True),
            padrao=dados.get('padrao', False)
        )
        
        # Se for marcado como padrão, desmarcar outros padrões do mesmo tipo
        if template.padrao:
            TemplateMensagem.query.filter_by(
                tipo_produto=template.tipo_produto,
                tipo_template=template.tipo_template,
                padrao=True
            ).update({'padrao': False})
        
        db.session.add(template)
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Template criado com sucesso',
            'template': template.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@template_mensagem_bp.route('/templates/<int:template_id>', methods=['GET'])
def obter_template(template_id):
    """Obtém um template específico"""
    try:
        template = TemplateMensagem.query.get_or_404(template_id)
        return jsonify({'template': template.to_dict()})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@template_mensagem_bp.route('/templates/<int:template_id>', methods=['PUT'])
def atualizar_template(template_id):
    """Atualiza um template existente"""
    try:
        template = TemplateMensagem.query.get_or_404(template_id)
        dados = request.get_json()
        
        # Atualizar campos se fornecidos
        if 'nome' in dados:
            template.nome = dados['nome']
        
        if 'tipo_produto' in dados:
            if dados['tipo_produto'].upper() not in ['IPTV', 'VPN', 'OUTROS', 'GERAL']:
                return jsonify({'erro': 'Tipo de produto deve ser IPTV, VPN, OUTROS ou GERAL'}), 400
            template.tipo_produto = dados['tipo_produto'].upper()
        
        if 'tipo_template' in dados:
            if dados['tipo_template'] not in ['vencimento', 'renovacao', 'personalizada']:
                return jsonify({'erro': 'Tipo de template deve ser vencimento, renovacao ou personalizada'}), 400
            template.tipo_template = dados['tipo_template']
        
        if 'conteudo' in dados:
            template.conteudo = dados['conteudo']
        
        if 'variaveis_disponiveis' in dados:
            variaveis = dados['variaveis_disponiveis']
            if isinstance(variaveis, list):
                variaveis = json.dumps(variaveis)
            template.variaveis_disponiveis = variaveis
        
        if 'ativo' in dados:
            template.ativo = dados['ativo']
        
        if 'padrao' in dados:
            template.padrao = dados['padrao']
            # Se for marcado como padrão, desmarcar outros padrões do mesmo tipo
            if template.padrao:
                TemplateMensagem.query.filter(
                    TemplateMensagem.id != template.id,
                    TemplateMensagem.tipo_produto == template.tipo_produto,
                    TemplateMensagem.tipo_template == template.tipo_template,
                    TemplateMensagem.padrao == True
                ).update({'padrao': False})
        
        template.data_atualizacao = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'mensagem': 'Template atualizado com sucesso',
            'template': template.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@template_mensagem_bp.route('/templates/<int:template_id>', methods=['DELETE'])
def deletar_template(template_id):
    """Deleta um template"""
    try:
        template = TemplateMensagem.query.get_or_404(template_id)
        
        # Verificar se há clientes usando este template
        from src.models.cliente import Cliente
        clientes_usando = Cliente.query.filter_by(template_mensagem_id=template_id).count()
        
        if clientes_usando > 0:
            return jsonify({
                'erro': f'Não é possível deletar o template. {clientes_usando} cliente(s) estão usando este template.'
            }), 400
        
        db.session.delete(template)
        db.session.commit()
        
        return jsonify({'mensagem': 'Template deletado com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@template_mensagem_bp.route('/templates/<int:template_id>/preview', methods=['POST'])
def preview_template(template_id):
    """Gera uma prévia do template com dados de exemplo"""
    try:
        template = TemplateMensagem.query.get_or_404(template_id)
        dados = request.get_json()
        
        # Dados de exemplo ou fornecidos
        nome = dados.get('nome', 'João Silva')
        plano = dados.get('plano', 'Plano Premium')
        valor = dados.get('valor', 29.90)
        dias = dados.get('dias', 3)
        
        # Criar objeto cliente fictício para preview
        class ClienteFicticio:
            def __init__(self, nome, plano, valor):
                self.nome_completo = nome
                self.plano_contratado = plano
                self.valor_plano = valor
        
        cliente_ficticio = ClienteFicticio(nome, plano, valor)
        mensagem_processada = template.processar_template(cliente_ficticio, dias)
        
        return jsonify({
            'template_original': template.conteudo,
            'mensagem_processada': mensagem_processada,
            'variaveis_usadas': {
                'nome': nome,
                'plano': plano,
                'valor': f'R$ {valor:.2f}',
                'dias': str(dias)
            }
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@template_mensagem_bp.route('/templates/padrao/<tipo_produto>/<tipo_template>', methods=['GET'])
def obter_template_padrao(tipo_produto, tipo_template):
    """Obtém o template padrão para um tipo de produto e template específico"""
    try:
        if tipo_produto.upper() not in ['IPTV', 'VPN', 'OUTROS', 'GERAL']:
            return jsonify({'erro': 'Tipo de produto inválido'}), 400
        
        if tipo_template not in ['vencimento', 'renovacao', 'personalizada']:
            return jsonify({'erro': 'Tipo de template inválido'}), 400
        
        # Buscar template padrão específico primeiro
        template = TemplateMensagem.query.filter_by(
            tipo_produto=tipo_produto.upper(),
            tipo_template=tipo_template,
            padrao=True,
            ativo=True
        ).first()
        
        # Se não encontrar, buscar template geral
        if not template:
            template = TemplateMensagem.query.filter_by(
                tipo_produto='GERAL',
                tipo_template=tipo_template,
                padrao=True,
                ativo=True
            ).first()
        
        if not template:
            return jsonify({'erro': 'Template padrão não encontrado'}), 404
        
        return jsonify({'template': template.to_dict()})
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

