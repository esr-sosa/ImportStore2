'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { FiUser, FiLogOut, FiShoppingBag, FiPackage, FiFileText, FiArrowRight, FiCheckCircle, FiXCircle, FiClock } from 'react-icons/fi';
import { useAuthStore } from '@/stores/authStore';
import { api, Pedido } from '@/lib/api';
import toast from 'react-hot-toast';

export default function UsuarioPage() {
  const router = useRouter();
  const { user, isAuthenticated, logout, checkAuth } = useAuthStore();
  const [pedidos, setPedidos] = useState<Pedido[]>([]);
  const [isLoadingPedidos, setIsLoadingPedidos] = useState(true);

  useEffect(() => {
    checkAuth();
    if (!isAuthenticated) {
      router.push('/login?redirect=/usuario');
    } else {
      loadPedidos();
    }
  }, [isAuthenticated, router, checkAuth]);

  const loadPedidos = async () => {
    try {
      setIsLoadingPedidos(true);
      const data = await api.getPedidos();
      setPedidos(data.pedidos || []);
    } catch (error: any) {
      console.error('Error cargando pedidos:', error);
      toast.error('Error al cargar pedidos');
    } finally {
      setIsLoadingPedidos(false);
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      toast.success('Sesión cerrada');
      router.push('/');
    } catch (error) {
      toast.error('Error al cerrar sesión');
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'COMPLETADO':
        return <FiCheckCircle className="w-4 h-4 text-green-500" />;
      case 'CANCELADO':
      case 'DEVUELTO':
        return <FiXCircle className="w-4 h-4 text-red-500" />;
      default:
        return <FiClock className="w-4 h-4 text-yellow-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'COMPLETADO':
        return 'bg-green-100 text-green-700';
      case 'CANCELADO':
      case 'DEVUELTO':
        return 'bg-red-100 text-red-700';
      case 'PAGADO':
        return 'bg-blue-100 text-blue-700';
      default:
        return 'bg-yellow-100 text-yellow-700';
    }
  };

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Mi Cuenta</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Información del Usuario */}
          <div className="lg:col-span-2 space-y-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100"
            >
              <div className="flex items-center space-x-4 mb-6">
                <div className="w-16 h-16 bg-black rounded-full flex items-center justify-center">
                  <FiUser className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">
                    {user.first_name && user.last_name
                      ? `${user.first_name} ${user.last_name}`
                      : user.username}
                  </h2>
                  <p className="text-gray-600">{user.email || 'Sin email'}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Usuario
                  </label>
                  <p className="text-gray-900 font-semibold">{user.username}</p>
                </div>
                {user.email && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Email
                    </label>
                    <p className="text-gray-900">{user.email}</p>
                  </div>
                )}
                {user.documento && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      DNI
                    </label>
                    <p className="text-gray-900">{user.documento}</p>
                  </div>
                )}
                {user.telefono && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Teléfono
                    </label>
                    <p className="text-gray-900">{user.telefono}</p>
                  </div>
                )}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Tipo de Cuenta
                  </label>
                  <p className="text-gray-900">
                    <span className="px-2 py-1 bg-gray-100 rounded text-sm">
                      {user.tipo_usuario === 'MAYORISTA' ? 'Mayorista' : 'Minorista'}
                    </span>
                  </p>
                </div>
                {(user.direccion || user.ciudad) && (
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Dirección
                    </label>
                    <p className="text-gray-900">
                      {user.direccion || ''} {user.ciudad ? `, ${user.ciudad}` : ''}
                    </p>
                  </div>
                )}
              </div>
            </motion.div>

            {/* Mis Pedidos */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <FiPackage className="mr-2" />
                Mis Pedidos
              </h3>
              
              {isLoadingPedidos ? (
                <div className="space-y-3">
                  {[...Array(3)].map((_, i) => (
                    <div key={i} className="h-20 bg-gray-100 rounded-lg animate-pulse" />
                  ))}
                </div>
              ) : pedidos.length > 0 ? (
                <div className="space-y-3">
                  {pedidos.map((pedido) => (
                    <Link
                      key={pedido.id}
                      href={`/pedidos/${pedido.id}`}
                      className="block p-4 border border-gray-200 rounded-lg hover:border-gray-300 hover:shadow-md transition-all"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-2">
                            <span className="font-semibold text-gray-900">{pedido.id}</span>
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(pedido.status)}`}>
                              {pedido.status_display || pedido.status}
                            </span>
                            <span className="text-xs text-gray-500">
                              {pedido.origen_display || pedido.origen || 'Web'}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 mb-1">
                            {new Date(pedido.fecha).toLocaleDateString('es-AR', {
                              year: 'numeric',
                              month: 'long',
                              day: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit'
                            })}
                          </p>
                          <p className="text-sm text-gray-600">
                            {pedido.items_count} {pedido.items_count === 1 ? 'producto' : 'productos'} · 
                            {pedido.metodo_pago_display || pedido.metodo_pago}
                          </p>
                          {(pedido.status === 'CANCELADO' || pedido.status === 'DEVUELTO') && pedido.motivo_cancelacion && (
                            <p className="text-xs text-red-600 mt-2">
                              Motivo: {pedido.motivo_cancelacion}
                            </p>
                          )}
                        </div>
                        <div className="text-right ml-4">
                          <p className="text-lg font-bold text-gray-900">
                            ${pedido.total_ars.toLocaleString('es-AR', { maximumFractionDigits: 0 })}
                          </p>
                          <FiArrowRight className="w-5 h-5 text-gray-400 mt-2" />
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <FiPackage className="w-16 h-16 mx-auto text-gray-300 mb-4" />
                  <p className="text-gray-500">No tienes pedidos aún</p>
                  <Link
                    href="/productos"
                    className="inline-block mt-4 px-6 py-2 bg-black text-white rounded-full font-semibold hover:bg-gray-800 transition-colors"
                  >
                    Ver Productos
                  </Link>
                </div>
              )}
            </motion.div>
          </div>

          {/* Acciones Rápidas */}
          <div className="space-y-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Acciones</h3>
              <div className="space-y-3">
                <Link
                  href="/productos"
                  className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <span className="flex items-center">
                    <FiShoppingBag className="mr-2" />
                    Ver Productos
                  </span>
                  <FiArrowRight className="w-4 h-4" />
                </Link>
                <Link
                  href="/carrito"
                  className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <span className="flex items-center">
                    <FiShoppingBag className="mr-2" />
                    Mi Carrito
                  </span>
                  <FiArrowRight className="w-4 h-4" />
                </Link>
                <button
                  onClick={handleLogout}
                  className="w-full flex items-center justify-between px-4 py-3 bg-red-50 hover:bg-red-100 text-red-600 rounded-lg transition-colors"
                >
                  <span className="flex items-center">
                    <FiLogOut className="mr-2" />
                    Cerrar Sesión
                  </span>
                </button>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
