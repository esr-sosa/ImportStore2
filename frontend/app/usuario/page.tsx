'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { FiUser, FiLogOut, FiShoppingBag, FiPackage } from 'react-icons/fi';
import { useAuthStore } from '@/stores/authStore';
import toast from 'react-hot-toast';

export default function UsuarioPage() {
  const router = useRouter();
  const { user, isAuthenticated, logout, checkAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
    if (!isAuthenticated) {
      router.push('/login?redirect=/usuario');
    }
  }, [isAuthenticated, router, checkAuth]);

  const handleLogout = async () => {
    try {
      await logout();
      toast.success('Sesión cerrada');
      router.push('/');
    } catch (error) {
      toast.error('Error al cerrar sesión');
    }
  };

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Mi Cuenta</h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Información del Usuario */}
          <div className="md:col-span-2 space-y-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-2xl p-6 shadow-sm"
            >
              <div className="flex items-center space-x-4 mb-6">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
                  <FiUser className="w-8 h-8 text-blue-600" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">
                    {user.first_name && user.last_name
                      ? `${user.first_name} ${user.last_name}`
                      : user.username}
                  </h2>
                  <p className="text-gray-500">{user.email || 'Sin email'}</p>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Usuario
                  </label>
                  <p className="text-gray-900">{user.username}</p>
                </div>
                {user.email && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Email
                    </label>
                    <p className="text-gray-900">{user.email}</p>
                  </div>
                )}
              </div>
            </motion.div>

            {/* Mis Pedidos */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white rounded-2xl p-6 shadow-sm"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <FiPackage className="mr-2" />
                Mis Pedidos
              </h3>
              <p className="text-gray-500 text-sm">
                Próximamente podrás ver el historial de tus pedidos aquí.
              </p>
            </motion.div>
          </div>

          {/* Acciones Rápidas */}
          <div className="space-y-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white rounded-2xl p-6 shadow-sm"
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Acciones</h3>
              <div className="space-y-3">
                <button
                  onClick={() => router.push('/productos')}
                  className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <span className="flex items-center">
                    <FiShoppingBag className="mr-2" />
                    Ver Productos
                  </span>
                </button>
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

