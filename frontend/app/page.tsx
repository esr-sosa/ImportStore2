'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { FiArrowRight, FiShoppingBag, FiTag, FiGrid } from 'react-icons/fi';
import { api, Producto, Categoria } from '@/lib/api';
import ProductCard from '@/components/ProductCard';
import { useConfigStore } from '@/stores/configStore';
import { useAuthStore } from '@/stores/authStore';

export default function HomePage() {
  const [productosDestacados, setProductosDestacados] = useState<Producto[]>([]);
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { config } = useConfigStore();
  const colorPrimary = config?.color_principal || '#2563eb';

  useEffect(() => {
    const loadData = async () => {
      try {
        const { user } = useAuthStore.getState();
        const tipo_precio = user?.tipo_usuario || 'MINORISTA';
        
        const [productos, cats] = await Promise.all([
          api.getProductoDestacados(tipo_precio),
          api.getCategorias(),
        ]);
        setProductosDestacados(productos);
        setCategorias(cats.slice(0, 6));
      } catch (error) {
        console.error('Error cargando datos:', error);
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, []);

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-gray-50 to-white py-20 md:py-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center"
          >
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              {config?.nombre_comercial || 'Bienvenido a ImportStore'}
            </h1>
            {config?.lema && (
              <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">{config.lema}</p>
            )}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/productos"
                className="inline-flex items-center justify-center px-8 py-4 rounded-full text-white font-semibold transition-all hover:scale-105 shadow-lg"
                style={{ backgroundColor: colorPrimary }}
              >
                Ver Productos
                <FiArrowRight className="ml-2" />
              </Link>
              <Link
                href="/categorias"
                className="inline-flex items-center justify-center px-8 py-4 rounded-full border-2 border-gray-300 text-gray-700 font-semibold transition-all hover:border-gray-400"
              >
                Explorar Categorías
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Categorías */}
      {categorias.length > 0 && (
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-3xl font-bold text-gray-900">Categorías</h2>
              <Link
                href="/categorias"
                className="text-blue-600 hover:text-blue-700 font-semibold flex items-center"
              >
                Ver todas
                <FiArrowRight className="ml-1" />
              </Link>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
              {categorias.map((categoria, index) => (
                <motion.div
                  key={categoria.id}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Link
                    href={`/productos?categoria=${categoria.id}`}
                    className="block p-6 bg-gray-50 rounded-2xl hover:bg-gray-100 transition-all text-center group"
                  >
                    <FiGrid className="w-8 h-8 mx-auto mb-3 text-gray-400 group-hover:text-blue-600 transition-colors" />
                    <h3 className="font-semibold text-gray-900">{categoria.nombre}</h3>
                    <p className="text-sm text-gray-500 mt-1">
                      {categoria.productos_count} productos
                    </p>
                  </Link>
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Productos Destacados */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-3xl font-bold text-gray-900">Productos Destacados</h2>
            <Link
              href="/productos"
              className="text-blue-600 hover:text-blue-700 font-semibold flex items-center"
            >
              Ver todos
              <FiArrowRight className="ml-1" />
            </Link>
          </div>

          {isLoading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {[...Array(8)].map((_, i) => (
                <div key={i} className="bg-white rounded-2xl h-96 animate-pulse" />
              ))}
            </div>
          ) : productosDestacados.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {productosDestacados.map((producto, index) => (
                <ProductCard key={producto.id} product={producto} index={index} />
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <FiShoppingBag className="w-16 h-16 mx-auto text-gray-300 mb-4" />
              <p className="text-gray-500">No hay productos destacados disponibles</p>
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              ¿Buscas algo específico?
            </h2>
            <p className="text-gray-600 mb-8">
              Explora nuestro catálogo completo de productos premium
            </p>
            <Link
              href="/productos"
              className="inline-flex items-center justify-center px-8 py-4 rounded-full text-white font-semibold transition-all hover:scale-105 shadow-lg"
              style={{ backgroundColor: colorPrimary }}
            >
              Explorar Catálogo
              <FiArrowRight className="ml-2" />
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  );
}

