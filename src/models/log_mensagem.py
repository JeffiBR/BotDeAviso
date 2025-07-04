from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class LogMensagem(db.Model):
    __tablename__ = 'logs_mensagem'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    telefone_destino = db.Column(db.String(20), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'enviada', 'falha', 'pendente'
    tipo_notificacao = db.Column(db.String(50))  # 'vencimento', 'renovacao', 'personalizada'
    data_agendamento = db.Column(db.DateTime)
    data_envio = db.Column(db.DateTime)
    erro_detalhes = db.Column(db.Text)
    tentativas = db.Column(db.Integer, default=0)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<LogMensagem Cliente:{self.cliente_id} - {self.status}>'

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'telefone_destino': self.telefone_destino,
            'mensagem': self.mensagem,
            'status': self.status,
            'tipo_notificacao': self.tipo_notificacao,
            'data_agendamento': self.data_agendamento.isoformat() if self.data_agendamento else None,
            'data_envio': self.data_envio.isoformat() if self.data_envio else None,
            'erro_detalhes': self.erro_detalhes,
            'tentativas': self.tentativas,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }

