'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { FiPackage, FiCalendar, FiDollarSign, FiCheckCircle, FiClock } from 'react-icons/fi';
import { api, Pedido } from '@/lib/api';
import { useAuthStore } from '@/stores/authStore';
import ProtectedRoute from '@/components/ProtectedRoute';
import toast from 'react-hot-toast';

export default function HistorialPage() {
  return (
    <ProtectedRoute>
      <HistorialContent />
    </ProtectedRoute>
  );
}

function HistorialContent() {
  const router = useRouter();
  const [pedidos, setPedidos] = useState<Pedido[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadHistorial();
  }, []);

  const loadHistorial = async () => {
    setIsLoading(true);
    try {
      const { pedidos: pedidosData } = await api.getPedidos();
      setPedidos(pedidosData);
    } catch (error: any) {
      toast.error(error.message || 'Error al cargar historial');
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'PAGADO':
      case 'COMPLETADO':
        return 'bg-green-100 text-green-800';
      case 'PENDIENTE_PAGO':
        return 'bg-yellow-100 text-yellow-800';
      case 'CANCELADO':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'PAGADO':
      case 'COMPLETADO':
        return <FiCheckCircle className="w-4 h-4" />;
      case 'PENDIENTE_PAGO':
        return <FiClock className="w-4 h-4" />;
      default:
        return <FiPackage className="w-4 h-4" />;
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl p-12 animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-8" />
            <div className="space-y-4">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-24 bg-gray-200 rounded" />
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Historial de Pedidos</h1>

        {pedidos.length > 0 ? (
          <div className="space-y-4">
            {pedidos.map((pedido, index) => (
              <motion.div
                key={pedido.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                className="bg-white rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center space-x-4 mb-2">
                      <Link href={`/pedidos/${pedido.id}`} className="text-lg font-semibold text-gray-900 hover:text-blue-600 transition-colors">
                        {pedido.id}
                      </Link>
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(pedido.status)}`}>
                        {getStatusIcon(pedido.status)}
                        <span className="ml-1">{pedido.status_display || pedido.status.replace('_', ' ')}</span>
                      </span>
                      {pedido.origen_display && (
                        <span className="text-xs text-gray-500">({pedido.origen_display})</span>
                      )}
                    </div>
                    <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                      <div className="flex items-center">
                        <FiCalendar className="mr-2" />
                        {new Date(pedido.fecha).toLocaleDateString('es-AR', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric',
                        })}
                      </div>
                      {pedido.cliente_nombre && (
                        <div className="flex items-center">
                          <span>{pedido.cliente_nombre}</span>
                        </div>
                      )}
                      <div className="flex items-center">
                        <FiPackage className="mr-2" />
                        {pedido.items_count} {pedido.items_count === 1 ? 'item' : 'items'}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <div className="text-sm text-gray-500 mb-1">Total</div>
                      <div className="text-2xl font-bold text-gray-900 flex items-center">
                        <FiDollarSign className="w-5 h-5 mr-1" />
                        {pedido.total_ars.toLocaleString('es-AR', { maximumFractionDigits: 0 })}
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-2xl p-12 text-center">
            <FiPackage className="w-24 h-24 mx-auto text-gray-300 mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">No hay pedidos aún</h2>
            <p className="text-gray-500">Tus pedidos aparecerán aquí cuando realices una compra</p>
          </div>
        )}
      </div>
    </div>
  );
}

