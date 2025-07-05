// Configuração da API
export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
};

// URL base para as requisições
export const API_BASE_URL = API_CONFIG.baseURL;

// Verificar se a API está funcionando
export const checkApiHealth = async () => {
  try {
    const response = await fetch(API_BASE_URL.replace('/api', '/health'));
    const data = await response.json();
    return data.status === 'OK';
  } catch (error) {
    console.error('Erro ao verificar status da API:', error);
    return false;
  }
};

// Configurações de axios se estiver sendo usado
export const createAxiosConfig = () => ({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
  headers: API_CONFIG.headers,
});