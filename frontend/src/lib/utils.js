import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { format, formatDistanceToNow, parseISO, isValid } from 'date-fns';
import { ptBR } from 'date-fns/locale';

// Função para combinar classes CSS
export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

// Formatação de datas
export const formatarData = (data, formato = 'dd/MM/yyyy') => {
  if (!data) return '';
  
  try {
    const dataObj = typeof data === 'string' ? parseISO(data) : data;
    if (!isValid(dataObj)) return '';
    
    return format(dataObj, formato, { locale: ptBR });
  } catch (error) {
    console.error('Erro ao formatar data:', error);
    return '';
  }
};

export const formatarDataHora = (data, formato = 'dd/MM/yyyy HH:mm') => {
  return formatarData(data, formato);
};

export const formatarDataRelativa = (data) => {
  if (!data) return '';
  
  try {
    const dataObj = typeof data === 'string' ? parseISO(data) : data;
    if (!isValid(dataObj)) return '';
    
    return formatDistanceToNow(dataObj, { 
      addSuffix: true, 
      locale: ptBR 
    });
  } catch (error) {
    console.error('Erro ao formatar data relativa:', error);
    return '';
  }
};

// Formatação de valores monetários
export const formatarMoeda = (valor, moeda = 'BRL') => {
  if (valor === null || valor === undefined) return 'R$ 0,00';
  
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: moeda,
  }).format(valor);
};

// Formatação de números
export const formatarNumero = (numero, decimais = 0) => {
  if (numero === null || numero === undefined) return '0';
  
  return new Intl.NumberFormat('pt-BR', {
    minimumFractionDigits: decimais,
    maximumFractionDigits: decimais,
  }).format(numero);
};

// Formatação de telefone
export const formatarTelefone = (telefone) => {
  if (!telefone) return '';
  
  // Remove tudo que não é número
  const numeros = telefone.replace(/\D/g, '');
  
  // Aplica formatação baseada no tamanho
  if (numeros.length === 11) {
    return numeros.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
  } else if (numeros.length === 10) {
    return numeros.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
  }
  
  return telefone;
};

// Validações
export const validarEmail = (email) => {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
};

export const validarTelefone = (telefone) => {
  const numeros = telefone.replace(/\D/g, '');
  return numeros.length >= 10 && numeros.length <= 11;
};

export const validarCPF = (cpf) => {
  const numeros = cpf.replace(/\D/g, '');
  
  if (numeros.length !== 11) return false;
  
  // Verifica se todos os dígitos são iguais
  if (/^(\d)\1{10}$/.test(numeros)) return false;
  
  // Validação do CPF
  let soma = 0;
  for (let i = 0; i < 9; i++) {
    soma += parseInt(numeros.charAt(i)) * (10 - i);
  }
  
  let resto = 11 - (soma % 11);
  if (resto === 10 || resto === 11) resto = 0;
  if (resto !== parseInt(numeros.charAt(9))) return false;
  
  soma = 0;
  for (let i = 0; i < 10; i++) {
    soma += parseInt(numeros.charAt(i)) * (11 - i);
  }
  
  resto = 11 - (soma % 11);
  if (resto === 10 || resto === 11) resto = 0;
  if (resto !== parseInt(numeros.charAt(10))) return false;
  
  return true;
};

// Utilitários para status
export const getStatusColor = (status) => {
  const cores = {
    ativo: 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900/20',
    inativo: 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900/20',
    vencido: 'text-red-600 bg-red-100 dark:text-red-400 dark:bg-red-900/20',
    vencendo: 'text-yellow-600 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900/20',
    renovado: 'text-blue-600 bg-blue-100 dark:text-blue-400 dark:bg-blue-900/20',
    enviada: 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900/20',
    falha: 'text-red-600 bg-red-100 dark:text-red-400 dark:bg-red-900/20',
    pendente: 'text-yellow-600 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900/20',
  };
  
  return cores[status] || cores.inativo;
};

export const getStatusText = (status) => {
  const textos = {
    ativo: 'Ativo',
    inativo: 'Inativo',
    vencido: 'Vencido',
    vencendo: 'Vencendo',
    renovado: 'Renovado',
    enviada: 'Enviada',
    falha: 'Falha',
    pendente: 'Pendente',
  };
  
  return textos[status] || status;
};

// Utilitários para tipos de produto
export const getTipoProdutoColor = (tipo) => {
  const cores = {
    IPTV: 'text-purple-600 bg-purple-100 dark:text-purple-400 dark:bg-purple-900/20',
    VPN: 'text-blue-600 bg-blue-100 dark:text-blue-400 dark:bg-blue-900/20',
    OUTROS: 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900/20',
  };
  
  return cores[tipo] || cores.OUTROS;
};

export const getTipoProdutoIcon = (tipo) => {
  const icones = {
    IPTV: '📺',
    VPN: '🔒',
    OUTROS: '📦',
  };
  
  return icones[tipo] || icones.OUTROS;
};

// Utilitários para cálculos
export const calcularDiasVencimento = (dataVencimento) => {
  if (!dataVencimento) return null;
  
  try {
    const hoje = new Date();
    const vencimento = typeof dataVencimento === 'string' 
      ? parseISO(dataVencimento) 
      : dataVencimento;
    
    if (!isValid(vencimento)) return null;
    
    const diferenca = vencimento.getTime() - hoje.getTime();
    return Math.ceil(diferenca / (1000 * 60 * 60 * 24));
  } catch (error) {
    console.error('Erro ao calcular dias de vencimento:', error);
    return null;
  }
};

export const getStatusVencimento = (dataVencimento) => {
  const dias = calcularDiasVencimento(dataVencimento);
  
  if (dias === null) return 'indefinido';
  if (dias < 0) return 'vencido';
  if (dias === 0) return 'vence_hoje';
  if (dias <= 3) return 'vencendo';
  if (dias <= 7) return 'proximo_vencimento';
  
  return 'ativo';
};

// Utilitários para arrays
export const agruparPor = (array, chave) => {
  return array.reduce((grupos, item) => {
    const grupo = item[chave];
    if (!grupos[grupo]) {
      grupos[grupo] = [];
    }
    grupos[grupo].push(item);
    return grupos;
  }, {});
};

export const ordenarPor = (array, chave, ordem = 'asc') => {
  return [...array].sort((a, b) => {
    const valorA = a[chave];
    const valorB = b[chave];
    
    if (ordem === 'desc') {
      return valorB > valorA ? 1 : valorB < valorA ? -1 : 0;
    }
    
    return valorA > valorB ? 1 : valorA < valorB ? -1 : 0;
  });
};

// Utilitários para debounce
export const debounce = (func, delay) => {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(null, args), delay);
  };
};

// Utilitários para localStorage
export const salvarLocalStorage = (chave, valor) => {
  try {
    localStorage.setItem(chave, JSON.stringify(valor));
  } catch (error) {
    console.error('Erro ao salvar no localStorage:', error);
  }
};

export const lerLocalStorage = (chave, valorPadrao = null) => {
  try {
    const item = localStorage.getItem(chave);
    return item ? JSON.parse(item) : valorPadrao;
  } catch (error) {
    console.error('Erro ao ler do localStorage:', error);
    return valorPadrao;
  }
};

// Utilitários para tratamento de erros
export const tratarErroAPI = (error) => {
  if (error.response) {
    // Erro de resposta do servidor
    const { status, data } = error.response;
    
    if (status === 400) {
      return data.erro || 'Dados inválidos';
    } else if (status === 401) {
      return 'Não autorizado';
    } else if (status === 403) {
      return 'Acesso negado';
    } else if (status === 404) {
      return 'Recurso não encontrado';
    } else if (status === 500) {
      return 'Erro interno do servidor';
    }
    
    return data.erro || `Erro ${status}`;
  } else if (error.request) {
    // Erro de rede
    return 'Erro de conexão com o servidor';
  } else {
    // Outro tipo de erro
    return error.message || 'Erro desconhecido';
  }
};

// Utilitários para cores aleatórias
export const gerarCorAleatoria = () => {
  const cores = [
    'bg-red-500', 'bg-blue-500', 'bg-green-500', 'bg-yellow-500',
    'bg-purple-500', 'bg-pink-500', 'bg-indigo-500', 'bg-teal-500',
    'bg-orange-500', 'bg-cyan-500', 'bg-lime-500', 'bg-emerald-500'
  ];
  
  return cores[Math.floor(Math.random() * cores.length)];
};

// Utilitários para iniciais
export const obterIniciais = (nome) => {
  if (!nome) return '';
  
  return nome
    .split(' ')
    .map(palavra => palavra.charAt(0).toUpperCase())
    .slice(0, 2)
    .join('');
};

