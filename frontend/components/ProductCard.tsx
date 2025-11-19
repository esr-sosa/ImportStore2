'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { motion, AnimatePresence } from 'framer-motion';
import { FiHeart, FiShoppingCart } from 'react-icons/fi';
import { Producto, api } from '@/lib/api';
import PriceTag from './PriceTag';
import { useAuthStore } from '@/stores/authStore';
import { useCartStore } from '@/stores/cartStore';
import toast from 'react-hot-toast';

interface ProductCardProps {
  product: Producto;
  index?: number;
}

export default function ProductCard({ product, index = 0 }: ProductCardProps) {
  const imagenes = product.imagenes?.filter(img => img) || [];
  const imagenPrincipal = imagenes[0] || '/placeholder-product.jpg';
  const imagenSecundaria = imagenes[1] || null;
  const [imagenActual, setImagenActual] = useState(imagenPrincipal);
  const [isHovering, setIsHovering] = useState(false);
  
  const { isAuthenticated } = useAuthStore();
  const { agregarItem, total_items } = useCartStore();
  const [isFavorito, setIsFavorito] = useState(false);
  const [isLoadingFav, setIsLoadingFav] = useState(false);
  const [isAddingToCart, setIsAddingToCart] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      checkFavorito();
    }
  }, [isAuthenticated, product.id]);

  // Efecto para cambiar imagen en hover
  useEffect(() => {
    if (isHovering && imagenSecundaria) {
      setImagenActual(imagenSecundaria);
    } else {
      setImagenActual(imagenPrincipal);
    }
  }, [isHovering, imagenPrincipal, imagenSecundaria]);

  const checkFavorito = async () => {
    try {
      const favoritos = await api.getFavoritos();
      setIsFavorito(favoritos.some((f) => f.variante_id === product.id));
    } catch {
      // Ignorar errores
    }
  };

  const handleToggleFavorito = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (!isAuthenticated) {
      toast.error('Debes iniciar sesión para agregar favoritos');
      return;
    }

    setIsLoadingFav(true);
    try {
      if (isFavorito) {
        await api.eliminarFavorito(product.id);
        setIsFavorito(false);
        toast.success('Eliminado de favoritos');
      } else {
        await api.agregarFavorito(product.id);
        setIsFavorito(true);
        toast.success('Agregado a favoritos');
      }
    } catch (error: any) {
      toast.error(error.message || 'Error al actualizar favoritos');
    } finally {
      setIsLoadingFav(false);
    }
  };

  const handleAgregarAlCarrito = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (!product.stock.disponible) {
      toast.error('Producto no disponible');
      return;
    }

    setIsAddingToCart(true);
    try {
      await agregarItem(product.id, 1);
      toast.success('Producto agregado al carrito', {
        icon: '🛒',
        duration: 2000,
      });
    } catch (error: any) {
      if (error.response?.status === 401) {
        toast.error('Debes iniciar sesión para agregar al carrito');
      } else {
        toast.error(error.message || 'Error al agregar al carrito');
      }
    } finally {
      setIsAddingToCart(false);
    }
  };

  // Descripción corta (50-80 caracteres)
  const descripcionCorta = product.descripcion
    ? product.descripcion.length > 80
      ? product.descripcion.substring(0, 80) + '...'
      : product.descripcion
    : '';

  // Determinar si mostrar ambos precios (USD y ARS) - para celulares
  const tieneAmbosPrecios = product.precios.final.usd && product.precios.final.ars;
  const esCelular = product.categoria.nombre?.toLowerCase().includes('celular') || 
                    product.categoria.nombre?.toLowerCase().includes('iphone') ||
                    product.nombre.toLowerCase().includes('iphone') ||
                    product.nombre.toLowerCase().includes('celular');

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
      className="group"
      onMouseEnter={() => setIsHovering(true)}
      onMouseLeave={() => setIsHovering(false)}
    >
      <div className="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 border border-gray-100 h-full flex flex-col">
        <Link href={`/productos/${product.id}`} className="flex-1 flex flex-col">
          {/* Imagen con hover swap */}
          <div className="relative aspect-square overflow-hidden bg-gray-100">
            <AnimatePresence mode="wait">
              <motion.div
                key={imagenActual}
                initial={{ opacity: 0, scale: 0.98 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.98 }}
                transition={{ duration: 0.2 }}
                className="absolute inset-0"
              >
                <Image
                  src={imagenActual}
                  alt={product.nombre}
                  fill
                  className="object-cover group-hover:scale-110 transition-transform duration-500"
                  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                />
              </motion.div>
            </AnimatePresence>

            {/* Botones de acción */}
            <div className="absolute top-2 left-2 flex flex-col gap-2 z-10">
              {/* Botón de favoritos */}
              {isAuthenticated && (
                <button
                  onClick={handleToggleFavorito}
                  disabled={isLoadingFav}
                  className="p-2 bg-white/90 backdrop-blur-sm rounded-full hover:bg-white transition-colors disabled:opacity-50 shadow-sm"
                  aria-label="Agregar a favoritos"
                >
                  <FiHeart
                    className={`w-4 h-4 transition-colors ${
                      isFavorito ? 'text-red-500 fill-current' : 'text-gray-700'
                    }`}
                  />
                </button>
              )}
            </div>
          </div>

          {/* Contenido */}
          <div className="p-4 flex-1 flex flex-col">
            <h3 className="font-semibold text-gray-900 mb-1 line-clamp-2 min-h-[3rem] hover:text-gray-600 transition-colors">
              {product.nombre}
            </h3>
            
            {product.atributos.display && (
              <p className="text-sm text-gray-600 mb-2">{product.atributos.display}</p>
            )}

            {/* Descripción corta */}
            {descripcionCorta && (
              <p className="text-xs text-gray-500 mb-2 line-clamp-2 flex-1">{descripcionCorta}</p>
            )}

            {product.categoria.nombre && (
              <p className="text-xs text-gray-400 mb-3">{product.categoria.nombre}</p>
            )}

            {/* Precio - Mostrar USD y ARS si es celular o tiene ambos */}
            <div className="mt-auto">
              {(esCelular || tieneAmbosPrecios) && product.precios.final.usd && product.precios.final.ars ? (
                <PriceTag
                  precio={product.precios.final.ars}
                  precioUSD={product.precios.final.usd}
                  precioOriginal={null}
                  moneda="USD"
                  size="md"
                  showBoth={true}
                />
              ) : (
                <PriceTag
                  precio={product.precios.final.ars}
                  precioUSD={product.precios.final.usd}
                  precioOriginal={null}
                  moneda="ARS"
                  size="md"
                />
              )}
            </div>
          </div>
        </Link>

        {/* Botón agregar al carrito - siempre visible */}
        {product.stock.disponible && (
          <div className="p-4 pt-0 border-t border-gray-100">
            <motion.button
              onClick={handleAgregarAlCarrito}
              disabled={isAddingToCart}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full px-4 py-2.5 bg-black text-white rounded-lg font-semibold flex items-center justify-center gap-2 hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isAddingToCart ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Agregando...</span>
                </>
              ) : (
                <>
                  <FiShoppingCart className="w-4 h-4" />
                  <span>Agregar al Carrito</span>
                </>
              )}
            </motion.button>
          </div>
        )}
      </div>
    </motion.div>
  );
}
