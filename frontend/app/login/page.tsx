'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { FiLock, FiUser, FiMail, FiPhone, FiArrowRight } from 'react-icons/fi';
import { useAuthStore } from '@/stores/authStore';
import { useConfigStore } from '@/stores/configStore';
import toast from 'react-hot-toast';

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirect = searchParams.get('redirect') || '/';
  const [isLogin, setIsLogin] = useState(true);
  
  const [loginData, setLoginData] = useState({
    username: '',
    password: '',
  });
  
  const [registroData, setRegistroData] = useState({
    email: '',
    password: '',
    password_confirm: '',
    first_name: '',
    last_name: '',
    telefono: '',
    dni: '',  // DNI obligatorio
  });
  
  const [isLoading, setIsLoading] = useState(false);
  
  const { login, registro, isAuthenticated } = useAuthStore();
  const { config, getLogo } = useConfigStore();
  // Asegurar que siempre tengamos un color válido - usar valor fijo para debug
  const colorPrimary = '#2563eb'; // Temporalmente fijo para verificar que funciona
  const logo = getLogo();

  useEffect(() => {
    if (isAuthenticated) {
      router.push(redirect);
    }
  }, [isAuthenticated, router, redirect]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      await login(loginData.username, loginData.password);
      toast.success('Sesión iniciada correctamente');
      setTimeout(() => {
        router.push(redirect);
      }, 1000);
    } catch (error: any) {
      toast.error(error.response?.data?.error || error.message || 'Error al iniciar sesión');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegistro = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (registroData.password !== registroData.password_confirm) {
      toast.error('Las contraseñas no coinciden');
      return;
    }
    
    setIsLoading(true);
    
    try {
      // SIEMPRE crear como minorista
      // El username se genera automáticamente desde el email en el backend
      await registro({
        ...registroData,
        tipo_usuario: 'MINORISTA', // Forzar minorista
      });
      toast.success('Cuenta creada exitosamente');
      router.push(redirect);
    } catch (error: any) {
      toast.error(error.response?.data?.error || error.message || 'Error al registrar');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full"
      >
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {/* Logo */}
          <div className="text-center mb-8">
            {logo ? (
              <img src={logo} alt={config?.nombre_comercial || 'Logo'} className="h-16 mx-auto mb-4" />
            ) : (
              <h2 className="text-3xl font-bold" style={{ color: colorPrimary }}>
                {config?.nombre_comercial || 'ImportStore'}
              </h2>
            )}
            <p className="text-gray-600 mt-2">
              {isLogin ? 'Iniciar sesión en tu cuenta' : 'Crear una nueva cuenta'}
            </p>
          </div>

          {/* Toggle Login/Registro */}
          <div className="flex mb-6 bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setIsLogin(true)}
              className={`flex-1 py-2 px-4 rounded-md text-sm font-semibold transition-colors ${
                isLogin
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Iniciar Sesión
            </button>
            <button
              onClick={() => setIsLogin(false)}
              className={`flex-1 py-2 px-4 rounded-md text-sm font-semibold transition-colors ${
                !isLogin
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Registrarse
            </button>
          </div>

          <AnimatePresence mode="wait">
            {isLogin ? (
              <motion.form
                key="login"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                onSubmit={handleLogin}
                className="space-y-6"
              >
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email
                  </label>
                  <div className="relative">
                    <FiMail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <input
                      type="email"
                      required
                      value={loginData.username}
                      onChange={(e) => {
                        setLoginData((prev) => ({ ...prev, username: e.target.value }));
                      }}
                      className="w-full pl-10 pr-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                      placeholder="tu@email.com"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Contraseña
                  </label>
                  <div className="relative">
                    <FiLock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <input
                      type="password"
                      required
                      value={loginData.password}
                      onChange={(e) => {
                        setLoginData((prev) => ({ ...prev, password: e.target.value }));
                      }}
                      className="w-full pl-10 pr-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                      placeholder="Contraseña"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full px-6 py-3 rounded-full font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl bg-blue-600 text-white hover:bg-blue-700"
                >
                  {isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
                </button>
              </motion.form>
            ) : (
              <motion.form
                key="registro"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                onSubmit={handleRegistro}
                className="space-y-4"
              >
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Nombre
                    </label>
                    <input
                      type="text"
                      value={registroData.first_name}
                      onChange={(e) => setRegistroData((prev) => ({ ...prev, first_name: e.target.value }))}
                      className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Apellido
                    </label>
                    <input
                      type="text"
                      value={registroData.last_name}
                      onChange={(e) => setRegistroData((prev) => ({ ...prev, last_name: e.target.value }))}
                      className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email *
                  </label>
                  <div className="relative">
                    <FiMail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <input
                      type="email"
                      required
                      value={registroData.email}
                      onChange={(e) => setRegistroData((prev) => ({ ...prev, email: e.target.value }))}
                      className="w-full pl-10 pr-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                      placeholder="tu@email.com"
                    />
                  </div>
                  <p className="text-xs text-gray-500 mt-1">El email será tu usuario para iniciar sesión</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    DNI *
                  </label>
                  <input
                    type="text"
                    required
                    value={registroData.dni}
                    onChange={(e) => setRegistroData((prev) => ({ ...prev, dni: e.target.value }))}
                    className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                    placeholder="12345678"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Teléfono/WhatsApp
                  </label>
                  <div className="relative">
                    <FiPhone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <input
                      type="tel"
                      value={registroData.telefono}
                      onChange={(e) => setRegistroData((prev) => ({ ...prev, telefono: e.target.value }))}
                      className="w-full pl-10 pr-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Contraseña *
                  </label>
                  <div className="relative">
                    <FiLock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <input
                      type="password"
                      required
                      value={registroData.password}
                      onChange={(e) => setRegistroData((prev) => ({ ...prev, password: e.target.value }))}
                      className="w-full pl-10 pr-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Confirmar Contraseña *
                  </label>
                  <div className="relative">
                    <FiLock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <input
                      type="password"
                      required
                      value={registroData.password_confirm}
                      onChange={(e) => setRegistroData((prev) => ({ ...prev, password_confirm: e.target.value }))}
                      className="w-full pl-10 pr-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full px-6 py-3 rounded-full font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl bg-blue-600 text-white hover:bg-blue-700"
                >
                  {isLoading ? 'Creando cuenta...' : 'Crear Cuenta Minorista'}
                </button>

                <div className="text-center mt-4">
                  <p className="text-sm text-gray-600 mb-2">
                    ¿Necesitás una cuenta mayorista?
                  </p>
                  <Link
                    href="/solicitar-mayorista"
                    className="text-sm font-semibold inline-flex items-center gap-1"
                    style={{ color: colorPrimary }}
                  >
                    Solicitar cuenta mayorista
                    <FiArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </motion.form>
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    </div>
  );
}
