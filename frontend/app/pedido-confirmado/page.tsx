'use client';

import { useSearchParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { FiCheckCircle, FiShoppingBag, FiHome } from 'react-icons/fi';

export default function PedidoConfirmadoPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const venta_id = searchParams.get('venta_id');

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white rounded-2xl p-12 text-center shadow-lg"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: 'spring' }}
            className="mb-6"
          >
            <FiCheckCircle className="w-24 h-24 mx-auto text-green-500" />
          </motion.div>

          <h1 className="text-3xl font-bold text-gray-900 mb-4">¡Pedido Confirmado!</h1>
          <p className="text-gray-600 mb-2">
            Tu pedido ha sido registrado exitosamente.
          </p>
          {venta_id && (
            <p className="text-sm text-gray-500 mb-8">
              Número de pedido: <span className="font-semibold">{venta_id}</span>
            </p>
          )}

          <div className="space-y-4">
            <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <Link
                href="/productos"
                className="inline-flex items-center justify-center w-full px-6 py-3 bg-blue-600 text-white rounded-full font-semibold hover:bg-blue-700 transition-all shadow-lg hover:shadow-xl"
              >
                <FiShoppingBag className="mr-2" />
                Seguir Comprando
              </Link>
            </motion.div>
            <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <Link
                href="/"
                className="inline-flex items-center justify-center w-full px-6 py-3 border-2 border-gray-300 text-gray-900 rounded-full font-semibold hover:bg-gray-100 hover:border-gray-400 transition-all shadow-sm hover:shadow-md"
              >
                <FiHome className="mr-2" />
                Volver al Inicio
              </Link>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}

