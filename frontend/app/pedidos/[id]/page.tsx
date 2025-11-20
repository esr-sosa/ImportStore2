'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { FiArrowLeft, FiDownload, FiCheckCircle, FiXCircle, FiClock, FiPackage, FiTruck, FiDollarSign } from 'react-icons/fi';
import { api } from '@/lib/api';
import { useAuthStore } from '@/stores/authStore';
import ProtectedRoute from '@/components/ProtectedRoute';
import toast from 'react-hot-toast';

interface PedidoDetalle {
  id: string;
  fecha: string;
  cliente_nombre: string;
  cliente_documento: string;
  total_ars: number;
  subtotal_ars: number;
  descuento_total_ars: number;
  impuestos_ars: number;
  status: string;
  status_display: string;
  metodo_pago: string;
  metodo_pago_display: string;
  origen: string;
  origen_display: string;
  motivo_cancelacion?: string;
  nota?: string;
  items: Array<{
    sku: string;
    descripcion: string;
    cantidad: number;
    precio_unitario_ars: number;
    subtotal_ars: number;
  }>;
  historial: Array<{
    estado_anterior?: string;
    estado_anterior_display?: string;
    estado_nuevo: string;
    estado_nuevo_display: string;
    usuario: string;
    nota?: string;
    fecha: string;
  }>;
}

export default function PedidoDetallePage() {
  return (
    <ProtectedRoute>
      <PedidoDetalleContent />
    </ProtectedRoute>
  );
}

function PedidoDetalleContent() {
  const params = useParams();
  const router = useRouter();
  const pedidoId = params.id as string;
  const { isAuthenticated } = useAuthStore();
  const [pedido, setPedido] = useState<PedidoDetalle | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (isAuthenticated) {
      loadPedido();
    }
  }, [pedidoId, isAuthenticated]);

  const loadPedido = async () => {
    setIsLoading(true);
    try {
      const data = await api.getPedido(pedidoId);
      setPedido(data);
    } catch (error: any) {
      toast.error(error.message || 'Error al cargar el pedido');
      router.push('/historial');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDescargarPDF = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/pedidos/${pedidoId}/pdf/`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `comprobante-${pedidoId}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        toast.success('Comprobante descargado');
      } else {
        toast.error('Error al descargar el comprobante');
      }
    } catch (error) {
      toast.error('Error al descargar el comprobante');
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'COMPLETADO':
        return <FiCheckCircle className="w-5 h-5 text-green-500" />;
      case 'CANCELADO':
      case 'DEVUELTO':
        return <FiXCircle className="w-5 h-5 text-red-500" />;
      case 'EN_CAMINO':
        return <FiTruck className="w-5 h-5 text-blue-500" />;
      case 'LISTO_RETIRAR':
        return <FiPackage className="w-5 h-5 text-yellow-500" />;
      default:
        return <FiClock className="w-5 h-5 text-yellow-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'COMPLETADO':
        return 'bg-green-100 text-green-700 border-green-200';
      case 'CANCELADO':
      case 'DEVUELTO':
        return 'bg-red-100 text-red-700 border-red-200';
      case 'PAGADO':
        return 'bg-blue-100 text-blue-700 border-blue-200';
      case 'EN_CAMINO':
        return 'bg-purple-100 text-purple-700 border-purple-200';
      case 'LISTO_RETIRAR':
        return 'bg-yellow-100 text-yellow-700 border-yellow-200';
      default:
        return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl p-12 animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-8" />
            <div className="space-y-4">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-24 bg-gray-200 rounded" />
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!pedido) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-2xl p-12 text-center">
            <p className="text-gray-500">Pedido no encontrado</p>
          </div>
        </div>
      </div>
    );
  }

  const isCancelado = pedido.status === 'CANCELADO' || pedido.status === 'DEVUELTO';

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => router.back()}
            className="flex items-center text-gray-600 hover:text-gray-900 mb-4 transition-colors"
          >
            <FiArrowLeft className="w-4 h-4 mr-2" />
            Volver
          </button>
          <h1 className="text-3xl font-bold text-gray-900">Pedido {pedido.id}</h1>
        </div>

        {/* Banner de cancelación/devuelto */}
        {isCancelado && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-red-50 border-2 border-red-200 rounded-2xl p-6 mb-6"
          >
            <div className="flex items-start space-x-3">
              <FiXCircle className="w-6 h-6 text-red-500 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-semibold text-red-900 mb-1">
                  Pedido {pedido.status === 'CANCELADO' ? 'Cancelado' : 'Devuelto'}
                </h3>
                {pedido.motivo_cancelacion && (
                  <p className="text-red-700 text-sm">{pedido.motivo_cancelacion}</p>
                )}
              </div>
            </div>
          </motion.div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Información Principal */}
          <div className="lg:col-span-2 space-y-6">
            {/* Estado Actual */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100"
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Estado Actual</h2>
                {getStatusIcon(pedido.status)}
              </div>
              <div className={`inline-flex items-center px-4 py-2 rounded-lg border-2 ${getStatusColor(pedido.status)}`}>
                <span className="font-semibold">{pedido.status_display}</span>
              </div>
              <p className="text-sm text-gray-500 mt-2">
                Origen: {pedido.origen_display || pedido.origen}
              </p>
            </motion.div>

            {/* Productos */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100"
            >
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Productos</h2>
              <div className="space-y-3">
                {pedido.items.map((item, index) => (
                  <div key={index} className="flex items-start justify-between py-3 border-b border-gray-100 last:border-0">
                    <div className="flex-1">
                      <p className="font-semibold text-gray-900">{item.descripcion}</p>
                      <p className="text-sm text-gray-500">SKU: {item.sku}</p>
                      <p className="text-sm text-gray-600 mt-1">
                        Cantidad: {item.cantidad} × ${item.precio_unitario_ars.toLocaleString('es-AR')}
                      </p>
                    </div>
                    <div className="text-right ml-4">
                      <p className="font-semibold text-gray-900">
                        ${item.subtotal_ars.toLocaleString('es-AR', { maximumFractionDigits: 0 })}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>

            {/* Historial de Estados */}
            {pedido.historial && pedido.historial.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100"
              >
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Historial de Cambios</h2>
                <div className="space-y-4">
                  {pedido.historial.map((cambio, index) => (
                    <div key={index} className="flex items-start space-x-3 pb-4 border-b border-gray-100 last:border-0 last:pb-0">
                      <div className="flex-shrink-0 w-2 h-2 bg-blue-500 rounded-full mt-2" />
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <span className="font-semibold text-gray-900">
                            {cambio.estado_anterior_display || 'Nuevo'} → {cambio.estado_nuevo_display}
                          </span>
                        </div>
                        <p className="text-sm text-gray-500">
                          {new Date(cambio.fecha).toLocaleString('es-AR', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </p>
                        {cambio.usuario && (
                          <p className="text-xs text-gray-400 mt-1">Por: {cambio.usuario}</p>
                        )}
                        {cambio.nota && (
                          <p className="text-sm text-gray-600 mt-2">{cambio.nota}</p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}
          </div>

          {/* Resumen */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 sticky top-24"
            >
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Resumen</h2>
              
              <div className="space-y-3 mb-6">
                <div className="flex justify-between text-sm text-gray-600">
                  <span>Subtotal</span>
                  <span className="font-semibold text-gray-900">
                    ${pedido.subtotal_ars.toLocaleString('es-AR', { maximumFractionDigits: 0 })}
                  </span>
                </div>
                {pedido.descuento_total_ars > 0 && (
                  <div className="flex justify-between text-sm text-gray-600">
                    <span>Descuento</span>
                    <span className="font-semibold text-red-600">
                      -${pedido.descuento_total_ars.toLocaleString('es-AR', { maximumFractionDigits: 0 })}
                    </span>
                  </div>
                )}
                {pedido.impuestos_ars > 0 && (
                  <div className="flex justify-between text-sm text-gray-600">
                    <span>Impuestos</span>
                    <span className="font-semibold text-gray-900">
                      ${pedido.impuestos_ars.toLocaleString('es-AR', { maximumFractionDigits: 0 })}
                    </span>
                  </div>
                )}
                <div className="border-t border-gray-200 pt-3">
                  <div className="flex justify-between text-lg font-bold text-gray-900">
                    <span>Total</span>
                    <span>${pedido.total_ars.toLocaleString('es-AR', { maximumFractionDigits: 0 })}</span>
                  </div>
                </div>
              </div>

              <div className="space-y-3 text-sm">
                <div>
                  <span className="text-gray-600">Fecha:</span>
                  <p className="text-gray-900 font-semibold">
                    {new Date(pedido.fecha).toLocaleDateString('es-AR', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </p>
                </div>
                <div>
                  <span className="text-gray-600">Método de pago:</span>
                  <p className="text-gray-900 font-semibold">{pedido.metodo_pago_display || pedido.metodo_pago}</p>
                </div>
                {pedido.cliente_documento && (
                  <div>
                    <span className="text-gray-600">DNI:</span>
                    <p className="text-gray-900 font-semibold">{pedido.cliente_documento}</p>
                  </div>
                )}
              </div>

              <button
                onClick={handleDescargarPDF}
                className="w-full mt-6 px-4 py-3 bg-black text-white rounded-full font-semibold flex items-center justify-center space-x-2 hover:bg-gray-800 transition-colors"
              >
                <FiDownload className="w-4 h-4" />
                <span>Descargar Comprobante PDF</span>
              </button>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}

