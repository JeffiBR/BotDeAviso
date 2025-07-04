import { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { 
  Menu, 
  Bell, 
  Search, 
  Sun, 
  Moon, 
  Settings,
  User,
  ChevronDown,
  Wifi,
  WifiOff
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// Hooks
import { useTheme, useSidebar, useWhatsAppStatus } from '../../lib/store';

// Utils
import { cn } from '../../lib/utils';

const Header = ({ isMobile = false }) => {
  const location = useLocation();
  const { tema, toggleTheme } = useTheme();
  const { toggleSidebar } = useSidebar();
  const { status: whatsappStatus } = useWhatsAppStatus();
  
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);

  // Obter título da página atual
  const getPageTitle = () => {
    const path = location.pathname;
    const titles = {
      '/': 'Dashboard',
      '/dashboard': 'Dashboard',
      '/clientes': 'Clientes',
      '/templates': 'Templates',
      '/whatsapp': 'WhatsApp',
      '/configuracoes': 'Configurações',
      '/logs': 'Logs',
      '/renovacoes': 'Renovações',
    };
    return titles[path] || 'Sistema';
  };

  const getPageSubtitle = () => {
    const path = location.pathname;
    const subtitles = {
      '/': 'Visão geral do sistema',
      '/dashboard': 'Visão geral do sistema',
      '/clientes': 'Gerenciar clientes',
      '/templates': 'Mensagens personalizadas',
      '/whatsapp': 'Integração e envios',
      '/configuracoes': 'Configurações do sistema',
      '/logs': 'Histórico de mensagens',
      '/renovacoes': 'Histórico de renovações',
    };
    return subtitles[path] || '';
  };

  return (
    <header className={cn(
      "bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 transition-colors duration-300",
      isMobile ? "mobile-header safe-area-top" : "sticky top-0 z-40"
    )}>
      <div className={cn(
        "flex items-center justify-between",
        isMobile ? "px-4 py-3" : "px-6 py-4"
      )}>
        {/* Left Section */}
        <div className="flex items-center space-x-4">
          {/* Menu Button */}
          <motion.button
            whileTap={{ scale: 0.95 }}
            onClick={toggleSidebar}
            className={cn(
              "p-2 rounded-lg transition-colors duration-200",
              "hover:bg-gray-100 dark:hover:bg-gray-800",
              "focus:outline-none focus:ring-2 focus:ring-blue-500",
              isMobile ? "touch-target" : ""
            )}
          >
            <Menu className="w-5 h-5 text-gray-600 dark:text-gray-400" />
          </motion.button>

          {/* Page Title */}
          <div className="flex flex-col">
            <h1 className={cn(
              "font-semibold text-gray-900 dark:text-white",
              isMobile ? "mobile-header-title" : "text-xl"
            )}>
              {getPageTitle()}
            </h1>
            {!isMobile && (
              <p className="text-sm text-gray-500 dark:text-gray-400">
                {getPageSubtitle()}
              </p>
            )}
          </div>
        </div>

        {/* Center Section - Search (Desktop only) */}
        {!isMobile && (
          <div className="flex-1 max-w-md mx-8">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Buscar clientes, templates..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200"
              />
            </div>
          </div>
        )}

        {/* Right Section */}
        <div className="flex items-center space-x-2">
          {/* WhatsApp Status */}
          <div className={cn(
            "flex items-center space-x-2 px-3 py-1.5 rounded-lg",
            whatsappStatus.conectado 
              ? "bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400"
              : "bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400"
          )}>
            {whatsappStatus.conectado ? (
              <Wifi className="w-4 h-4" />
            ) : (
              <WifiOff className="w-4 h-4" />
            )}
            {!isMobile && (
              <span className="text-xs font-medium">
                {whatsappStatus.conectado ? 'Conectado' : 'Desconectado'}
              </span>
            )}
          </div>

          {/* Search Button (Mobile only) */}
          {isMobile && (
            <motion.button
              whileTap={{ scale: 0.95 }}
              className="touch-target p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200"
            >
              <Search className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            </motion.button>
          )}

          {/* Notifications */}
          <div className="relative">
            <motion.button
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowNotifications(!showNotifications)}
              className={cn(
                "p-2 rounded-lg transition-colors duration-200 relative",
                "hover:bg-gray-100 dark:hover:bg-gray-800",
                "focus:outline-none focus:ring-2 focus:ring-blue-500",
                isMobile ? "touch-target" : ""
              )}
            >
              <Bell className="w-5 h-5 text-gray-600 dark:text-gray-400" />
              {/* Notification Badge */}
              <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full flex items-center justify-center">
                <span className="text-xs text-white font-bold">3</span>
              </span>
            </motion.button>

            {/* Notifications Dropdown */}
            <AnimatePresence>
              {showNotifications && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95, y: -10 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.95, y: -10 }}
                  transition={{ duration: 0.2 }}
                  className={cn(
                    "absolute right-0 mt-2 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50",
                    isMobile && "w-screen max-w-sm -right-4"
                  )}
                >
                  <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                    <h3 className="font-semibold text-gray-900 dark:text-white">Notificações</h3>
                  </div>
                  <div className="max-h-64 overflow-y-auto">
                    {/* Notification Items */}
                    {[1, 2, 3].map((item) => (
                      <div key={item} className="p-4 border-b border-gray-100 dark:border-gray-700 last:border-b-0 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-150">
                        <div className="flex items-start space-x-3">
                          <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                          <div className="flex-1">
                            <p className="text-sm font-medium text-gray-900 dark:text-white">
                              Cliente João Silva vence hoje
                            </p>
                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                              há 5 minutos
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="p-3 border-t border-gray-200 dark:border-gray-700">
                    <button className="w-full text-sm text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium">
                      Ver todas as notificações
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Theme Toggle */}
          <motion.button
            whileTap={{ scale: 0.95 }}
            onClick={toggleTheme}
            className={cn(
              "p-2 rounded-lg transition-colors duration-200",
              "hover:bg-gray-100 dark:hover:bg-gray-800",
              "focus:outline-none focus:ring-2 focus:ring-blue-500",
              isMobile ? "touch-target" : ""
            )}
          >
            {tema === 'dark' ? (
              <Sun className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            ) : (
              <Moon className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            )}
          </motion.button>

          {/* User Menu */}
          <div className="relative">
            <motion.button
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowUserMenu(!showUserMenu)}
              className={cn(
                "flex items-center space-x-2 p-2 rounded-lg transition-colors duration-200",
                "hover:bg-gray-100 dark:hover:bg-gray-800",
                "focus:outline-none focus:ring-2 focus:ring-blue-500",
                isMobile ? "touch-target" : ""
              )}
            >
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <User className="w-4 h-4 text-white" />
              </div>
              {!isMobile && (
                <>
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    Admin
                  </span>
                  <ChevronDown className="w-4 h-4 text-gray-500 dark:text-gray-400" />
                </>
              )}
            </motion.button>

            {/* User Dropdown */}
            <AnimatePresence>
              {showUserMenu && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95, y: -10 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.95, y: -10 }}
                  transition={{ duration: 0.2 }}
                  className={cn(
                    "absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50",
                    isMobile && "-right-2"
                  )}
                >
                  <div className="py-2">
                    <button className="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-150 flex items-center space-x-2">
                      <User className="w-4 h-4" />
                      <span>Perfil</span>
                    </button>
                    <button className="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-150 flex items-center space-x-2">
                      <Settings className="w-4 h-4" />
                      <span>Configurações</span>
                    </button>
                    <hr className="my-2 border-gray-200 dark:border-gray-700" />
                    <button className="w-full px-4 py-2 text-left text-sm text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-150">
                      Sair
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>

      {/* Mobile Search Bar */}
      {isMobile && (
        <div className="px-4 pb-3">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Buscar..."
              className="mobile-input pl-10"
            />
          </div>
        </div>
      )}

      {/* Click outside to close dropdowns */}
      {(showUserMenu || showNotifications) && (
        <div 
          className="fixed inset-0 z-30" 
          onClick={() => {
            setShowUserMenu(false);
            setShowNotifications(false);
          }}
        />
      )}
    </header>
  );
};

export default Header;

