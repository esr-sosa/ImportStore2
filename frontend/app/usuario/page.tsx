'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { FiUser, FiLogOut, FiShoppingBag, FiPackage, FiFileText, FiArrowRight, FiCheckCircle, FiXCircle, FiClock, FiEdit2, FiLock, FiSave, FiX } from 'react-icons/fi';
import { useAuthStore } from '@/stores/authStore';
import { api, Pedido } from '@/lib/api';
import toast from 'react-hot-toast';

export default function UsuarioPage() {
  const router = useRouter();
  const { user, isAuthenticated, logout, checkAuth, actualizarPerfil } = useAuthStore();
  const [pedidos, setPedidos] = useState<Pedido[]>([]);
  const [isLoadingPedidos, setIsLoadingPedidos] = useState(true);
  const [activeTab, setActiveTab] = useState<'perfil' | 'pedidos' | 'editar' | 'contraseña'>('perfil');
  
  // Estados para edición
  const [editando, setEditando] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    telefono: '',
    documento: '',
    direccion: '',
    ciudad: '',
  });
  const [isSaving, setIsSaving] = useState(false);
  
  // Estados para cambio de contraseña
  const [passwordData, setPasswordData] = useState({
    contraseña_actual: '',
    nueva_contraseña: '',
    confirmar_contraseña: '',
  });
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const hasInitializedRef = useRef(false);

  // Inicializar solo una vez al montar
  useEffect(() => {
    if (!hasInitializedRef.current) {
      hasInitializedRef.current = true;
      checkAuth();
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Redirigir si no está autenticado
  useEffect(() => {
    if (hasInitializedRef.current && !isAuthenticated) {
      router.push('/login?redirect=/usuario');
    }
  }, [isAuthenticated, router]);

  // Cargar pedidos cuando esté autenticado (solo una vez)
  const hasLoadedPedidosRef = useRef(false);
  useEffect(() => {
    if (isAuthenticated && hasInitializedRef.current && !hasLoadedPedidosRef.current) {
      hasLoadedPedidosRef.current = true;
      loadPedidos();
    }
  }, [isAuthenticated]); // eslint-disable-line react-hooks/exhaustive-deps

  // Actualizar formData solo cuando el usuario cambie (evitar loops)
  const lastUserIdRef = useRef<number | null>(null);
  useEffect(() => {
    if (user && user.id && user.id !== lastUserIdRef.current) {
      lastUserIdRef.current = user.id;
      setFormData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
        telefono: user.telefono || '',
        documento: user.documento || '',
        direccion: user.direccion || '',
        ciudad: user.ciudad || '',
      });
    }
  }, [user?.id]); // Solo cuando cambie el ID del usuario

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

  const handleSaveProfile = async () => {
    try {
      setIsSaving(true);
      const response = await api.actualizarPerfil(formData);
      if (response.success) {
        await actualizarPerfil(response.user);
        toast.success('Perfil actualizado correctamente');
        setEditando(false);
        // No necesitamos llamar checkAuth aquí, actualizarPerfil ya actualiza el estado
      }
    } catch (error: any) {
      console.error('Error actualizando perfil:', error);
      toast.error(error.response?.data?.error || 'Error al actualizar el perfil');
    } finally {
      setIsSaving(false);
    }
  };

  const handleChangePassword = async () => {
    if (passwordData.nueva_contraseña !== passwordData.confirmar_contraseña) {
      toast.error('Las contraseñas no coinciden');
      return;
    }
    
    if (passwordData.nueva_contraseña.length < 8) {
      toast.error('La contraseña debe tener al menos 8 caracteres');
      return;
    }

    try {
      setIsChangingPassword(true);
      const response = await api.cambiarContraseña(passwordData);
      if (response.success) {
        toast.success('Contraseña actualizada correctamente');
        setPasswordData({
          contraseña_actual: '',
          nueva_contraseña: '',
          confirmar_contraseña: '',
        });
        setActiveTab('perfil');
      }
    } catch (error: any) {
      console.error('Error cambiando contraseña:', error);
      toast.error(error.response?.data?.error || 'Error al cambiar la contraseña');
    } finally {
      setIsChangingPassword(false);
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

        {/* Tabs */}
        <div className="mb-6 border-b border-gray-200">
          <nav className="flex space-x-8">
            {[
              { id: 'perfil', label: 'Mi Perfil', icon: FiUser },
              { id: 'pedidos', label: 'Mis Pedidos', icon: FiPackage },
              { id: 'editar', label: 'Editar Perfil', icon: FiEdit2 },
              { id: 'contraseña', label: 'Cambiar Contraseña', icon: FiLock },
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-black text-black'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Contenido de las tabs */}
        {activeTab === 'perfil' && (
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
        )}

        {activeTab === 'editar' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100"
          >
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Editar Perfil</h2>
            
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nombre
                  </label>
                  <input
                    type="text"
                    value={formData.first_name}
                    onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-black"
                    placeholder="Nombre"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Apellido
                  </label>
                  <input
                    type="text"
                    value={formData.last_name}
                    onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-black"
                    placeholder="Apellido"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email *
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-black"
                  placeholder="email@ejemplo.com"
                  required
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Teléfono/WhatsApp
                  </label>
                  <input
                    type="tel"
                    value={formData.telefono}
                    onChange={(e) => setFormData({ ...formData, telefono: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-black"
                    placeholder="+54 9 11 1234-5678"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    DNI
                  </label>
                  <input
                    type="text"
                    value={formData.documento}
                    onChange={(e) => setFormData({ ...formData, documento: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-black"
                    placeholder="12345678"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Dirección
                </label>
                <input
                  type="text"
                  value={formData.direccion}
                  onChange={(e) => setFormData({ ...formData, direccion: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-black"
                  placeholder="Calle y número"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Ciudad
                </label>
                <input
                  type="text"
                  value={formData.ciudad}
                  onChange={(e) => setFormData({ ...formData, ciudad: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-black"
                  placeholder="Ciudad"
                />
              </div>

              <div className="flex space-x-4 pt-4">
                <motion.button
                  onClick={handleSaveProfile}
                  disabled={isSaving}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="flex items-center space-x-2 px-6 py-3 bg-black text-white rounded-lg font-semibold hover:bg-gray-800 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <FiSave className="w-4 h-4" />
                  <span>{isSaving ? 'Guardando...' : 'Guardar Cambios'}</span>
                </motion.button>
                <motion.button
                  onClick={() => {
                    setFormData({
                      first_name: user.first_name || '',
                      last_name: user.last_name || '',
                      email: user.email || '',
                      telefono: user.telefono || '',
                      documento: user.documento || '',
                      direccion: user.direccion || '',
                      ciudad: user.ciudad || '',
                    });
                  }}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="flex items-center space-x-2 px-6 py-3 bg-gray-100 text-gray-700 rounded-lg font-semibold hover:bg-gray-200 transition-all"
                >
                  <FiX className="w-4 h-4" />
                  <span>Cancelar</span>
                </motion.button>
              </div>
            </div>
          </motion.div>
        )}

        {activeTab === 'contraseña' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100"
          >
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Cambiar Contraseña</h2>
            
            <div className="space-y-4 max-w-md">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Contraseña Actual *
                </label>
                <input
                  type="password"
                  value={passwordData.contraseña_actual}
                  onChange={(e) => setPasswordData({ ...passwordData, contraseña_actual: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-black"
                  placeholder="Ingresa tu contraseña actual"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nueva Contraseña *
                </label>
                <input
                  type="password"
                  value={passwordData.nueva_contraseña}
                  onChange={(e) => setPasswordData({ ...passwordData, nueva_contraseña: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-black"
                  placeholder="Mínimo 8 caracteres"
                  required
                />
                <p className="text-xs text-gray-500 mt-1">La contraseña debe tener al menos 8 caracteres</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Confirmar Nueva Contraseña *
                </label>
                <input
                  type="password"
                  value={passwordData.confirmar_contraseña}
                  onChange={(e) => setPasswordData({ ...passwordData, confirmar_contraseña: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-black"
                  placeholder="Confirma tu nueva contraseña"
                  required
                />
              </div>

              <motion.button
                onClick={handleChangePassword}
                disabled={isChangingPassword || !passwordData.contraseña_actual || !passwordData.nueva_contraseña || !passwordData.confirmar_contraseña}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-full flex items-center justify-center space-x-2 px-6 py-3 bg-black text-white rounded-lg font-semibold hover:bg-gray-800 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <FiLock className="w-4 h-4" />
                <span>{isChangingPassword ? 'Cambiando...' : 'Cambiar Contraseña'}</span>
              </motion.button>
            </div>
          </motion.div>
        )}

        {activeTab === 'pedidos' && (
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
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Link
                    href="/productos"
                    className="inline-block mt-4 px-6 py-2 bg-black text-white rounded-full font-semibold hover:bg-gray-800 transition-all shadow-lg hover:shadow-xl"
                  >
                    Ver Productos
                  </Link>
                </motion.div>
              </div>
            )}
          </motion.div>
        )}

        {/* Acciones Rápidas */}
        {activeTab === 'perfil' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mt-6 bg-white rounded-2xl p-6 shadow-sm border border-gray-100"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Acciones</h3>
            <div className="space-y-3">
              <motion.div whileHover={{ x: 4 }}>
                <Link
                  href="/productos"
                  className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-all text-gray-900 font-medium shadow-sm hover:shadow-md"
                >
                  <span className="flex items-center">
                    <FiShoppingBag className="mr-2" />
                    Ver Productos
                  </span>
                  <FiArrowRight className="w-4 h-4" />
                </Link>
              </motion.div>
              <motion.div whileHover={{ x: 4 }}>
                <Link
                  href="/carrito"
                  className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-all text-gray-900 font-medium shadow-sm hover:shadow-md"
                >
                  <span className="flex items-center">
                    <FiShoppingBag className="mr-2" />
                    Mi Carrito
                  </span>
                  <FiArrowRight className="w-4 h-4" />
                </Link>
              </motion.div>
              <motion.button
                onClick={handleLogout}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-full flex items-center justify-between px-4 py-3 bg-red-50 hover:bg-red-100 text-red-700 rounded-lg transition-all font-medium shadow-sm hover:shadow-md"
              >
                <span className="flex items-center">
                  <FiLogOut className="mr-2" />
                  Cerrar Sesión
                </span>
              </motion.button>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
