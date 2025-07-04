import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// Store principal da aplicação
export const useAppStore = create(
  persist(
    (set, get) => ({
      // Estado da aplicação
      tema: 'dark',
      sidebarAberta: true,
      carregando: false,
      
      // Estado do WhatsApp
      whatsappStatus: {
        executando: false,
        conectado: false,
        qrDisponivel: false,
      },
      
      // Dados em cache
      clientes: [],
      templates: [],
      configuracoes: {},
      
      // Filtros ativos
      filtros: {
        tipoProduto: 'todos',
        status: 'todos',
        dataInicio: null,
        dataFim: null,
      },
      
      // Actions
      setTema: (tema) => set({ tema }),
      
      toggleSidebar: () => set((state) => ({ 
        sidebarAberta: !state.sidebarAberta 
      })),
      
      setCarregando: (carregando) => set({ carregando }),
      
      setWhatsappStatus: (status) => set({ 
        whatsappStatus: { ...get().whatsappStatus, ...status } 
      }),
      
      setClientes: (clientes) => set({ clientes }),
      
      adicionarCliente: (cliente) => set((state) => ({
        clientes: [...state.clientes, cliente]
      })),
      
      atualizarCliente: (id, dadosAtualizados) => set((state) => ({
        clientes: state.clientes.map(cliente => 
          cliente.id === id ? { ...cliente, ...dadosAtualizados } : cliente
        )
      })),
      
      removerCliente: (id) => set((state) => ({
        clientes: state.clientes.filter(cliente => cliente.id !== id)
      })),
      
      setTemplates: (templates) => set({ templates }),
      
      setConfiguracoes: (configuracoes) => set({ configuracoes }),
      
      setFiltros: (novosFiltros) => set((state) => ({
        filtros: { ...state.filtros, ...novosFiltros }
      })),
      
      limparFiltros: () => set({
        filtros: {
          tipoProduto: 'todos',
          status: 'todos',
          dataInicio: null,
          dataFim: null,
        }
      }),
    }),
    {
      name: 'sistema-vencimento-storage',
      partialize: (state) => ({
        tema: state.tema,
        sidebarAberta: state.sidebarAberta,
        filtros: state.filtros,
      }),
    }
  )
);

// Store para notificações
export const useNotificationStore = create((set, get) => ({
  notificacoes: [],
  
  adicionarNotificacao: (notificacao) => {
    const id = Date.now().toString();
    const novaNotificacao = {
      id,
      tipo: 'info',
      duracao: 5000,
      ...notificacao,
    };
    
    set((state) => ({
      notificacoes: [...state.notificacoes, novaNotificacao]
    }));
    
    // Auto-remover após a duração especificada
    if (novaNotificacao.duracao > 0) {
      setTimeout(() => {
        get().removerNotificacao(id);
      }, novaNotificacao.duracao);
    }
    
    return id;
  },
  
  removerNotificacao: (id) => set((state) => ({
    notificacoes: state.notificacoes.filter(n => n.id !== id)
  })),
  
  limparNotificacoes: () => set({ notificacoes: [] }),
}));

// Store para modais
export const useModalStore = create((set) => ({
  modais: {},
  
  abrirModal: (nome, dados = {}) => set((state) => ({
    modais: { ...state.modais, [nome]: { aberto: true, dados } }
  })),
  
  fecharModal: (nome) => set((state) => ({
    modais: { ...state.modais, [nome]: { aberto: false, dados: {} } }
  })),
  
  isModalAberto: (nome) => {
    const state = useModalStore.getState();
    return state.modais[nome]?.aberto || false;
  },
  
  getDadosModal: (nome) => {
    const state = useModalStore.getState();
    return state.modais[nome]?.dados || {};
  },
}));

// Hooks personalizados para facilitar o uso
export const useTheme = () => {
  const tema = useAppStore((state) => state.tema);
  const setTema = useAppStore((state) => state.setTema);
  
  const toggleTheme = () => {
    setTema(tema === 'dark' ? 'light' : 'dark');
  };
  
  return { tema, setTema, toggleTheme };
};

export const useSidebar = () => {
  const sidebarAberta = useAppStore((state) => state.sidebarAberta);
  const toggleSidebar = useAppStore((state) => state.toggleSidebar);
  
  return { sidebarAberta, toggleSidebar };
};

export const useLoading = () => {
  const carregando = useAppStore((state) => state.carregando);
  const setCarregando = useAppStore((state) => state.setCarregando);
  
  return { carregando, setCarregando };
};

export const useWhatsAppStatus = () => {
  const status = useAppStore((state) => state.whatsappStatus);
  const setStatus = useAppStore((state) => state.setWhatsappStatus);
  
  return { status, setStatus };
};

