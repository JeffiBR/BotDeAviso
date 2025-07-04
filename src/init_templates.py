"""
Script para inicializar templates de mensagem padrão
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db
from src.models.template_mensagem import TemplateMensagem
from src.main import app
import json

def criar_templates_padrao():
    """Cria templates de mensagem padrão para o sistema"""
    
    templates_padrao = [
        # Templates para IPTV
        {
            'nome': 'Vencimento IPTV - 7 dias',
            'tipo_produto': 'IPTV',
            'tipo_template': 'vencimento',
            'conteudo': '''Olá {nome}! 📺

Seu plano {plano} vence em {dias} dias.

💰 Valor: {valor}
📅 Para manter seu acesso sem interrupções, renove antes do vencimento.

Entre em contato para renovar! 👍''',
            'variaveis_disponiveis': json.dumps(['nome', 'plano', 'valor', 'dias']),
            'padrao': True
        },
        {
            'nome': 'Vencimento IPTV - Hoje',
            'tipo_produto': 'IPTV',
            'tipo_template': 'vencimento',
            'conteudo': '''🚨 ATENÇÃO {nome}!

Seu plano {plano} vence HOJE!

💰 Valor: {valor}
⚠️ Renove agora para não perder o acesso aos canais.

Entre em contato urgente! 📞''',
            'variaveis_disponiveis': json.dumps(['nome', 'plano', 'valor', 'dias'])
        },
        {
            'nome': 'Renovação IPTV Confirmada',
            'tipo_produto': 'IPTV',
            'tipo_template': 'renovacao',
            'conteudo': '''✅ Renovação Confirmada!

Olá {nome}, sua renovação foi processada com sucesso!

📺 Plano: {plano}
💰 Valor pago: {valor}
📅 Válido por mais {dias} dias

Obrigado pela confiança! 🙏''',
            'variaveis_disponiveis': json.dumps(['nome', 'plano', 'valor', 'dias'])
        },
        
        # Templates para VPN
        {
            'nome': 'Vencimento VPN - 7 dias',
            'tipo_produto': 'VPN',
            'tipo_template': 'vencimento',
            'conteudo': '''Olá {nome}! 🔒

Seu plano {plano} vence em {dias} dias.

💰 Valor: {valor}
🛡️ Para manter sua navegação segura, renove antes do vencimento.

Entre em contato para renovar! 👍''',
            'variaveis_disponiveis': json.dumps(['nome', 'plano', 'valor', 'dias']),
            'padrao': True
        },
        {
            'nome': 'Vencimento VPN - Hoje',
            'tipo_produto': 'VPN',
            'tipo_template': 'vencimento',
            'conteudo': '''🚨 ATENÇÃO {nome}!

Seu plano {plano} vence HOJE!

💰 Valor: {valor}
⚠️ Renove agora para manter sua proteção online.

Entre em contato urgente! 📞''',
            'variaveis_disponiveis': json.dumps(['nome', 'plano', 'valor', 'dias'])
        },
        {
            'nome': 'Renovação VPN Confirmada',
            'tipo_produto': 'VPN',
            'tipo_template': 'renovacao',
            'conteudo': '''✅ Renovação Confirmada!

Olá {nome}, sua renovação foi processada com sucesso!

🔒 Plano: {plano}
💰 Valor pago: {valor}
📅 Válido por mais {dias} dias

Sua segurança está garantida! 🛡️''',
            'variaveis_disponiveis': json.dumps(['nome', 'plano', 'valor', 'dias'])
        },
        
        # Templates para OUTROS
        {
            'nome': 'Vencimento Geral - 7 dias',
            'tipo_produto': 'OUTROS',
            'tipo_template': 'vencimento',
            'conteudo': '''Olá {nome}! 

Seu plano {plano} vence em {dias} dias.

💰 Valor: {valor}
📅 Para manter seu acesso, renove antes do vencimento.

Entre em contato para renovar! 👍''',
            'variaveis_disponiveis': json.dumps(['nome', 'plano', 'valor', 'dias']),
            'padrao': True
        },
        
        # Templates gerais
        {
            'nome': 'Mensagem Personalizada Geral',
            'tipo_produto': 'GERAL',
            'tipo_template': 'personalizada',
            'conteudo': '''Olá {nome}!

Esta é uma mensagem personalizada sobre seu plano {plano}.

💰 Valor: {valor}

Entre em contato para mais informações! 📞''',
            'variaveis_disponiveis': json.dumps(['nome', 'plano', 'valor', 'dias']),
            'padrao': True
        }
    ]
    
    with app.app_context():
        # Verificar se já existem templates
        if TemplateMensagem.query.count() > 0:
            print("Templates já existem no banco de dados.")
            return
        
        templates_criados = 0
        
        for template_data in templates_padrao:
            template = TemplateMensagem(
                nome=template_data['nome'],
                tipo_produto=template_data['tipo_produto'],
                tipo_template=template_data['tipo_template'],
                conteudo=template_data['conteudo'],
                variaveis_disponiveis=template_data['variaveis_disponiveis'],
                padrao=template_data.get('padrao', False),
                ativo=True
            )
            
            db.session.add(template)
            templates_criados += 1
        
        try:
            db.session.commit()
            print(f"{templates_criados} templates padrão criados com sucesso!")
        except Exception as e:
            print(f"Erro ao criar templates: {e}")
            db.session.rollback()

if __name__ == '__main__':
    criar_templates_padrao()

