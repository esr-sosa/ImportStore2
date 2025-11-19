'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { FiGrid, FiArrowRight } from 'react-icons/fi';
import { api, Categoria } from '@/lib/api';

export default function CategoriasPage() {
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadCategorias();
  }, []);

  const loadCategorias = async () => {
    try {
      const cats = await api.getCategorias();
      setCategorias(cats);
    } catch (error) {
      console.error('Error cargando categorías:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Categorías</h1>

        {isLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="bg-white rounded-2xl h-48 animate-pulse" />
            ))}
          </div>
        ) : categorias.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {categorias.map((categoria, index) => (
              <motion.div
                key={categoria.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Link
                  href={`/productos?categoria=${categoria.id}`}
                  className="block bg-white rounded-2xl p-8 hover:shadow-xl transition-all group"
                >
                  <FiGrid className="w-12 h-12 text-gray-400 group-hover:text-blue-600 transition-colors mb-4" />
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">{categoria.nombre}</h3>
                  {categoria.descripcion && (
                    <p className="text-gray-500 text-sm mb-4 line-clamp-2">
                      {categoria.descripcion}
                    </p>
                  )}
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-400">
                      {categoria.productos_count} productos
                    </span>
                    <FiArrowRight className="text-gray-400 group-hover:text-blue-600 transition-colors" />
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-2xl p-12 text-center">
            <p className="text-gray-500">No hay categorías disponibles</p>
          </div>
        )}
      </div>
    </div>
  );
}

