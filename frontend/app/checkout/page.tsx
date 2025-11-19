'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { FiCheckCircle, FiArrowLeft } from 'react-icons/fi';
import { useCartStore } from '@/stores/cartStore';
import { useAuthStore } from '@/stores/authStore';
import { api } from '@/lib/api';
import ProtectedRoute from '@/components/ProtectedRoute';
import toast from 'react-hot-toast';

export default function CheckoutPage() {
  return (
    <ProtectedRoute>
      <CheckoutContent />
    </ProtectedRoute>
  );
}

function CheckoutContent() {
  const router = useRouter();
  const { items, total_ars, loadCarrito, limpiarCarrito } = useCartStore();
  const { user } = useAuthStore();
  const [isProcessing, setIsProcessing] = useState(false);
  const [formData, setFormData] = useState({
    cliente_nombre: user?.first_name && user?.last_name 
      ? `${user.first_name} ${user.last_name}`.trim() 
      : user?.username || '',
    cliente_documento: '',
    metodo_pago: 'EFECTIVO_ARS',
    nota: '',
  });

  useEffect(() => {
    loadCarrito();
  }, [loadCarrito]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (items.length === 0) {
      toast.error('El carrito está vacío');
      return;
    }

    setIsProcessing(true);
    try {
      const resultado = await api.crearPedido(formData);
      await limpiarCarrito();
      toast.success('Pedido creado exitosamente');
      router.push(`/pedido-confirmado?venta_id=${resultado.venta_id}`);
    } catch (error: any) {
      toast.error(error.message || 'Error al crear el pedido');
    } finally {
      setIsProcessing(false);
    }
  };

  if (items.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl p-12 text-center">
            <p className="text-gray-500 text-lg mb-4">El carrito está vacío</p>
            <button
              onClick={() => router.push('/productos')}
              className="text-blue-600 hover:text-blue-700 font-semibold"
            >
              Volver a productos
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <button
          onClick={() => router.back()}
          className="flex items-center text-gray-600 hover:text-gray-900 mb-6"
        >
          <FiArrowLeft className="mr-2" />
          Volver
        </button>

        <h1 className="text-3xl font-bold text-gray-900 mb-8">Checkout</h1>

        <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Formulario */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white rounded-2xl p-6 shadow-sm">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Datos del Cliente</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Nombre Completo *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.cliente_nombre}
                    onChange={(e) =>
                      setFormData((prev) => ({ ...prev, cliente_nombre: e.target.value }))
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Documento (opcional)
                  </label>
                  <input
                    type="text"
                    value={formData.cliente_documento}
                    onChange={(e) =>
                      setFormData((prev) => ({ ...prev, cliente_documento: e.target.value }))
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Método de Pago *
                  </label>
                  <select
                    required
                    value={formData.metodo_pago}
                    onChange={(e) =>
                      setFormData((prev) => ({ ...prev, metodo_pago: e.target.value }))
                    }
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="EFECTIVO_ARS">Efectivo (ARS)</option>
                    <option value="EFECTIVO_USD">Efectivo (USD)</option>
                    <option value="TRANSFERENCIA">Transferencia</option>
                    <option value="TARJETA">Tarjeta</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Notas (opcional)
                  </label>
                  <textarea
                    value={formData.nota}
                    onChange={(e) => setFormData((prev) => ({ ...prev, nota: e.target.value }))}
                    rows={4}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Instrucciones especiales, dirección de entrega, etc."
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Resumen */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl p-6 shadow-sm sticky top-24">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Resumen del Pedido</h2>

              <div className="space-y-3 mb-6">
                {items.map((item, index) => (
                  <div key={index} className="flex justify-between text-sm">
                    <span className="text-gray-600">
                      {item.nombre} x{item.cantidad}
                    </span>
                    <span className="font-semibold">
                      ${(item.precio_unitario_ars * item.cantidad).toLocaleString('es-AR', {
                        maximumFractionDigits: 0,
                      })}
                    </span>
                  </div>
                ))}
              </div>

              <div className="border-t border-gray-200 pt-4 mb-6">
                <div className="flex justify-between text-lg font-bold text-gray-900">
                  <span>Total</span>
                  <span>${total_ars.toLocaleString('es-AR', { maximumFractionDigits: 0 })}</span>
                </div>
              </div>

              <motion.button
                type="submit"
                disabled={isProcessing}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="w-full px-6 py-4 bg-blue-600 text-white rounded-full font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isProcessing ? 'Procesando...' : 'Confirmar Pedido'}
              </motion.button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

