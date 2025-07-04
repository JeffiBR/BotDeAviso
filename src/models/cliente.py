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
    
    # Configurações de aviso
    aviso_ativo = db.Column(db.Boolean, default=True)
    dias_aviso_antecedencia = db.Column(db.Integer, default=3)  # Dias antes do vencimento
    horario_aviso = db.Column(db.Time)  # Horário específico para aviso
    
    # Sistema de comentários
    comentarios = db.Column(db.Text)  # Comentários sobre o cliente
    data_ultimo_comentario = db.Column(db.DateTime)
    
    # Controle de status
    ativo = db.Column(db.Boolean, default=True)
    ultima_mensagem_enviada = db.Column(db.DateTime)  # Controle para evitar spam
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
            'aviso_ativo': self.aviso_ativo,
            'dias_aviso_antecedencia': self.dias_aviso_antecedencia,
            'horario_aviso': self.horario_aviso.strftime('%H:%M') if self.horario_aviso else None,
            'comentarios': self.comentarios,
            'data_ultimo_comentario': self.data_ultimo_comentario.isoformat() if self.data_ultimo_comentario else None,
            'ativo': self.ativo,
            'ultima_mensagem_enviada': self.ultima_mensagem_enviada.isoformat() if self.ultima_mensagem_enviada else None,
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

    def precisa_aviso_antecedencia(self):
        """Verifica se precisa enviar aviso de antecedência"""
        if not self.aviso_ativo:
            return False
        
        dias = self.dias_para_vencimento()
        return dias is not None and dias == self.dias_aviso_antecedencia

    def foi_renovado_recentemente(self):
        """Verifica se foi renovado nas últimas 24 horas"""
        from datetime import datetime, timedelta
        
        if not self.renovacoes:
            return False
        
        ultima_renovacao = max(self.renovacoes, key=lambda r: r.data_renovacao)
        limite = datetime.now().date() - timedelta(days=1)
        
        return ultima_renovacao.data_renovacao >= limite

    def pode_enviar_mensagem(self):
        """Verifica se pode enviar mensagem (evita spam)"""
        from datetime import datetime, timedelta
        
        if not self.ultima_mensagem_enviada:
            return True
        
        # Não enviar se já enviou nas últimas 2 horas
        limite = datetime.utcnow() - timedelta(hours=2)
        return self.ultima_mensagem_enviada <= limite

    def atualizar_comentario(self, novo_comentario):
        """Atualiza o comentário do cliente"""
        from datetime import datetime
        
        self.comentarios = novo_comentario
        self.data_ultimo_comentario = datetime.utcnow()
        self.data_atualizacao = datetime.utcnow()

