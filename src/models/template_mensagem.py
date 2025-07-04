from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class TemplateMensagem(db.Model):
    __tablename__ = 'templates_mensagem'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo_produto = db.Column(db.String(10), nullable=False)  # 'IPTV', 'VPN', 'OUTROS', 'GERAL'
    tipo_template = db.Column(db.String(50), nullable=False)  # 'vencimento', 'renovacao', 'personalizada'
    conteudo = db.Column(db.Text, nullable=False)
    variaveis_disponiveis = db.Column(db.Text)  # JSON string com as variáveis disponíveis
    ativo = db.Column(db.Boolean, default=True)
    padrao = db.Column(db.Boolean, default=False)  # Se é o template padrão para o tipo
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<TemplateMensagem {self.nome} - {self.tipo_produto}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo_produto': self.tipo_produto,
            'tipo_template': self.tipo_template,
            'conteudo': self.conteudo,
            'variaveis_disponiveis': self.variaveis_disponiveis,
            'ativo': self.ativo,
            'padrao': self.padrao,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None
        }

    def processar_template(self, cliente, dias_vencimento=None):
        """Processa o template substituindo as variáveis pelos dados do cliente"""
        conteudo_processado = self.conteudo
        
        # Substituir variáveis básicas
        conteudo_processado = conteudo_processado.replace('{nome}', cliente.nome_completo)
        conteudo_processado = conteudo_processado.replace('{plano}', cliente.plano_contratado)
        conteudo_processado = conteudo_processado.replace('{valor}', f'R$ {cliente.valor_plano:.2f}')
        
        # Substituir dias para vencimento
        if dias_vencimento is not None:
            conteudo_processado = conteudo_processado.replace('{dias}', str(abs(dias_vencimento)))
        
        return conteudo_processado

