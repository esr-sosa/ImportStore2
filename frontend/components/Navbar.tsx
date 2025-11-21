'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { FiShoppingCart, FiUser, FiMenu, FiX, FiSearch, FiHeart } from 'react-icons/fi';
import { useCartStore } from '@/stores/cartStore';
import { useAuthStore } from '@/stores/authStore';
import { useConfigStore } from '@/stores/configStore';
import SearchAutocomplete from './SearchAutocomplete';
import { getTextColorClass, getTextColorStyle } from '@/lib/colorUtils';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [showSearch, setShowSearch] = useState(false);
  const { total_items, loadCarrito } = useCartStore();
  const { user, isAuthenticated, logout } = useAuthStore();
  const { config, getLogo } = useConfigStore();

  useEffect(() => {
    loadCarrito();
  }, [loadCarrito]);

  const logo = getLogo();
  const colorPrimary = config?.color_principal || '#2563eb';

  return (
    <>
      <nav className="sticky top-0 z-50 bg-white/95 backdrop-blur-xl border-b border-gray-200/50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20 md:h-24">
            {/* Logo - Mejorado con animación sutil */}
            <Link 
              href="/" 
              className="flex items-center space-x-3 group"
            >
              <motion.div
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                transition={{ type: 'spring', stiffness: 400, damping: 17 }}
              >
                {logo ? (
                  <img 
                    src={logo} 
                    alt={config?.nombre_comercial || 'Logo'} 
                    className="h-14 md:h-16 w-auto transition-opacity group-hover:opacity-90 object-contain" 
                  />
                ) : (
                  <span 
                    className="text-2xl md:text-3xl font-display font-bold tracking-tight" 
                    style={{ color: colorPrimary }}
                  >
                    {config?.nombre_comercial || 'ImportStore'}
                  </span>
                )}
              </motion.div>
            </Link>

            {/* Desktop Navigation - Mejorado */}
            <div className="hidden md:flex items-center space-x-1">
              <Link 
                href="/" 
                className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 rounded-lg hover:bg-gray-50 transition-all duration-200 relative group"
              >
                Inicio
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-current group-hover:w-full transition-all duration-300"></span>
              </Link>
              <Link 
                href="/productos" 
                className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 rounded-lg hover:bg-gray-50 transition-all duration-200 relative group"
              >
                Productos
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-current group-hover:w-full transition-all duration-300"></span>
              </Link>
              <Link 
                href="/categorias" 
                className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900 rounded-lg hover:bg-gray-50 transition-all duration-200 relative group"
              >
                Categorías
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-current group-hover:w-full transition-all duration-300"></span>
              </Link>
            </div>

            {/* Search Bar - Desktop */}
            <div className="hidden lg:flex flex-1 max-w-md mx-8">
              <SearchAutocomplete />
            </div>

            {/* Actions */}
            <div className="flex items-center space-x-4">
              {/* Search Button - Mobile/Tablet */}
              <button
                onClick={() => setShowSearch(!showSearch)}
                className="lg:hidden p-2 text-gray-700 hover:text-gray-900 transition-colors"
              >
                <FiSearch className="w-6 h-6" />
              </button>

              {/* Favoritos */}
              {isAuthenticated && (
                <Link
                  href="/favoritos"
                  className="p-2 text-gray-700 hover:text-gray-900 transition-colors"
                >
                  <FiHeart className="w-6 h-6" />
                </Link>
              )}
              
              {/* Cart */}
              <Link
                href="/carrito"
                data-cart-button
                className="relative p-2 text-gray-700 hover:text-gray-900 transition-colors"
              >
                <motion.div
                  animate={{}}
                  transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                >
                  <FiShoppingCart className="w-6 h-6" />
                </motion.div>
                {total_items > 0 && (
                  <motion.span
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-semibold"
                  >
                    {total_items > 99 ? '99+' : total_items}
                  </motion.span>
                )}
              </Link>

              {/* User Menu */}
              {isAuthenticated ? (
                <div className="relative group">
                  <button className="p-2 text-gray-700 hover:text-gray-900 transition-colors">
                    <FiUser className="w-6 h-6" />
                  </button>
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                    <Link
                      href="/usuario"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                    >
                      Mi Perfil
                    </Link>
                    <Link
                      href="/historial"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                    >
                      Historial
                    </Link>
                    <button
                      onClick={logout}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                    >
                      Cerrar Sesión
                    </button>
                  </div>
                </div>
              ) : (
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <Link
                    href="/login"
                    className={`px-6 py-2.5 rounded-full font-display font-semibold text-sm transition-all shadow-md hover:shadow-lg ${getTextColorClass(colorPrimary)}`}
                    style={{ backgroundColor: colorPrimary, ...getTextColorStyle(colorPrimary) }}
                  >
                    Iniciar Sesión
                  </Link>
                </motion.div>
              )}

              {/* Mobile Menu Button */}
              <button
                onClick={() => setIsOpen(!isOpen)}
                className="md:hidden p-2 text-gray-700"
              >
                {isOpen ? <FiX className="w-6 h-6" /> : <FiMenu className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Search */}
        <AnimatePresence>
          {showSearch && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="lg:hidden border-t border-gray-200 px-4 py-3"
            >
              <SearchAutocomplete onClose={() => setShowSearch(false)} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Mobile Menu */}
        <AnimatePresence>
          {isOpen && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="md:hidden border-t border-gray-200"
            >
              <div className="px-4 py-4 space-y-3">
                <Link
                  href="/"
                  onClick={() => setIsOpen(false)}
                  className="block text-gray-700 hover:text-gray-900"
                >
                  Inicio
                </Link>
                <Link
                  href="/productos"
                  onClick={() => setIsOpen(false)}
                  className="block text-gray-700 hover:text-gray-900"
                >
                  Productos
                </Link>
                <Link
                  href="/categorias"
                  onClick={() => setIsOpen(false)}
                  className="block text-gray-700 hover:text-gray-900"
                >
                  Categorías
                </Link>
                {isAuthenticated && (
                  <>
                    <Link
                      href="/favoritos"
                      onClick={() => setIsOpen(false)}
                      className="block text-gray-700 hover:text-gray-900"
                    >
                      Favoritos
                    </Link>
                    <Link
                      href="/usuario"
                      onClick={() => setIsOpen(false)}
                      className="block text-gray-700 hover:text-gray-900"
                    >
                      Mi Perfil
                    </Link>
                    <Link
                      href="/historial"
                      onClick={() => setIsOpen(false)}
                      className="block text-gray-700 hover:text-gray-900"
                    >
                      Historial
                    </Link>
                    <button
                      onClick={() => {
                        logout();
                        setIsOpen(false);
                      }}
                      className="block w-full text-left text-gray-700 hover:text-gray-900"
                    >
                      Cerrar Sesión
                    </button>
                  </>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>
    </>
  );
}
