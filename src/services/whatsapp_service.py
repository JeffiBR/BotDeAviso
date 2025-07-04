"""
Serviço de integração com WhatsApp usando whatsapp-web.js
"""
import os
import json
import time
import threading
import subprocess
import requests
from datetime import datetime, timedelta
from src.models.user import db
from src.models.cliente import Cliente
from src.models.log_mensagem import LogMensagem
from src.models.configuracao import Configuracao
from src.models.template_mensagem import TemplateMensagem

class WhatsAppService:
    def __init__(self):
        self.processo_whatsapp = None
        self.conectado = False
        self.qr_code = None
        self.porta = 3001
        self.base_url = f"http://localhost:{self.porta}"
        self.thread_envio = None
        self.executando = False
        
    def iniciar_servico(self):
        """Inicia o serviço do WhatsApp"""
        try:
            # Verificar se o Node.js está instalado
            subprocess.run(['node', '--version'], check=True, capture_output=True)
            
            # Criar diretório para o serviço se não existir
            whatsapp_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'whatsapp-service')
            os.makedirs(whatsapp_dir, exist_ok=True)
            
            # Criar package.json se não existir
            package_json_path = os.path.join(whatsapp_dir, 'package.json')
            if not os.path.exists(package_json_path):
                self._criar_package_json(package_json_path)
            
            # Instalar dependências
            self._instalar_dependencias(whatsapp_dir)
            
            # Criar servidor WhatsApp se não existir
            server_js_path = os.path.join(whatsapp_dir, 'server.js')
            if not os.path.exists(server_js_path):
                self._criar_servidor_whatsapp(server_js_path)
            
            # Iniciar o processo
            self.processo_whatsapp = subprocess.Popen(
                ['node', 'server.js'],
                cwd=whatsapp_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Aguardar inicialização
            time.sleep(5)
            
            # Verificar se está rodando
            if self._verificar_servico():
                self.executando = True
                self._iniciar_thread_envio()
                return True
            else:
                return False
                
        except Exception as e:
            self._log_erro(f"Erro ao iniciar serviço WhatsApp: {str(e)}")
            return False
    
    def parar_servico(self):
        """Para o serviço do WhatsApp"""
        try:
            self.executando = False
            
            if self.thread_envio:
                self.thread_envio.join(timeout=5)
            
            if self.processo_whatsapp:
                self.processo_whatsapp.terminate()
                self.processo_whatsapp.wait(timeout=10)
                
            self.conectado = False
            return True
            
        except Exception as e:
            self._log_erro(f"Erro ao parar serviço WhatsApp: {str(e)}")
            return False
    
    def obter_qr_code(self):
        """Obtém o QR code para conexão"""
        try:
            response = requests.get(f"{self.base_url}/qr", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.qr_code = data.get('qr')
                return self.qr_code
            return None
        except Exception as e:
            self._log_erro(f"Erro ao obter QR code: {str(e)}")
            return None
    
    def verificar_conexao(self):
        """Verifica se está conectado ao WhatsApp"""
        try:
            response = requests.get(f"{self.base_url}/status", timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.conectado = data.get('connected', False)
                return self.conectado
            return False
        except Exception as e:
            self._log_erro(f"Erro ao verificar conexão: {str(e)}")
            return False
    
    def enviar_mensagem(self, numero, mensagem, cliente_id=None):
        """Envia uma mensagem via WhatsApp"""
        try:
            # Formatar número
            numero_formatado = self._formatar_numero(numero)
            
            # Dados para envio
            dados = {
                'number': numero_formatado,
                'message': mensagem
            }
            
            # Enviar mensagem
            response = requests.post(
                f"{self.base_url}/send-message",
                json=dados,
                timeout=30
            )
            
            # Criar log
            status = 'enviada' if response.status_code == 200 else 'falha'
            erro_detalhes = None
            
            if response.status_code != 200:
                erro_detalhes = f"HTTP {response.status_code}: {response.text}"
            
            self._criar_log_mensagem(
                cliente_id=cliente_id,
                telefone_destino=numero,
                mensagem=mensagem,
                status=status,
                erro_detalhes=erro_detalhes
            )
            
            return response.status_code == 200
            
        except Exception as e:
            erro_msg = str(e)
            self._log_erro(f"Erro ao enviar mensagem: {erro_msg}")
            
            # Criar log de erro
            self._criar_log_mensagem(
                cliente_id=cliente_id,
                telefone_destino=numero,
                mensagem=mensagem,
                status='falha',
                erro_detalhes=erro_msg
            )
            
            return False
    
    def processar_avisos_automaticos(self):
        """Processa e envia avisos automáticos"""
        try:
            if not self.conectado:
                return
            
            # Buscar clientes que precisam de aviso
            response = requests.get('http://localhost:5000/api/clientes/avisos-pendentes')
            if response.status_code != 200:
                return
            
            dados = response.json()
            clientes_para_aviso = dados.get('clientes_para_aviso', [])
            
            if not clientes_para_aviso:
                return
            
            # Obter intervalo entre mensagens
            intervalo = Configuracao.get_configuracao('whatsapp_intervalo_mensagens', 60)
            
            for aviso in clientes_para_aviso:
                try:
                    cliente_data = aviso['cliente']
                    tipo_aviso = aviso['tipo_aviso']
                    
                    # Verificar se está no horário correto
                    if not self._esta_no_horario_funcionamento():
                        continue
                    
                    # Gerar mensagem
                    mensagem = self._gerar_mensagem_aviso(cliente_data, tipo_aviso)
                    
                    if mensagem:
                        # Enviar mensagem
                        sucesso = self.enviar_mensagem(
                            cliente_data['telefone'],
                            mensagem,
                            cliente_data['id']
                        )
                        
                        if sucesso:
                            # Marcar como enviada
                            requests.post(
                                f"http://localhost:5000/api/clientes/marcar-mensagem-enviada/{cliente_data['id']}"
                            )
                        
                        # Aguardar intervalo entre mensagens
                        time.sleep(intervalo)
                
                except Exception as e:
                    self._log_erro(f"Erro ao processar aviso para cliente {cliente_data.get('id', 'N/A')}: {str(e)}")
                    continue
        
        except Exception as e:
            self._log_erro(f"Erro no processamento automático: {str(e)}")
    
    def _iniciar_thread_envio(self):
        """Inicia thread para envio automático"""
        def loop_envio():
            while self.executando:
                try:
                    if self.conectado:
                        self.processar_avisos_automaticos()
                    time.sleep(300)  # Verificar a cada 5 minutos
                except Exception as e:
                    self._log_erro(f"Erro na thread de envio: {str(e)}")
                    time.sleep(60)
        
        self.thread_envio = threading.Thread(target=loop_envio, daemon=True)
        self.thread_envio.start()
    
    def _verificar_servico(self):
        """Verifica se o serviço está rodando"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _formatar_numero(self, numero):
        """Formata número para WhatsApp"""
        # Remove caracteres especiais
        numero_limpo = ''.join(filter(str.isdigit, numero))
        
        # Adiciona código do país se necessário
        if len(numero_limpo) == 11 and numero_limpo.startswith('11'):
            numero_limpo = '55' + numero_limpo
        elif len(numero_limpo) == 10:
            numero_limpo = '5511' + numero_limpo
        elif not numero_limpo.startswith('55'):
            numero_limpo = '55' + numero_limpo
        
        return numero_limpo + '@c.us'
    
    def _gerar_mensagem_aviso(self, cliente_data, tipo_aviso):
        """Gera mensagem de aviso para o cliente"""
        try:
            # Buscar template apropriado
            template_id = cliente_data.get('template_mensagem_id')
            
            if template_id:
                response = requests.get(f"http://localhost:5000/api/templates/{template_id}")
                if response.status_code == 200:
                    template_data = response.json()['template']
                else:
                    template_data = None
            else:
                template_data = None
            
            # Se não tem template específico, buscar padrão
            if not template_data:
                tipo_template = 'vencimento' if tipo_aviso in ['vencimento', 'antecedencia'] else 'personalizada'
                response = requests.get(
                    f"http://localhost:5000/api/templates/padrao/{cliente_data['tipo_produto']}/{tipo_template}"
                )
                if response.status_code == 200:
                    template_data = response.json()['template']
                else:
                    return None
            
            # Processar template
            if template_data:
                from src.models.template_mensagem import TemplateMensagem
                
                # Criar objeto cliente fictício
                class ClienteFicticio:
                    def __init__(self, data):
                        self.nome_completo = data['nome_completo']
                        self.plano_contratado = data['plano_contratado']
                        self.valor_plano = data['valor_plano']
                
                cliente_obj = ClienteFicticio(cliente_data)
                
                # Calcular dias para vencimento
                from datetime import datetime
                data_vencimento = datetime.fromisoformat(cliente_data['data_vencimento']).date()
                dias_vencimento = (data_vencimento - datetime.now().date()).days
                
                # Processar template
                template = TemplateMensagem()
                template.conteudo = template_data['conteudo']
                
                return template.processar_template(cliente_obj, dias_vencimento)
            
            return None
            
        except Exception as e:
            self._log_erro(f"Erro ao gerar mensagem: {str(e)}")
            return None
    
    def _esta_no_horario_funcionamento(self):
        """Verifica se está no horário de funcionamento"""
        try:
            from datetime import datetime, time
            
            agora = datetime.now()
            hora_atual = agora.time()
            dia_semana = agora.weekday()  # 0 = segunda
            
            # Obter configurações
            horario_inicio = Configuracao.get_configuracao('whatsapp_horario_inicio', '08:00')
            horario_fim = Configuracao.get_configuracao('whatsapp_horario_fim', '22:00')
            dias_funcionamento = Configuracao.get_configuracao('whatsapp_dias_funcionamento', 
                ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'])
            
            # Verificar dia da semana
            dias_semana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']
            dia_atual = dias_semana[dia_semana]
            
            if dia_atual not in dias_funcionamento:
                return False
            
            # Verificar horário
            inicio = datetime.strptime(horario_inicio, '%H:%M').time()
            fim = datetime.strptime(horario_fim, '%H:%M').time()
            
            return inicio <= hora_atual <= fim
            
        except Exception as e:
            self._log_erro(f"Erro ao verificar horário: {str(e)}")
            return True  # Em caso de erro, permitir envio
    
    def _criar_log_mensagem(self, cliente_id, telefone_destino, mensagem, status, erro_detalhes=None):
        """Cria log de mensagem no banco"""
        try:
            from src.main import app
            
            with app.app_context():
                log = LogMensagem(
                    cliente_id=cliente_id,
                    telefone_destino=telefone_destino,
                    mensagem=mensagem,
                    status=status,
                    tipo_notificacao='automatica',
                    data_envio=datetime.utcnow() if status == 'enviada' else None,
                    erro_detalhes=erro_detalhes,
                    tentativas=1
                )
                
                db.session.add(log)
                db.session.commit()
                
        except Exception as e:
            print(f"Erro ao criar log: {str(e)}")
    
    def _log_erro(self, mensagem):
        """Registra erro no log"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] WHATSAPP ERROR: {mensagem}"
        print(log_msg)
        
        # Salvar em arquivo de log
        try:
            log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            log_file = os.path.join(log_dir, 'whatsapp.log')
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_msg + '\n')
        except:
            pass
    
    def _criar_package_json(self, caminho):
        """Cria package.json para o serviço WhatsApp"""
        package_json = {
            "name": "whatsapp-service",
            "version": "1.0.0",
            "description": "Serviço WhatsApp para sistema de vencimento",
            "main": "server.js",
            "dependencies": {
                "whatsapp-web.js": "^1.23.0",
                "express": "^4.18.2",
                "qrcode": "^1.5.3",
                "cors": "^2.8.5"
            }
        }
        
        with open(caminho, 'w') as f:
            json.dump(package_json, f, indent=2)
    
    def _instalar_dependencias(self, diretorio):
        """Instala dependências do Node.js"""
        try:
            subprocess.run(['npm', 'install'], cwd=diretorio, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            self._log_erro(f"Erro ao instalar dependências: {str(e)}")
    
    def _criar_servidor_whatsapp(self, caminho):
        """Cria servidor Node.js para WhatsApp"""
        codigo_servidor = '''
const { Client, LocalAuth } = require('whatsapp-web.js');
const express = require('express');
const QRCode = require('qrcode');
const cors = require('cors');

const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

let client;
let qrCodeData = null;
let isConnected = false;

// Inicializar cliente WhatsApp
function initializeClient() {
    client = new Client({
        authStrategy: new LocalAuth({
            dataPath: './whatsapp-session'
        }),
        puppeteer: {
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        }
    });

    client.on('qr', async (qr) => {
        console.log('QR Code recebido');
        qrCodeData = qr;
        try {
            qrCodeData = await QRCode.toDataURL(qr);
        } catch (err) {
            console.error('Erro ao gerar QR code:', err);
        }
    });

    client.on('ready', () => {
        console.log('Cliente WhatsApp conectado!');
        isConnected = true;
        qrCodeData = null;
    });

    client.on('authenticated', () => {
        console.log('Cliente autenticado');
    });

    client.on('auth_failure', (msg) => {
        console.error('Falha na autenticação:', msg);
        isConnected = false;
    });

    client.on('disconnected', (reason) => {
        console.log('Cliente desconectado:', reason);
        isConnected = false;
        qrCodeData = null;
    });

    client.initialize();
}

// Rotas da API
app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.get('/status', (req, res) => {
    res.json({ 
        connected: isConnected,
        hasQR: !!qrCodeData,
        timestamp: new Date().toISOString()
    });
});

app.get('/qr', (req, res) => {
    if (qrCodeData) {
        res.json({ qr: qrCodeData });
    } else {
        res.status(404).json({ error: 'QR code não disponível' });
    }
});

app.post('/send-message', async (req, res) => {
    try {
        const { number, message } = req.body;

        if (!isConnected) {
            return res.status(400).json({ error: 'WhatsApp não conectado' });
        }

        if (!number || !message) {
            return res.status(400).json({ error: 'Número e mensagem são obrigatórios' });
        }

        await client.sendMessage(number, message);
        
        res.json({ 
            success: true, 
            message: 'Mensagem enviada com sucesso',
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        console.error('Erro ao enviar mensagem:', error);
        res.status(500).json({ 
            error: 'Erro ao enviar mensagem',
            details: error.message 
        });
    }
});

app.listen(port, () => {
    console.log(`Servidor WhatsApp rodando na porta ${port}`);
    initializeClient();
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('Encerrando servidor...');
    if (client) {
        client.destroy();
    }
    process.exit(0);
});
'''
        
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(codigo_servidor)

# Instância global do serviço
whatsapp_service = WhatsAppService()

