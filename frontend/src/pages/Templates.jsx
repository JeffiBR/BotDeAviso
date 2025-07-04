import { motion } from 'framer-motion';
import { FileText } from 'lucide-react';
import { cn } from '../lib/utils';

const Templates = ({ isMobile = false }) => {
  return (
    <div className={cn(
      "space-y-6",
      isMobile ? "mobile-container" : "max-w-7xl mx-auto"
    )}>
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Templates
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Gerencie templates de mensagens
        </p>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className={cn(
          "bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6",
          isMobile && "mobile-card"
        )}
      >
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              Página em Desenvolvimento
            </h3>
            <p className="text-gray-500 dark:text-gray-400">
              A funcionalidade de templates será implementada em breve
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Templates;

