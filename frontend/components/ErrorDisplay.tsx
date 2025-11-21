'use client';

import { FiAlertCircle, FiRefreshCw } from 'react-icons/fi';
import { motion } from 'framer-motion';

interface ErrorDisplayProps {
  message?: string;
  onRetry?: () => void;
  className?: string;
}

export default function ErrorDisplay({ message, onRetry, className = '' }: ErrorDisplayProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-white rounded-2xl p-12 text-center ${className}`}
    >
      <FiAlertCircle className="w-16 h-16 mx-auto text-red-500 mb-4" />
      <h3 className="text-xl font-semibold text-gray-900 mb-2">Algo salió mal</h3>
      <p className="text-gray-500 mb-6">
        {message || 'Ocurrió un error al cargar los datos. Por favor, intenta nuevamente.'}
      </p>
      {onRetry && (
        <motion.button
          onClick={onRetry}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="inline-flex items-center px-6 py-3 bg-black text-white rounded-full font-semibold hover:bg-gray-800 transition-all shadow-lg hover:shadow-xl"
        >
          <FiRefreshCw className="mr-2" />
          Reintentar
        </motion.button>
      )}
    </motion.div>
  );
}

