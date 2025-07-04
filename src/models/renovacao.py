from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from src.models.user import db

class Renovacao(db.Model):
    __tablename__ = 'renovacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    data_renovacao = db.Column(db.Date, nullable=False, default=date.today)
    data_vencimento_anterior = db.Column(db.Date, nullable=False)
    data_vencimento_nova = db.Column(db.Date, nullable=False)
    dias_renovados = db.Column(db.Integer, nullable=False)  # 30, 60, 90, 180, 365
    valor_pago = db.Column(db.Float, nullable=False)
    observacoes = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Renovacao Cliente:{self.cliente_id} - {self.dias_renovados} dias>'

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'data_renovacao': self.data_renovacao.isoformat() if self.data_renovacao else None,
            'data_vencimento_anterior': self.data_vencimento_anterior.isoformat() if self.data_vencimento_anterior else None,
            'data_vencimento_nova': self.data_vencimento_nova.isoformat() if self.data_vencimento_nova else None,
            'dias_renovados': self.dias_renovados,
            'valor_pago': self.valor_pago,
            'observacoes': self.observacoes,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }

