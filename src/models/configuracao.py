from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Configuracao(db.Model):
    __tablename__ = 'configuracoes'
    
    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text)
    descricao = db.Column(db.String(255))
    tipo = db.Column(db.String(20), default='string')  # 'string', 'integer', 'boolean', 'json'
    categoria = db.Column(db.String(50))  # 'whatsapp', 'ia', 'sistema', 'notificacao'
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Configuracao {self.chave}>'

    def to_dict(self):
        return {
            'id': self.id,
            'chave': self.chave,
            'valor': self.get_valor_tipado(),
            'descricao': self.descricao,
            'tipo': self.tipo,
            'categoria': self.categoria,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None
        }

    def get_valor_tipado(self):
        """Retorna o valor convertido para o tipo apropriado"""
        if self.valor is None:
            return None
            
        if self.tipo == 'integer':
            try:
                return int(self.valor)
            except (ValueError, TypeError):
                return 0
        elif self.tipo == 'boolean':
            return self.valor.lower() in ('true', '1', 'yes', 'on') if isinstance(self.valor, str) else bool(self.valor)
        elif self.tipo == 'json':
            import json
            try:
                return json.loads(self.valor)
            except (json.JSONDecodeError, TypeError):
                return {}
        else:
            return self.valor

    def set_valor_tipado(self, valor):
        """Define o valor convertendo para string se necessário"""
        if self.tipo == 'json':
            import json
            self.valor = json.dumps(valor)
        else:
            self.valor = str(valor)

    @staticmethod
    def get_configuracao(chave, valor_padrao=None):
        """Método utilitário para buscar uma configuração"""
        config = Configuracao.query.filter_by(chave=chave).first()
        if config:
            return config.get_valor_tipado()
        return valor_padrao

    @staticmethod
    def set_configuracao(chave, valor, descricao=None, tipo='string', categoria='sistema'):
        """Método utilitário para definir uma configuração"""
        config = Configuracao.query.filter_by(chave=chave).first()
        if not config:
            config = Configuracao(chave=chave, tipo=tipo, categoria=categoria)
            if descricao:
                config.descricao = descricao
            db.session.add(config)
        
        config.set_valor_tipado(valor)
        config.data_atualizacao = datetime.utcnow()
        db.session.commit()
        return config

