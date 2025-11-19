'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { FiHeart, FiShoppingBag, FiArrowRight } from 'react-icons/fi';
import { api, Favorito } from '@/lib/api';
import ProductCard from '@/components/ProductCard';
import { useAuthStore } from '@/stores/authStore';
import ProtectedRoute from '@/components/ProtectedRoute';
import toast from 'react-hot-toast';

export default function FavoritosPage() {
  return (
    <ProtectedRoute>
      <FavoritosContent />
    </ProtectedRoute>
  );
}

function FavoritosContent() {
  const router = useRouter();
  const [favoritos, setFavoritos] = useState<Favorito[]>([]);
  const [productos, setProductos] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadFavoritos();
  }, []);

  const loadFavoritos = async () => {
    setIsLoading(true);
    try {
      const favs = await api.getFavoritos();
      setFavoritos(favs);
      
      // Cargar detalles de productos
      const productosData = await Promise.all(
        favs.map(async (fav) => {
          try {
            return await api.getProducto(fav.variante_id);
          } catch {
            return null;
          }
        })
      );
      setProductos(productosData.filter((p) => p !== null));
    } catch (error: any) {
      toast.error(error.message || 'Error al cargar favoritos');
    } finally {
      setIsLoading(false);
    }
  };

  const handleEliminarFavorito = async (variante_id: number) => {
    try {
      await api.eliminarFavorito(variante_id);
      toast.success('Eliminado de favoritos');
      loadFavoritos();
    } catch (error: any) {
      toast.error(error.message || 'Error al eliminar');
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl p-12 animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-8" />
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-96 bg-gray-200 rounded-2xl" />
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
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <FiHeart className="mr-3 text-red-500" />
            Mis Favoritos
          </h1>
        </div>

        {productos.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {productos.map((producto, index) => (
              <div key={producto.id} className="relative">
                <ProductCard product={producto} index={index} />
                <button
                  onClick={() => handleEliminarFavorito(producto.id)}
                  className="absolute top-4 right-4 p-2 bg-white rounded-full shadow-lg hover:bg-red-50 transition-colors"
                >
                  <FiHeart className="w-5 h-5 text-red-500 fill-current" />
                </button>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-2xl p-12 text-center">
            <FiHeart className="w-24 h-24 mx-auto text-gray-300 mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">No tenés favoritos aún</h2>
            <p className="text-gray-500 mb-8">Agregá productos a tus favoritos para encontrarlos fácilmente</p>
            <Link
              href="/productos"
              className="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-full font-semibold hover:bg-blue-700 transition-colors"
            >
              <FiShoppingBag className="mr-2" />
              Explorar Productos
              <FiArrowRight className="ml-2" />
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}

