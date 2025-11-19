'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { FiTrash2, FiPlus, FiMinus, FiShoppingBag, FiArrowRight } from 'react-icons/fi';
import { useCartStore } from '@/stores/cartStore';
import PriceTag from '@/components/PriceTag';
import toast from 'react-hot-toast';

export default function CarritoPage() {
  const { items, total_items, total_ars, loadCarrito, eliminarItem, actualizarCantidad, isLoading } =
    useCartStore();

  useEffect(() => {
    loadCarrito();
  }, [loadCarrito]);

  const handleEliminar = async (index: number) => {
    try {
      await eliminarItem(index);
      toast.success('Producto eliminado del carrito');
    } catch (error: any) {
      toast.error(error.message || 'Error al eliminar');
    }
  };

  const handleActualizarCantidad = async (index: number, cantidad: number) => {
    if (cantidad < 1) {
      await handleEliminar(index);
      return;
    }
    try {
      await actualizarCantidad(index, cantidad);
    } catch (error: any) {
      toast.error(error.message || 'Error al actualizar cantidad');
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl p-12">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-8 animate-pulse" />
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="h-24 bg-gray-200 rounded animate-pulse" />
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl p-12 text-center">
            <FiShoppingBag className="w-24 h-24 mx-auto text-gray-300 mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Tu carrito está vacío</h2>
            <p className="text-gray-600 mb-8">Agregá productos para comenzar</p>
            <Link
              href="/productos"
              className="inline-flex items-center px-6 py-3 bg-black text-white rounded-full font-semibold hover:bg-gray-800 transition-colors"
            >
              Explorar Productos
              <FiArrowRight className="ml-2" />
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Carrito de Compras</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Items del Carrito */}
          <div className="lg:col-span-2 space-y-4">
            {items.map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3 }}
                className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 mb-1">{item.nombre}</h3>
                    {item.descripcion && (
                      <p className="text-sm text-gray-600 mb-2">{item.descripcion}</p>
                    )}
                    <p className="text-xs text-gray-500 mb-4">SKU: <span className="font-mono">{item.sku}</span></p>

                    <div className="flex items-center space-x-6 flex-wrap">
                      {/* Cantidad */}
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => handleActualizarCantidad(index, item.cantidad - 1)}
                          className="w-10 h-10 border-2 border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center justify-center text-gray-700 font-semibold"
                        >
                          <FiMinus className="w-4 h-4" />
                        </button>
                        <span className="w-12 text-center font-semibold text-gray-900">{item.cantidad}</span>
                        <button
                          onClick={() => handleActualizarCantidad(index, item.cantidad + 1)}
                          className="w-10 h-10 border-2 border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center justify-center text-gray-700 font-semibold"
                        >
                          <FiPlus className="w-4 h-4" />
                        </button>
                      </div>

                      {/* Precio */}
                      <div>
                        <PriceTag
                          precio={item.precio_unitario_ars * item.cantidad}
                          moneda="ARS"
                          size="md"
                        />
                        <p className="text-xs text-gray-500 mt-1">
                          ${item.precio_unitario_ars.toLocaleString('es-AR')} c/u
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Eliminar */}
                  <button
                    onClick={() => handleEliminar(index)}
                    className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors flex-shrink-0"
                    aria-label="Eliminar producto"
                  >
                    <FiTrash2 className="w-5 h-5" />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Resumen */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 sticky top-24">
              <h2 className="text-xl font-bold text-gray-900 mb-6">Resumen</h2>

              <div className="space-y-4 mb-6">
                <div className="flex justify-between text-gray-700">
                  <span>Subtotal ({total_items} {total_items === 1 ? 'item' : 'items'})</span>
                  <span className="font-semibold text-gray-900">
                    ${total_ars.toLocaleString('es-AR', { maximumFractionDigits: 0 })}
                  </span>
                </div>
                <div className="border-t border-gray-200 pt-4">
                  <div className="flex justify-between text-lg font-bold text-gray-900">
                    <span>Total</span>
                    <span>${total_ars.toLocaleString('es-AR', { maximumFractionDigits: 0 })}</span>
                  </div>
                </div>
              </div>

              <Link
                href="/checkout"
                className="block w-full px-6 py-4 bg-black text-white rounded-full font-semibold text-center hover:bg-gray-800 transition-colors"
              >
                Proceder al Checkout
                <FiArrowRight className="inline ml-2" />
              </Link>

              <Link
                href="/productos"
                className="block w-full mt-4 text-center text-gray-600 hover:text-gray-900 transition-colors"
              >
                Seguir comprando
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
