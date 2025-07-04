import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Home, 
  Users, 
  MessageSquare, 
  Settings,
  BarChart3,
  FileText,
  RefreshCw,
  ChevronLeft,
  Smartphone,
  Monitor
} from 'lucide-react';

// Hooks
import { useSidebar } from '../../lib/store';

// Utils
import { cn } from '../../lib/utils';

const Sidebar = ({ isMobile = false }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { sidebarAberta, toggleSidebar } = useSidebar();

  const navigationItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: Home,
      path: '/dashboard',
      description: 'Visão geral'
    },
    {
      id: 'clientes',
      label: 'Clientes',
      icon: Users,
      path: '/clientes',
      description: 'Gerenciar clientes'
    },
    {
      id: 'templates',
      label: 'Templates',
      icon: FileText,
      path: '/templates',
      description: 'Mensagens'
    },
    {
      id: 'whatsapp',
      label: 'WhatsApp',
      icon: MessageSquare,
      path: '/whatsapp',
      description: 'Integração'
    },
    {
      id: 'renovacoes',
      label: 'Renovações',
      icon: RefreshCw,
      path: '/renovacoes',
      description: 'Histórico'
    },
    {
      id: 'logs',
      label: 'Logs',
      icon: BarChart3,
      path: '/logs',
      description: 'Relatórios'
    },
    {
      id: 'configuracoes',
      label: 'Configurações',
      icon: Settings,
      path: '/configuracoes',
      description: 'Sistema'
    }
  ];

  const handleNavigation = (path) => {
    navigate(path);
    if (isMobile) {
      toggleSidebar();
    }
  };

  const isActive = (path) => {
    if (path === '/dashboard') {
      return location.pathname === '/' || location.pathname === '/dashboard';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <aside className={cn(
      "flex flex-col bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 transition-all duration-300",
      isMobile ? "w-64 h-full" : sidebarAberta ? "w-64" : "w-16",
      !isMobile && "fixed left-0 top-0 h-screen z-30"
    )}>
      {/* Header */}
      <div className={cn(
        "flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700",
        isMobile && "safe-area-top"
      )}>
        {(sidebarAberta || isMobile) && (
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-3"
          >
            <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">SV</span>
            </div>
            <div>
              <h2 className="font-bold text-gray-900 dark:text-white text-sm">
                Sistema Vencimento
              </h2>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Dashboard Pro
              </p>
            </div>
          </motion.div>
        )}

        {!isMobile && (
          <motion.button
            whileTap={{ scale: 0.95 }}
            onClick={toggleSidebar}
            className="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200"
          >
            <ChevronLeft className={cn(
              "w-4 h-4 text-gray-600 dark:text-gray-400 transition-transform duration-300",
              !sidebarAberta && "rotate-180"
            )} />
          </motion.button>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2 overflow-y-auto custom-scrollbar">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.path);

          return (
            <motion.button
              key={item.id}
              whileTap={{ scale: 0.98 }}
              onClick={() => handleNavigation(item.path)}
              className={cn(
                "w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-all duration-200 relative group",
                active 
                  ? "bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400" 
                  : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-gray-100"
              )}
            >
              {/* Active indicator */}
              {active && (
                <motion.div
                  layoutId="sidebarActiveIndicator"
                  className="absolute left-0 top-0 bottom-0 w-1 bg-blue-600 dark:bg-blue-400 rounded-r-full"
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                />
              )}

              {/* Icon */}
              <Icon className={cn(
                "w-5 h-5 flex-shrink-0 transition-colors duration-200",
                active ? "text-blue-600 dark:text-blue-400" : ""
              )} />

              {/* Label */}
              {(sidebarAberta || isMobile) && (
                <motion.div
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="flex-1 text-left"
                >
                  <div className="font-medium text-sm">
                    {item.label}
                  </div>
                  <div className="text-xs opacity-70">
                    {item.description}
                  </div>
                </motion.div>
              )}

              {/* Tooltip for collapsed state */}
              {!sidebarAberta && !isMobile && (
                <div className="absolute left-full ml-2 px-2 py-1 bg-gray-900 dark:bg-gray-700 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-50">
                  {item.label}
                  <div className="absolute left-0 top-1/2 transform -translate-x-1 -translate-y-1/2 w-0 h-0 border-t-2 border-b-2 border-r-2 border-transparent border-r-gray-900 dark:border-r-gray-700"></div>
                </div>
              )}
            </motion.button>
          );
        })}
      </nav>

      {/* Footer */}
      <div className={cn(
        "p-4 border-t border-gray-200 dark:border-gray-700",
        isMobile && "safe-area-bottom"
      )}>
        {(sidebarAberta || isMobile) && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-3"
          >
            {/* Device indicator */}
            <div className="flex items-center justify-center space-x-2 text-xs text-gray-500 dark:text-gray-400">
              {isMobile ? (
                <>
                  <Smartphone className="w-3 h-3" />
                  <span>Mobile</span>
                </>
              ) : (
                <>
                  <Monitor className="w-3 h-3" />
                  <span>Desktop</span>
                </>
              )}
            </div>

            {/* Version */}
            <div className="text-center">
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Versão 1.0.0
              </p>
            </div>
          </motion.div>
        )}

        {/* Collapsed state indicator */}
        {!sidebarAberta && !isMobile && (
          <div className="flex justify-center">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          </div>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;

