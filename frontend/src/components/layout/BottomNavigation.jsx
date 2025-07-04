import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Home, 
  Users, 
  MessageSquare, 
  Settings,
  BarChart3,
  Plus
} from 'lucide-react';

// Utils
import { cn } from '../../lib/utils';

const BottomNavigation = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const navigationItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: Home,
      path: '/dashboard',
      color: 'text-blue-600 dark:text-blue-400'
    },
    {
      id: 'clientes',
      label: 'Clientes',
      icon: Users,
      path: '/clientes',
      color: 'text-green-600 dark:text-green-400'
    },
    {
      id: 'add',
      label: 'Adicionar',
      icon: Plus,
      path: '/clientes/novo',
      color: 'text-white',
      special: true
    },
    {
      id: 'whatsapp',
      label: 'WhatsApp',
      icon: MessageSquare,
      path: '/whatsapp',
      color: 'text-emerald-600 dark:text-emerald-400'
    },
    {
      id: 'stats',
      label: 'Relatórios',
      icon: BarChart3,
      path: '/logs',
      color: 'text-purple-600 dark:text-purple-400'
    }
  ];

  const handleNavigation = (item) => {
    if (item.id === 'add') {
      // Ação especial para adicionar cliente
      // Pode abrir modal ou navegar para página de criação
      navigate('/clientes');
      // TODO: Abrir modal de criação de cliente
    } else {
      navigate(item.path);
    }
  };

  const isActive = (path) => {
    if (path === '/dashboard') {
      return location.pathname === '/' || location.pathname === '/dashboard';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <nav className="bottom-nav safe-area-bottom">
      <div className="flex items-center justify-around">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.path);

          if (item.special) {
            // Botão especial de adicionar (FAB style)
            return (
              <motion.button
                key={item.id}
                whileTap={{ scale: 0.9 }}
                onClick={() => handleNavigation(item)}
                className="relative -top-4 w-14 h-14 bg-blue-600 hover:bg-blue-700 rounded-full shadow-lg flex items-center justify-center transition-colors duration-200"
              >
                <Icon className="w-6 h-6 text-white" />
                
                {/* Ripple effect */}
                <motion.div
                  initial={{ scale: 0, opacity: 0.5 }}
                  animate={{ scale: 1.5, opacity: 0 }}
                  transition={{ duration: 0.6, repeat: Infinity }}
                  className="absolute inset-0 bg-blue-400 rounded-full"
                />
              </motion.button>
            );
          }

          return (
            <motion.button
              key={item.id}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleNavigation(item)}
              className={cn(
                "bottom-nav-item relative",
                active ? "bottom-nav-item-active" : "bottom-nav-item-inactive"
              )}
            >
              {/* Icon */}
              <div className="relative">
                <Icon className={cn(
                  "w-5 h-5 transition-colors duration-200",
                  active ? item.color : "text-gray-500 dark:text-gray-400"
                )} />
                
                {/* Active indicator */}
                {active && (
                  <motion.div
                    layoutId="activeIndicator"
                    className="absolute -top-1 -right-1 w-2 h-2 bg-blue-600 dark:bg-blue-400 rounded-full"
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                  />
                )}
              </div>

              {/* Label */}
              <span className={cn(
                "text-xs font-medium mt-1 transition-colors duration-200",
                active ? item.color : "text-gray-500 dark:text-gray-400"
              )}>
                {item.label}
              </span>

              {/* Background highlight */}
              {active && (
                <motion.div
                  layoutId="activeBackground"
                  className="absolute inset-0 bg-blue-50 dark:bg-blue-900/20 rounded-lg -z-10"
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                />
              )}
            </motion.button>
          );
        })}
      </div>

      {/* Background blur effect */}
      <div className="absolute inset-0 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg -z-20 rounded-t-2xl" />
      
      {/* Top border gradient */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-gray-200 dark:via-gray-700 to-transparent" />
    </nav>
  );
};

export default BottomNavigation;

