import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import './App.css';

// Hooks
import { useTheme, useSidebar } from './lib/store';

// Componentes
import Sidebar from './components/layout/Sidebar';
import Header from './components/layout/Header';
import BottomNavigation from './components/layout/BottomNavigation';
import LoadingScreen from './components/ui/LoadingScreen';

// Páginas
import Dashboard from './pages/Dashboard';
import Clientes from './pages/Clientes';
import Templates from './pages/Templates';
import WhatsApp from './pages/WhatsApp';
import Configuracoes from './pages/Configuracoes';
import Logs from './pages/Logs';
import Renovacoes from './pages/Renovacoes';

// Configuração do React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutos
    },
  },
});

function App() {
  const { tema } = useTheme();
  const { sidebarAberta } = useSidebar();
  const [carregandoInicial, setCarregandoInicial] = useState(true);
  const [isMobile, setIsMobile] = useState(false);

  // Detectar se é mobile
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // Aplicar tema
  useEffect(() => {
    document.documentElement.classList.toggle('dark', tema === 'dark');
  }, [tema]);

  // Simular carregamento inicial
  useEffect(() => {
    const timer = setTimeout(() => {
      setCarregandoInicial(false);
    }, 1500);

    return () => clearTimeout(timer);
  }, []);

  if (carregandoInicial) {
    return <LoadingScreen />;
  }

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className={`min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300 ${tema}`}>
          {/* Layout Desktop */}
          {!isMobile && (
            <div className="flex h-screen">
              {/* Sidebar Desktop */}
              <Sidebar />
              
              {/* Conteúdo Principal Desktop */}
              <div className={`flex-1 flex flex-col transition-all duration-300 ${
                sidebarAberta ? 'ml-64' : 'ml-16'
              }`}>
                <Header />
                <main className="flex-1 overflow-y-auto p-6 custom-scrollbar">
                  <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/clientes" element={<Clientes />} />
                    <Route path="/templates" element={<Templates />} />
                    <Route path="/whatsapp" element={<WhatsApp />} />
                    <Route path="/configuracoes" element={<Configuracoes />} />
                    <Route path="/logs" element={<Logs />} />
                    <Route path="/renovacoes" element={<Renovacoes />} />
                  </Routes>
                </main>
              </div>
            </div>
          )}

          {/* Layout Mobile */}
          {isMobile && (
            <div className="flex flex-col h-screen">
              {/* Header Mobile */}
              <Header isMobile={true} />
              
              {/* Conteúdo Principal Mobile */}
              <main className="flex-1 overflow-y-auto mobile-content custom-scrollbar">
                <Routes>
                  <Route path="/" element={<Dashboard isMobile={true} />} />
                  <Route path="/dashboard" element={<Dashboard isMobile={true} />} />
                  <Route path="/clientes" element={<Clientes isMobile={true} />} />
                  <Route path="/templates" element={<Templates isMobile={true} />} />
                  <Route path="/whatsapp" element={<WhatsApp isMobile={true} />} />
                  <Route path="/configuracoes" element={<Configuracoes isMobile={true} />} />
                  <Route path="/logs" element={<Logs isMobile={true} />} />
                  <Route path="/renovacoes" element={<Renovacoes isMobile={true} />} />
                </Routes>
              </main>
              
              {/* Bottom Navigation Mobile */}
              <BottomNavigation />
            </div>
          )}

          {/* Overlay para sidebar mobile */}
          {isMobile && sidebarAberta && (
            <div className="mobile-overlay" onClick={() => useSidebar.getState().toggleSidebar()} />
          )}

          {/* Sidebar Mobile */}
          {isMobile && (
            <div className={`mobile-sidebar ${sidebarAberta ? 'mobile-sidebar-open' : 'mobile-sidebar-closed'}`}>
              <Sidebar isMobile={true} />
            </div>
          )}

          {/* Notificações Toast */}
          <Toaster
            position={isMobile ? "top-center" : "top-right"}
            toastOptions={{
              duration: 4000,
              className: isMobile ? 'mobile-toast' : '',
              style: {
                background: tema === 'dark' ? '#1f2937' : '#ffffff',
                color: tema === 'dark' ? '#f9fafb' : '#111827',
                border: `1px solid ${tema === 'dark' ? '#374151' : '#e5e7eb'}`,
              },
            }}
          />
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;

