'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { FiCheckCircle, FiArrowLeft, FiX, FiTag } from 'react-icons/fi';
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
  
  // Estados para cupones
  const [codigoCupon, setCodigoCupon] = useState('');
  const [cuponAplicado, setCuponAplicado] = useState<{
    codigo: string;
    descuento: number;
    monto_final: number;
  } | null>(null);
  const [isValidandoCupon, setIsValidandoCupon] = useState(false);
  
  // Inicializar formData con datos del usuario si existen
  const [formData, setFormData] = useState({
    cliente_nombre: user?.first_name && user?.last_name 
      ? `${user.first_name} ${user.last_name}`.trim() 
      : user?.username || '',
    cliente_documento: user?.documento || '',
    metodo_pago: 'EFECTIVO_ARS',
    nota: '',
  });

  useEffect(() => {
    loadCarrito();
    // Actualizar documento si el usuario se carga después
    if (user?.documento && !formData.cliente_documento) {
      setFormData(prev => ({ ...prev, cliente_documento: user.documento || '' }));
    }
  }, [loadCarrito, user]);

  const handleValidarCupon = async () => {
    if (!codigoCupon.trim()) {
      toast.error('Ingresa un código de cupón');
      return;
    }

    setIsValidandoCupon(true);
    try {
      const resultado = await api.validarCupon(codigoCupon.trim().toUpperCase(), total_ars);
      setCuponAplicado({
        codigo: resultado.cupon.codigo,
        descuento: resultado.descuento,
        monto_final: resultado.monto_final,
      });
      toast.success(`Cupón aplicado: ${resultado.descuento > 0 ? `-$${resultado.descuento.toLocaleString('es-AR')}` : 'Válido'}`);
    } catch (error: any) {
      toast.error(error.response?.data?.error || error.message || 'Cupón inválido');
      setCuponAplicado(null);
    } finally {
      setIsValidandoCupon(false);
    }
  };

  const handleRemoverCupon = () => {
    setCuponAplicado(null);
    setCodigoCupon('');
    toast.success('Cupón removido');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (items.length === 0) {
      toast.error('El carrito está vacío');
      return;
    }

    setIsProcessing(true);
    try {
      // Si el usuario tiene documento, usarlo automáticamente si no se proporciona
      const pedidoData = {
        ...formData,
        cliente_documento: formData.cliente_documento || user?.documento || '',
        codigo_cupon: cuponAplicado?.codigo || null,
      };
      
      const resultado = await api.crearPedido(pedidoData);
      await limpiarCarrito();
      toast.success('Pedido creado exitosamente');
      router.push(`/pedido-confirmado?venta_id=${resultado.venta_id}`);
    } catch (error: any) {
      console.error('Error al crear pedido:', error);
      toast.error(error.response?.data?.error || error.message || 'Error al crear el pedido');
    } finally {
      setIsProcessing(false);
    }
  };

  // Calcular descuentos por escalas
  const descuentoEscalas = items.reduce((sum, item) => {
    if (item.descuento_aplicado) {
      return sum + (item.descuento_aplicado * item.cantidad);
    }
    return sum;
  }, 0);
  
  // Calcular total con descuentos
  const subtotalConDescuentos = total_ars - descuentoEscalas;
  const totalConDescuento = cuponAplicado ? cuponAplicado.monto_final : subtotalConDescuentos;

  if (items.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl p-12 text-center">
            <p className="text-gray-500 text-lg mb-4">El carrito está vacío</p>
            <motion.button
              onClick={() => router.push('/productos')}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-6 py-3 bg-blue-600 text-white rounded-full font-semibold hover:bg-blue-700 transition-all shadow-md hover:shadow-lg"
            >
              Volver a productos
            </motion.button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.button
          onClick={() => router.back()}
          whileHover={{ x: -4 }}
          className="flex items-center text-gray-700 hover:text-gray-900 mb-6 font-medium transition-colors"
        >
          <FiArrowLeft className="mr-2" />
          Volver
        </motion.button>

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

                {/* Solo mostrar campo de documento si el usuario no tiene documento cargado */}
                {!user?.documento && (
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
                )}

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

                {/* Campo de Cupón */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Cupón de Descuento
                  </label>
                  {cuponAplicado ? (
                    <div className="flex items-center gap-2 p-3 bg-green-50 border border-green-200 rounded-lg">
                      <FiCheckCircle className="text-green-600" />
                      <span className="flex-1 text-sm text-green-800">
                        Cupón <strong>{cuponAplicado.codigo}</strong> aplicado
                        {cuponAplicado.descuento > 0 && (
                          <span className="ml-2">(-${cuponAplicado.descuento.toLocaleString('es-AR')})</span>
                        )}
                      </span>
                      <button
                        type="button"
                        onClick={handleRemoverCupon}
                        className="p-1 text-green-600 hover:text-green-800 transition-colors"
                      >
                        <FiX className="w-4 h-4" />
                      </button>
                    </div>
                  ) : (
                    <div className="flex gap-2">
                      <input
                        type="text"
                        value={codigoCupon}
                        onChange={(e) => setCodigoCupon(e.target.value.toUpperCase())}
                        onKeyPress={(e) => {
                          if (e.key === 'Enter') {
                            e.preventDefault();
                            handleValidarCupon();
                          }
                        }}
                        placeholder="Ingresa el código del cupón"
                        className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                      <button
                        type="button"
                        onClick={handleValidarCupon}
                        disabled={isValidandoCupon || !codigoCupon.trim()}
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                      >
                        {isValidandoCupon ? (
                          <>
                            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                            Validando...
                          </>
                        ) : (
                          <>
                            <FiTag className="w-4 h-4" />
                            Aplicar
                          </>
                        )}
                      </button>
                    </div>
                  )}
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
                  <div key={index} className="text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">
                        {item.nombre} x{item.cantidad}
                      </span>
                      <div className="text-right">
                        {item.descuento_aplicado && item.precio_base ? (
                          <div>
                            <span className="font-semibold text-gray-900">
                              ${(item.precio_unitario_ars * item.cantidad).toLocaleString('es-AR', {
                                maximumFractionDigits: 0,
                              })}
                            </span>
                            <div className="text-xs text-gray-500 line-through">
                              ${(item.precio_base * item.cantidad).toLocaleString('es-AR', {
                                maximumFractionDigits: 0,
                              })}
                            </div>
                            <div className="text-xs text-green-600 font-semibold mt-0.5">
                              -{item.porcentaje_descuento?.toFixed(1)}% desc.
                            </div>
                          </div>
                        ) : (
                          <span className="font-semibold">
                            ${(item.precio_unitario_ars * item.cantidad).toLocaleString('es-AR', {
                              maximumFractionDigits: 0,
                            })}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="border-t border-gray-200 pt-4 space-y-2 mb-6">
                <div className="flex justify-between text-sm text-gray-600">
                  <span>Subtotal</span>
                  <span>${total_ars.toLocaleString('es-AR', { maximumFractionDigits: 0 })}</span>
                </div>
                {descuentoEscalas > 0 && (
                  <div className="flex justify-between text-sm text-green-600">
                    <span>Descuento por cantidad</span>
                    <span>-${descuentoEscalas.toLocaleString('es-AR', { maximumFractionDigits: 0 })}</span>
                  </div>
                )}
                {cuponAplicado && cuponAplicado.descuento > 0 && (
                  <div className="flex justify-between text-sm text-green-600">
                    <span>Descuento ({cuponAplicado.codigo})</span>
                    <span>-${cuponAplicado.descuento.toLocaleString('es-AR', { maximumFractionDigits: 0 })}</span>
                  </div>
                )}
                <div className="flex justify-between text-lg font-bold text-gray-900 pt-2 border-t border-gray-200">
                  <span>Total</span>
                  <span>${totalConDescuento.toLocaleString('es-AR', { maximumFractionDigits: 0 })}</span>
                </div>
              </div>

              <motion.button
                type="submit"
                disabled={isProcessing}
                whileHover={{ scale: isProcessing ? 1 : 1.02 }}
                whileTap={{ scale: isProcessing ? 1 : 0.98 }}
                className="w-full px-6 py-4 bg-blue-600 text-white rounded-full font-semibold hover:bg-blue-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
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
