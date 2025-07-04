from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    tipo_produto = db.Column(db.String(10), nullable=False)  # 'IPTV', 'VPN' ou 'OUTROS'
    plano_contratado = db.Column(db.String(100), nullable=False)
    valor_plano = db.Column(db.Float, nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    horario_envio = db.Column(db.Time, nullable=False)
    template_mensagem_id = db.Column(db.Integer, db.ForeignKey('templates_mensagem.id'))
    mensagem_personalizada = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    template_mensagem = db.relationship('TemplateMensagem', backref='clientes', lazy=True)
    renovacoes = db.relationship('Renovacao', backref='cliente', lazy=True, cascade='all, delete-orphan')
    logs_mensagem = db.relationship('LogMensagem', backref='cliente', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Cliente {self.nome_completo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'telefone': self.telefone,
            'tipo_produto': self.tipo_produto,
            'plano_contratado': self.plano_contratado,
            'valor_plano': self.valor_plano,
            'data_vencimento': self.data_vencimento.isoformat() if self.data_vencimento else None,
            'horario_envio': self.horario_envio.strftime('%H:%M') if self.horario_envio else None,
            'template_mensagem_id': self.template_mensagem_id,
            'mensagem_personalizada': self.mensagem_personalizada,
            'ativo': self.ativo,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None
        }

    def dias_para_vencimento(self):
        """Calcula quantos dias faltam para o vencimento"""
        from datetime import date
        if self.data_vencimento:
            delta = self.data_vencimento - date.today()
            return delta.days
        return None

    def esta_vencido(self):
        """Verifica se o cliente está vencido"""
        dias = self.dias_para_vencimento()
        return dias is not None and dias < 0

    def vence_hoje(self):
        """Verifica se o cliente vence hoje"""
        dias = self.dias_para_vencimento()
        return dias is not None and dias == 0

