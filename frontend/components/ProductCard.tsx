'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { motion, AnimatePresence } from 'framer-motion';
import { FiHeart, FiShoppingCart } from 'react-icons/fi';
import { Producto, api } from '@/lib/api';
import PriceTag from './PriceTag';
import { useAuthStore } from '@/stores/authStore';
import { useCartStore } from '@/stores/cartStore';
import CartAnimation, { useCartPosition } from './CartAnimation';
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
  const { agregarItem, actualizarCantidad, eliminarItem, items } = useCartStore();
  const [isFavorito, setIsFavorito] = useState(false);
  const [isLoadingFav, setIsLoadingFav] = useState(false);
  const [isAddingToCart, setIsAddingToCart] = useState(false);
  const [isUpdatingQuantity, setIsUpdatingQuantity] = useState(false);
  const [showCartAnimation, setShowCartAnimation] = useState(false);
  const cardRef = useRef<HTMLDivElement>(null);
  const cartPosition = useCartPosition();
  
  // Verificar si el producto está en el carrito
  const cartItem = items.find(item => item.variante_id === product.id);
  const cantidadEnCarrito = cartItem?.cantidad || 0;

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
    
    // Validar stock antes de intentar agregar
    if (!product.stock.disponible || product.stock.actual <= 0) {
      toast.error('Producto sin stock disponible', { duration: 3000 });
      return;
    }

    setIsAddingToCart(true);
    
    // Activar animación 3D
    setShowCartAnimation(true);
    
    // Animar el carrito en el navbar
    const cartButton = document.querySelector('[data-cart-button]');
    if (cartButton) {
      cartButton.classList.add('animate-cart-bounce');
      setTimeout(() => {
        cartButton.classList.remove('animate-cart-bounce');
      }, 400);
    }
    
    try {
      await agregarItem(product.id, 1);
      toast.success('Producto agregado al carrito', {
        icon: '🛒',
        duration: 2000,
      });
    } catch (error: any) {
      // El error ya viene con el mensaje correcto del store
      toast.error(error.message || 'Error al agregar al carrito', { duration: 3000 });
      setShowCartAnimation(false);
    } finally {
      setIsAddingToCart(false);
    }
  };

  const handleIncrementar = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (!cartItem) return;
    
    // Verificar stock en tiempo real
    const stockDisponible = cartItem.stock_actual || product.stock.actual;
    if (cantidadEnCarrito >= stockDisponible) {
      toast.error(`Stock insuficiente. Disponible: ${stockDisponible}`, { duration: 3000 });
      return;
    }

    setIsUpdatingQuantity(true);
    try {
      const itemIndex = items.findIndex(item => item.variante_id === product.id);
      if (itemIndex !== -1) {
        await actualizarCantidad(itemIndex, cantidadEnCarrito + 1);
      }
    } catch (error: any) {
      toast.error(error.message || 'Error al actualizar cantidad', { duration: 3000 });
    } finally {
      setIsUpdatingQuantity(false);
    }
  };

  const handleDecrementar = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (!cartItem || cantidadEnCarrito <= 0) return;

    setIsUpdatingQuantity(true);
    try {
      const itemIndex = items.findIndex(item => item.variante_id === product.id);
      if (itemIndex !== -1) {
        if (cantidadEnCarrito === 1) {
          // Si es 1, eliminar del carrito
          await eliminarItem(itemIndex);
        } else {
          // Si es más de 1, decrementar
          await actualizarCantidad(itemIndex, cantidadEnCarrito - 1);
        }
      }
    } catch (error: any) {
      toast.error(error.message || 'Error al actualizar cantidad', { duration: 3000 });
    } finally {
      setIsUpdatingQuantity(false);
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
    <>
      <AnimatePresence>
        {showCartAnimation && (
          <CartAnimation
            productImage={imagenPrincipal}
            productName={product.nombre}
            cartPosition={cartPosition}
            onComplete={() => setShowCartAnimation(false)}
          />
        )}
      </AnimatePresence>
      
      <motion.div
        ref={cardRef}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: index * 0.05 }}
        className="group card-3d"
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
                <motion.button
                  onClick={handleToggleFavorito}
                  disabled={isLoadingFav}
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  className="p-2 bg-white/90 backdrop-blur-sm rounded-full hover:bg-white transition-all disabled:opacity-50 shadow-md hover:shadow-lg"
                  aria-label="Agregar a favoritos"
                >
                  <FiHeart
                    className={`w-4 h-4 transition-colors ${
                      isFavorito ? 'text-red-600 fill-current' : 'text-gray-700'
                    }`}
                  />
                </motion.button>
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

        {/* Botón agregar al carrito o controles de cantidad */}
        {product.stock.disponible && (
          <div className="p-4 pt-0 border-t border-gray-100">
            {cartItem && cantidadEnCarrito > 0 ? (
              // Controles de cantidad cuando el producto está en el carrito
              <div className="flex items-center justify-center gap-3">
                <motion.button
                  onClick={handleDecrementar}
                  disabled={isUpdatingQuantity || cantidadEnCarrito <= 0}
                  whileHover={{ scale: isUpdatingQuantity ? 1 : 1.1 }}
                  whileTap={{ scale: isUpdatingQuantity ? 1 : 0.9 }}
                  className="w-10 h-10 flex items-center justify-center bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg font-bold text-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  aria-label="Disminuir cantidad"
                >
                  {isUpdatingQuantity ? (
                    <div className="w-4 h-4 border-2 border-gray-600 border-t-transparent rounded-full animate-spin" />
                  ) : (
                    '−'
                  )}
                </motion.button>
                
                <span className="text-lg font-semibold text-gray-900 min-w-[2rem] text-center">
                  {cantidadEnCarrito}
                </span>
                
                <motion.button
                  onClick={handleIncrementar}
                  disabled={isUpdatingQuantity || cantidadEnCarrito >= (cartItem.stock_actual || product.stock.actual)}
                  whileHover={{ scale: isUpdatingQuantity ? 1 : 1.1 }}
                  whileTap={{ scale: isUpdatingQuantity ? 1 : 0.9 }}
                  className="w-10 h-10 flex items-center justify-center bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-bold text-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  aria-label="Aumentar cantidad"
                >
                  {isUpdatingQuantity ? (
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  ) : (
                    '+'
                  )}
                </motion.button>
              </div>
            ) : (
              // Botón agregar al carrito cuando no está en el carrito
              <motion.button
                onClick={handleAgregarAlCarrito}
                disabled={isAddingToCart}
                whileHover={{ scale: isAddingToCart ? 1 : 1.02 }}
                whileTap={{ scale: isAddingToCart ? 1 : 0.98 }}
                className="w-full px-4 py-2.5 bg-blue-600 text-white rounded-lg font-semibold flex items-center justify-center gap-2 hover:bg-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg"
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
            )}
          </div>
        )}
      </div>
      </motion.div>
    </>
  );
}
