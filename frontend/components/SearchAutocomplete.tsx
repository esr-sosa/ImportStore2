'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import { motion, AnimatePresence } from 'framer-motion';
import { FiSearch, FiX } from 'react-icons/fi';
import { api, Producto } from '@/lib/api';
import { useAuthStore } from '@/stores/authStore';

interface SearchAutocompleteProps {
  onClose?: () => void;
}

export default function SearchAutocomplete({ onClose }: SearchAutocompleteProps) {
  const router = useRouter();
  const { user } = useAuthStore();
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<Producto[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const searchRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const debounceRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    // Cerrar al hacer click fuera
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    // Limpiar debounce anterior
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    if (query.length < 2) {
      setSuggestions([]);
      setShowSuggestions(false);
      return;
    }

    // Debounce de 250ms
    debounceRef.current = setTimeout(async () => {
      setIsLoading(true);
      try {
        const tipo_precio = user?.tipo_usuario || 'MINORISTA';
        const response = await api.getProductos({
          q: query,
          tipo_precio,
          page_size: 8, // Limitar a 8 resultados
        });
        setSuggestions(response.productos);
        setShowSuggestions(true);
      } catch (error) {
        console.error('Error en búsqueda:', error);
        setSuggestions([]);
      } finally {
        setIsLoading(false);
      }
    }, 250);

    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }
    };
  }, [query, user]);

  const handleSelectProduct = (product: Producto) => {
    setQuery('');
    setShowSuggestions(false);
    router.push(`/productos/${product.id}`);
    if (onClose) onClose();
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/productos?q=${encodeURIComponent(query)}`);
      setShowSuggestions(false);
      if (onClose) onClose();
    }
  };

  const formatPrice = (precio: number | null) => {
    if (!precio) return 'N/A';
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(precio);
  };

  return (
    <div ref={searchRef} className="relative w-full max-w-2xl">
      <form onSubmit={handleSearch} className="relative">
        <div className="relative">
          <FiSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => query.length >= 2 && setShowSuggestions(true)}
            placeholder="Buscar productos, SKU, nombre..."
            className="w-full pl-12 pr-12 py-3 border border-gray-300 rounded-full focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white"
          />
          {query && (
            <button
              type="button"
              onClick={() => {
                setQuery('');
                setShowSuggestions(false);
                inputRef.current?.focus();
              }}
              className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              <FiX className="w-5 h-5" />
            </button>
          )}
        </div>
      </form>

      <AnimatePresence>
        {showSuggestions && (suggestions.length > 0 || isLoading) && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="absolute z-50 w-full mt-2 bg-white rounded-2xl shadow-xl border border-gray-200 max-h-96 overflow-y-auto"
          >
            {isLoading ? (
              <div className="p-4 text-center text-gray-500">
                <div className="inline-block w-6 h-6 border-2 border-gray-300 border-t-blue-500 rounded-full animate-spin" />
              </div>
            ) : suggestions.length > 0 ? (
              <>
                <div className="divide-y divide-gray-100">
                  {suggestions.map((product) => {
                    const imagen = product.imagenes?.[0] || '/placeholder-product.jpg';
                    return (
                      <button
                        key={product.id}
                        onClick={() => handleSelectProduct(product)}
                        className="w-full p-4 hover:bg-gray-50 transition-colors text-left flex items-center gap-4"
                      >
                        <div className="relative w-16 h-16 flex-shrink-0 rounded-lg overflow-hidden bg-gray-100">
                          <Image
                            src={imagen}
                            alt={product.nombre}
                            fill
                            className="object-cover"
                            sizes="64px"
                          />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h4 className="font-semibold text-gray-900 truncate">{product.nombre}</h4>
                          {product.sku && (
                            <p className="text-xs text-gray-500 mt-1">SKU: {product.sku}</p>
                          )}
                        </div>
                        <div className="flex-shrink-0 text-right">
                          <p className="font-bold text-gray-900">
                            {formatPrice(product.precios.final.ars)}
                          </p>
                          {product.precios.final.usd && (
                            <p className="text-xs text-gray-500">
                              US$ {product.precios.final.usd.toLocaleString('es-AR')}
                            </p>
                          )}
                        </div>
                      </button>
                    );
                  })}
                </div>
                {query && (
                  <div className="p-3 border-t border-gray-100">
                    <button
                      onClick={handleSearch}
                      className="w-full text-center text-blue-600 hover:text-blue-700 font-semibold text-sm py-2"
                    >
                      Ver más resultados para "{query}"
                    </button>
                  </div>
                )}
              </>
            ) : null}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

