'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';
import { motion } from 'framer-motion';
import { FiShoppingCart } from 'react-icons/fi';
import { QRCodeSVG } from 'qrcode.react';
import { api, Producto } from '@/lib/api';
import PriceTag from '@/components/PriceTag';
import ProductCard from '@/components/ProductCard';
import { useCartStore } from '@/stores/cartStore';
import { useAuthStore } from '@/stores/authStore';
import toast from 'react-hot-toast';

export default function ProductoDetallePage() {
  const params = useParams();
  const productoId = parseInt(params.id as string);
  const { user } = useAuthStore();
  
  const [producto, setProducto] = useState<Producto | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [imagenSeleccionada, setImagenSeleccionada] = useState(0);
  const [cantidad, setCantidad] = useState(1);
  const [isAddingToCart, setIsAddingToCart] = useState(false);
  const { agregarItem } = useCartStore();

  useEffect(() => {
    loadProducto();
  }, [productoId]);

  const loadProducto = async () => {
    setIsLoading(true);
    try {
      // Usar tipo_usuario del usuario autenticado si está disponible
      const tipo_precio = user?.tipo_usuario || 'MINORISTA';
      const prod = await api.getProducto(productoId, tipo_precio);
      setProducto(prod);
    } catch (error: any) {
      toast.error(error.message || 'Error al cargar el producto');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAgregarAlCarrito = async () => {
    if (!producto) return;
    
    // Validar stock antes de intentar agregar
    if (!producto.stock.disponible || producto.stock.actual <= 0) {
      toast.error('Producto sin stock disponible', { duration: 3000 });
      return;
    }
    
    if (cantidad > producto.stock.actual) {
      toast.error(`Stock insuficiente. Disponible: ${producto.stock.actual}`, { duration: 3000 });
      return;
    }

    setIsAddingToCart(true);
    try {
      await agregarItem(producto.id, cantidad);
      toast.success('Producto agregado al carrito', {
        icon: '🛒',
        duration: 2000,
      });
      setCantidad(1); // Resetear cantidad
    } catch (error: any) {
      // El error ya viene con el mensaje correcto del store
      toast.error(error.message || 'Error al agregar al carrito', { duration: 3000 });
    } finally {
      setIsAddingToCart(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl p-12">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="space-y-4">
                <div className="h-96 bg-gray-200 rounded-2xl animate-pulse" />
                <div className="grid grid-cols-4 gap-2">
                  {[...Array(4)].map((_, i) => (
                    <div key={i} className="h-20 bg-gray-200 rounded-lg animate-pulse" />
                  ))}
                </div>
              </div>
              <div className="space-y-4">
                <div className="h-8 bg-gray-200 rounded w-3/4 animate-pulse" />
                <div className="h-4 bg-gray-200 rounded w-1/2 animate-pulse" />
                <div className="h-12 bg-gray-200 rounded w-1/3 animate-pulse" />
                <div className="h-32 bg-gray-200 rounded animate-pulse" />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!producto) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl p-12 text-center">
            <p className="text-gray-500 text-lg">Producto no encontrado</p>
          </div>
        </div>
      </div>
    );
  }

  const imagenes = producto.imagenes.filter((img) => img !== null) as string[];
  const imagenPrincipal = imagenes[imagenSeleccionada] || imagenes[0] || '/placeholder-product.jpg';
  const esCelular = producto.categoria.nombre?.toLowerCase().includes('celular') || 
                    producto.categoria.nombre?.toLowerCase().includes('iphone') ||
                    producto.nombre.toLowerCase().includes('iphone') ||
                    producto.nombre.toLowerCase().includes('celular');
  const tieneAmbosPrecios = producto.precios.final.usd && producto.precios.final.ars;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-2xl overflow-hidden shadow-lg">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 p-8">
            {/* Galería de Imágenes */}
            <div>
              <div className="relative aspect-square mb-4 bg-gray-100 rounded-2xl overflow-hidden">
                {imagenPrincipal && (
                  <Image
                    src={imagenPrincipal}
                    alt={producto.nombre}
                    fill
                    className="object-cover"
                    priority
                  />
                )}
              </div>
              
              {imagenes.length > 1 && (
                <div className="grid grid-cols-4 gap-2">
                  {imagenes.map((img, index) => (
                    <button
                      key={index}
                      onClick={() => setImagenSeleccionada(index)}
                      className={`relative aspect-square rounded-lg overflow-hidden border-2 transition-all ${
                        imagenSeleccionada === index
                          ? 'border-blue-500'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <Image
                        src={img}
                        alt={`${producto.nombre} ${index + 1}`}
                        fill
                        className="object-cover"
                      />
                    </button>
                  ))}
                </div>
              )}

              {/* QR Code */}
              {producto.qr_code && (
                <div className="mt-6 p-4 bg-gray-50 rounded-lg text-center">
                  <p className="text-sm text-gray-600 mb-2">Código QR</p>
                  <div className="flex justify-center">
                    <QRCodeSVG value={producto.qr_code} size={120} />
                  </div>
                </div>
              )}
            </div>

            {/* Información del Producto */}
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{producto.nombre}</h1>
              
              {producto.nombre_variante && (
                <p className="text-lg text-gray-600 mb-4">{producto.nombre_variante}</p>
              )}

              {producto.atributos.display && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {producto.atributos.atributo_1 && (
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                      {producto.atributos.atributo_1}
                    </span>
                  )}
                  {producto.atributos.atributo_2 && (
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                      {producto.atributos.atributo_2}
                    </span>
                  )}
                </div>
              )}

              {/* Precio */}
              <div className="mb-6">
                {(esCelular || tieneAmbosPrecios) && producto.precios.final.usd && producto.precios.final.ars ? (
                  <PriceTag
                    precio={producto.precios.final.ars}
                    precioUSD={producto.precios.final.usd}
                    moneda="USD"
                    size="lg"
                    showBoth={true}
                  />
                ) : (
                  <PriceTag
                    precio={producto.precios.final.ars}
                    precioUSD={producto.precios.final.usd}
                    moneda="ARS"
                    size="lg"
                  />
                )}
              </div>

              {/* Descripción */}
              {producto.descripcion && (
                <div className="mb-6">
                  <h3 className="font-semibold text-gray-900 mb-2 text-lg">Descripción</h3>
                  <p className="text-gray-700 whitespace-pre-line leading-relaxed">{producto.descripcion}</p>
                </div>
              )}

              {/* SKU y Categoría */}
              <div className="mb-6 text-sm text-gray-600 space-y-1">
                <p>SKU: <span className="font-mono text-gray-900">{producto.sku}</span></p>
                {producto.categoria.nombre && (
                  <p>Categoría: <span className="text-gray-900">{producto.categoria.nombre}</span></p>
                )}
              </div>

              {/* Cantidad y Agregar al Carrito */}
              {producto.stock.disponible && (
                <div className="space-y-4">
                  <div className="flex items-center space-x-4">
                    <label className="font-semibold text-gray-900">Cantidad:</label>
                    <div className="flex items-center space-x-2">
                      <motion.button
                        onClick={() => setCantidad(Math.max(1, cantidad - 1))}
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        className="w-10 h-10 border-2 border-gray-300 rounded-lg hover:bg-gray-100 hover:border-gray-400 transition-all text-gray-900 font-semibold shadow-sm hover:shadow-md"
                      >
                        -
                      </motion.button>
                      <input
                        type="number"
                        value={cantidad}
                        onChange={(e) => {
                          const val = parseInt(e.target.value) || 1;
                          setCantidad(Math.max(1, val));
                        }}
                        className="w-20 text-center border-2 border-gray-300 rounded-lg py-2 text-gray-900 font-semibold focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        min="1"
                      />
                      <motion.button
                        onClick={() => setCantidad(cantidad + 1)}
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        className="w-10 h-10 border-2 border-gray-300 rounded-lg hover:bg-gray-100 hover:border-gray-400 transition-all text-gray-900 font-semibold shadow-sm hover:shadow-md"
                      >
                        +
                      </motion.button>
                    </div>
                  </div>

                  <motion.button
                    whileHover={{ scale: isAddingToCart ? 1 : 1.02 }}
                    whileTap={{ scale: isAddingToCart ? 1 : 0.98 }}
                    onClick={handleAgregarAlCarrito}
                    disabled={isAddingToCart}
                    className="w-full px-6 py-4 bg-black text-white rounded-full font-semibold flex items-center justify-center space-x-2 hover:bg-gray-800 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
                  >
                    {isAddingToCart ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                        <span>Agregando...</span>
                      </>
                    ) : (
                      <>
                        <FiShoppingCart className="w-5 h-5" />
                        <span>Agregar al Carrito</span>
                      </>
                    )}
                  </motion.button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Productos Relacionados */}
        {producto.relacionados && producto.relacionados.length > 0 && (
          <div className="mt-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Productos Relacionados</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              {producto.relacionados.map((rel, index) => (
                <ProductCard key={rel.id} product={rel} index={index} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
