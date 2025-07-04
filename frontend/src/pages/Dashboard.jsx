import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Users, 
  DollarSign, 
  TrendingUp, 
  AlertTriangle,
  Calendar,
  MessageSquare,
  RefreshCw,
  Eye,
  Filter,
  Download
} from 'lucide-react';
import { 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell,
  LineChart,
  Line,
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Legend
} from 'recharts';

// Hooks
import { useQuery } from '@tanstack/react-query';

// API
import { clientesAPI } from '../lib/api';

// Utils
import { formatarMoeda, formatarData, cn } from '../lib/utils';

const Dashboard = ({ isMobile = false }) => {
  const [filtroTempo, setFiltroTempo] = useState('30d');
  const [tipoProdutoSelecionado, setTipoProdutoSelecionado] = useState('todos');

  // Queries para dados do dashboard
  const { data: dashboardIPTV } = useQuery({
    queryKey: ['dashboard', 'IPTV'],
    queryFn: () => clientesAPI.dashboard('IPTV'),
  });

  const { data: dashboardVPN } = useQuery({
    queryKey: ['dashboard', 'VPN'],
    queryFn: () => clientesAPI.dashboard('VPN'),
  });

  const { data: dashboardOUTROS } = useQuery({
    queryKey: ['dashboard', 'OUTROS'],
    queryFn: () => clientesAPI.dashboard('OUTROS'),
  });

  // Dados mockados para demonstração
  const dadosReceita = [
    { mes: 'Jan', IPTV: 4500, VPN: 2300, OUTROS: 800 },
    { mes: 'Fev', IPTV: 5200, VPN: 2800, OUTROS: 1200 },
    { mes: 'Mar', IPTV: 4800, VPN: 3100, OUTROS: 900 },
    { mes: 'Abr', IPTV: 6100, VPN: 3500, OUTROS: 1500 },
    { mes: 'Mai', IPTV: 7200, VPN: 4200, OUTROS: 1800 },
    { mes: 'Jun', IPTV: 8500, VPN: 4800, OUTROS: 2100 },
  ];

  const dadosVencimentos = [
    { dia: 'Seg', vencimentos: 12, renovacoes: 8 },
    { dia: 'Ter', vencimentos: 19, renovacoes: 15 },
    { dia: 'Qua', vencimentos: 8, renovacoes: 6 },
    { dia: 'Qui', vencimentos: 25, renovacoes: 18 },
    { dia: 'Sex', vencimentos: 15, renovacoes: 12 },
    { dia: 'Sab', vencimentos: 7, renovacoes: 5 },
    { dia: 'Dom', vencimentos: 3, renovacoes: 2 },
  ];

  const dadosDistribuicao = [
    { nome: 'IPTV', valor: 65, cor: '#3B82F6' },
    { nome: 'VPN', valor: 25, cor: '#10B981' },
    { nome: 'OUTROS', valor: 10, cor: '#F59E0B' },
  ];

  // Métricas principais
  const metricas = [
    {
      titulo: 'Total de Clientes',
      valor: '1,247',
      mudanca: '+12%',
      tendencia: 'up',
      icon: Users,
      cor: 'blue',
      descricao: 'vs mês anterior'
    },
    {
      titulo: 'Receita Mensal',
      valor: 'R$ 18.650',
      mudanca: '+8.2%',
      tendencia: 'up',
      icon: DollarSign,
      cor: 'green',
      descricao: 'vs mês anterior'
    },
    {
      titulo: 'Taxa de Renovação',
      valor: '94.5%',
      mudanca: '+2.1%',
      tendencia: 'up',
      icon: RefreshCw,
      cor: 'purple',
      descricao: 'últimos 30 dias'
    },
    {
      titulo: 'Vencimentos Hoje',
      valor: '23',
      mudanca: '-5',
      tendencia: 'down',
      icon: AlertTriangle,
      cor: 'orange',
      descricao: 'clientes'
    }
  ];

  const MetricCard = ({ metrica, index }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className={cn(
        "bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 hover-lift",
        isMobile && "mobile-card"
      )}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className={cn(
            "p-3 rounded-lg",
            metrica.cor === 'blue' && "bg-blue-100 dark:bg-blue-900/20",
            metrica.cor === 'green' && "bg-green-100 dark:bg-green-900/20",
            metrica.cor === 'purple' && "bg-purple-100 dark:bg-purple-900/20",
            metrica.cor === 'orange' && "bg-orange-100 dark:bg-orange-900/20"
          )}>
            <metrica.icon className={cn(
              "w-6 h-6",
              metrica.cor === 'blue' && "text-blue-600 dark:text-blue-400",
              metrica.cor === 'green' && "text-green-600 dark:text-green-400",
              metrica.cor === 'purple' && "text-purple-600 dark:text-purple-400",
              metrica.cor === 'orange' && "text-orange-600 dark:text-orange-400"
            )} />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
              {metrica.titulo}
            </p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white">
              {metrica.valor}
            </p>
          </div>
        </div>
        <div className="text-right">
          <div className={cn(
            "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
            metrica.tendencia === 'up' 
              ? "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400"
              : "bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400"
          )}>
            <TrendingUp className={cn(
              "w-3 h-3 mr-1",
              metrica.tendencia === 'down' && "rotate-180"
            )} />
            {metrica.mudanca}
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
            {metrica.descricao}
          </p>
        </div>
      </div>
    </motion.div>
  );

  const ChartCard = ({ titulo, children, actions }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn(
        "bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6",
        isMobile && "mobile-card"
      )}
    >
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          {titulo}
        </h3>
        {actions && (
          <div className="flex items-center space-x-2">
            {actions}
          </div>
        )}
      </div>
      {children}
    </motion.div>
  );

  return (
    <div className={cn(
      "space-y-6",
      isMobile ? "mobile-container" : "max-w-7xl mx-auto"
    )}>
      {/* Header */}
      <div className="flex flex-col space-y-4 md:flex-row md:items-center md:justify-between md:space-y-0">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Visão geral do sistema de vencimentos
          </p>
        </div>
        
        <div className="flex items-center space-x-3">
          {/* Filtro de tempo */}
          <select
            value={filtroTempo}
            onChange={(e) => setFiltroTempo(e.target.value)}
            className={cn(
              "px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
              isMobile && "mobile-input"
            )}
          >
            <option value="7d">Últimos 7 dias</option>
            <option value="30d">Últimos 30 dias</option>
            <option value="90d">Últimos 90 dias</option>
            <option value="1y">Último ano</option>
          </select>

          {/* Botão de atualizar */}
          <motion.button
            whileTap={{ scale: 0.95 }}
            className={cn(
              "p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200",
              isMobile && "touch-target"
            )}
          >
            <RefreshCw className="w-4 h-4" />
          </motion.button>
        </div>
      </div>

      {/* Métricas principais */}
      <div className={cn(
        "grid gap-6",
        isMobile ? "grid-cols-1" : "grid-cols-1 md:grid-cols-2 lg:grid-cols-4"
      )}>
        {metricas.map((metrica, index) => (
          <MetricCard key={metrica.titulo} metrica={metrica} index={index} />
        ))}
      </div>

      {/* Gráficos principais */}
      <div className={cn(
        "grid gap-6",
        isMobile ? "grid-cols-1" : "grid-cols-1 lg:grid-cols-2"
      )}>
        {/* Gráfico de receita */}
        <ChartCard 
          titulo="Receita por Categoria"
          actions={
            <button className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200">
              <Download className="w-4 h-4" />
            </button>
          }
        >
          <div className={cn(
            "h-80",
            isMobile && "mobile-chart"
          )}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={dadosReceita}>
                <defs>
                  <linearGradient id="colorIPTV" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#3B82F6" stopOpacity={0.1}/>
                  </linearGradient>
                  <linearGradient id="colorVPN" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#10B981" stopOpacity={0.1}/>
                  </linearGradient>
                  <linearGradient id="colorOUTROS" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#F59E0B" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#F59E0B" stopOpacity={0.1}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                <XAxis 
                  dataKey="mes" 
                  stroke="#6B7280"
                  fontSize={12}
                />
                <YAxis 
                  stroke="#6B7280"
                  fontSize={12}
                  tickFormatter={(value) => `R$ ${value}`}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                    color: '#F9FAFB'
                  }}
                  formatter={(value) => [`R$ ${value}`, '']}
                />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="IPTV"
                  stackId="1"
                  stroke="#3B82F6"
                  fillOpacity={1}
                  fill="url(#colorIPTV)"
                />
                <Area
                  type="monotone"
                  dataKey="VPN"
                  stackId="1"
                  stroke="#10B981"
                  fillOpacity={1}
                  fill="url(#colorVPN)"
                />
                <Area
                  type="monotone"
                  dataKey="OUTROS"
                  stackId="1"
                  stroke="#F59E0B"
                  fillOpacity={1}
                  fill="url(#colorOUTROS)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        {/* Gráfico de vencimentos */}
        <ChartCard titulo="Vencimentos da Semana">
          <div className={cn(
            "h-80",
            isMobile && "mobile-chart"
          )}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={dadosVencimentos}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                <XAxis 
                  dataKey="dia" 
                  stroke="#6B7280"
                  fontSize={12}
                />
                <YAxis 
                  stroke="#6B7280"
                  fontSize={12}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                    color: '#F9FAFB'
                  }}
                />
                <Legend />
                <Bar 
                  dataKey="vencimentos" 
                  fill="#EF4444" 
                  name="Vencimentos"
                  radius={[4, 4, 0, 0]}
                />
                <Bar 
                  dataKey="renovacoes" 
                  fill="#10B981" 
                  name="Renovações"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      {/* Gráficos secundários */}
      <div className={cn(
        "grid gap-6",
        isMobile ? "grid-cols-1" : "grid-cols-1 md:grid-cols-3"
      )}>
        {/* Distribuição por tipo */}
        <ChartCard titulo="Distribuição por Tipo">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={dadosDistribuicao}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="valor"
                >
                  {dadosDistribuicao.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.cor} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{
                    backgroundColor: '#1F2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                    color: '#F9FAFB'
                  }}
                  formatter={(value) => [`${value}%`, '']}
                />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        {/* Atividade recente */}
        <div className={cn(
          "md:col-span-2 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6",
          isMobile && "mobile-card"
        )}>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Atividade Recente
          </h3>
          <div className="space-y-4">
            {[
              { tipo: 'renovacao', cliente: 'João Silva', acao: 'renovou IPTV por 30 dias', tempo: '2 min atrás', valor: 'R$ 45,00' },
              { tipo: 'vencimento', cliente: 'Maria Santos', acao: 'vence hoje - VPN', tempo: '5 min atrás', valor: 'R$ 25,00' },
              { tipo: 'pagamento', cliente: 'Pedro Costa', acao: 'pagou IPTV', tempo: '10 min atrás', valor: 'R$ 50,00' },
              { tipo: 'novo', cliente: 'Ana Oliveira', acao: 'novo cliente - OUTROS', tempo: '15 min atrás', valor: 'R$ 30,00' },
            ].map((atividade, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-150"
              >
                <div className="flex items-center space-x-3">
                  <div className={cn(
                    "w-2 h-2 rounded-full",
                    atividade.tipo === 'renovacao' && "bg-green-500",
                    atividade.tipo === 'vencimento' && "bg-red-500",
                    atividade.tipo === 'pagamento' && "bg-blue-500",
                    atividade.tipo === 'novo' && "bg-purple-500"
                  )} />
                  <div>
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {atividade.cliente}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {atividade.acao}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">
                    {atividade.valor}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    {atividade.tempo}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

