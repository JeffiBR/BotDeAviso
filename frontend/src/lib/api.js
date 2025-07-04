import axios from 'axios';

// Configuração base da API
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para requests
api.interceptors.request.use(
  (config) => {
    // Adicionar token de autenticação se necessário
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para responses
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Tratamento global de erros
    if (error.response?.status === 401) {
      // Redirecionar para login se necessário
      // window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Funções da API

// Clientes
export const clientesAPI = {
  listar: (filtros = {}) => api.get('/clientes', { params: filtros }),
  criar: (dados) => api.post('/clientes', dados),
  obter: (id) => api.get(`/clientes/${id}`),
  atualizar: (id, dados) => api.put(`/clientes/${id}`, dados),
  deletar: (id) => api.delete(`/clientes/${id}`),
  renovar: (id, dados) => api.post(`/clientes/${id}/renovar`, dados),
  dashboard: (tipoProduto) => api.get(`/clientes/dashboard/${tipoProduto}`),
  avisosPendentes: () => api.get('/clientes/avisos-pendentes'),
  marcarMensagemEnviada: (id) => api.post(`/clientes/marcar-mensagem-enviada/${id}`),
  atualizarComentario: (id, comentarios) => api.put(`/clientes/${id}/comentarios`, { comentarios }),
  deletarComentario: (id) => api.delete(`/clientes/${id}/comentarios`),
};

// Templates
export const templatesAPI = {
  listar: (filtros = {}) => api.get('/templates', { params: filtros }),
  criar: (dados) => api.post('/templates', dados),
  obter: (id) => api.get(`/templates/${id}`),
  atualizar: (id, dados) => api.put(`/templates/${id}`, dados),
  deletar: (id) => api.delete(`/templates/${id}`),
  preview: (id, dados) => api.post(`/templates/${id}/preview`, dados),
  obterPadrao: (tipoProduto, tipoTemplate) => 
    api.get(`/templates/padrao/${tipoProduto}/${tipoTemplate}`),
};

// Configurações
export const configuracoesAPI = {
  listar: (categoria = null) => 
    api.get('/configuracoes', categoria ? { params: { categoria } } : {}),
  listarCategoria: (categoria) => api.get(`/configuracoes/${categoria}`),
  criar: (dados) => api.post('/configuracoes', dados),
  obter: (chave) => api.get(`/configuracoes/${chave}`),
  atualizar: (chave, dados) => api.put(`/configuracoes/${chave}`, dados),
  deletar: (chave) => api.delete(`/configuracoes/${chave}`),
  atualizarLote: (configuracoes) => api.put('/configuracoes/batch', { configuracoes }),
  inicializar: () => api.post('/configuracoes/inicializar'),
};

// Logs
export const logsAPI = {
  listar: (filtros = {}) => api.get('/logs', { params: filtros }),
  criar: (dados) => api.post('/logs', dados),
  obter: (id) => api.get(`/logs/${id}`),
  atualizar: (id, dados) => api.put(`/logs/${id}`, dados),
  estatisticas: (filtros = {}) => api.get('/logs/estatisticas', { params: filtros }),
  reenviar: (id) => api.post(`/logs/reenviar/${id}`),
};

// Renovações
export const renovacoesAPI = {
  listar: (filtros = {}) => api.get('/renovacoes', { params: filtros }),
  obter: (id) => api.get(`/renovacoes/${id}`),
  atualizar: (id, dados) => api.put(`/renovacoes/${id}`, dados),
  deletar: (id) => api.delete(`/renovacoes/${id}`),
  estatisticas: (filtros = {}) => api.get('/renovacoes/estatisticas', { params: filtros }),
  historicoCliente: (clienteId) => api.get(`/renovacoes/cliente/${clienteId}`),
};

// WhatsApp
export const whatsappAPI = {
  status: () => api.get('/whatsapp/status'),
  iniciar: () => api.post('/whatsapp/iniciar'),
  parar: () => api.post('/whatsapp/parar'),
  obterQR: () => api.get('/whatsapp/qr'),
  enviarTeste: (dados) => api.post('/whatsapp/enviar-teste', dados),
  processarAvisos: () => api.post('/whatsapp/processar-avisos'),
  obterConfiguracoes: () => api.get('/whatsapp/configuracoes'),
  atualizarConfiguracoes: (dados) => api.put('/whatsapp/configuracoes', dados),
  obterLogs: () => api.get('/whatsapp/logs'),
  limparLogs: () => api.delete('/whatsapp/limpar-logs'),
};

export default api;

