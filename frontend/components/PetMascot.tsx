'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface PetMascotProps {
  state: 'idle' | 'typing-email' | 'typing-password' | 'error' | 'success';
  className?: string;
}

export default function PetMascot({ state, className = '' }: PetMascotProps) {
  const [isBlinking, setIsBlinking] = useState(false);
  const [eyeExpression, setEyeExpression] = useState<'normal' | 'wide' | 'closed' | 'squint'>('normal');

  // Animación de parpadeo natural
  useEffect(() => {
    const blinkInterval = setInterval(() => {
      setIsBlinking(true);
      setTimeout(() => setIsBlinking(false), 150);
    }, 3000 + Math.random() * 2000); // Parpadea cada 3-5 segundos

    return () => clearInterval(blinkInterval);
  }, []);

  // Cambiar expresión según el estado
  useEffect(() => {
    switch (state) {
      case 'typing-email':
        setEyeExpression('wide');
        break;
      case 'typing-password':
        setEyeExpression('squint');
        break;
      case 'error':
        setEyeExpression('squint');
        break;
      case 'success':
        setEyeExpression('wide');
        break;
      default:
        setEyeExpression('normal');
    }
  }, [state]);

  // Animaciones del cuerpo según el estado
  const bodyAnimations = {
    idle: {
      y: [0, -5, 0],
    },
    'typing-email': {
      y: [0, -3, 0],
      rotate: [0, 2, -2, 0],
    },
    'typing-password': {
      scale: [1, 0.95, 1],
      y: [0, 2, 0],
    },
    error: {
      y: [0, 5, 0],
      rotate: [0, -3, 3, 0],
    },
    success: {
      scale: [1, 1.1, 1],
      rotate: [0, 5, -5, 5, 0],
      y: [0, -8, 0],
    },
  };

  const eyesClosed = isBlinking || eyeExpression === 'closed';

  return (
    <div className={`relative ${className}`}>
      <motion.div
        animate={bodyAnimations[state]}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          repeatType: 'reverse',
          ease: 'easeInOut',
        }}
        className="relative w-40 h-40 mx-auto"
      >
        {/* Robot Body */}
        <div className="relative w-full h-full">
          {/* Cuerpo principal del robot */}
          <motion.div
            className="absolute inset-0 rounded-2xl"
            style={{
              background: 'linear-gradient(135deg, #4a5568 0%, #2d3748 50%, #1a202c 100%)',
              boxShadow: `
                0 15px 35px rgba(0, 0, 0, 0.3),
                inset 0 -8px 20px rgba(0, 0, 0, 0.4),
                inset 0 4px 8px rgba(255, 255, 255, 0.1)
              `,
            }}
          >
            {/* Panel frontal con textura metálica */}
            <div 
              className="absolute inset-2 rounded-xl"
              style={{
                background: 'linear-gradient(135deg, #718096 0%, #4a5568 50%, #2d3748 100%)',
                boxShadow: 'inset 0 2px 4px rgba(255, 255, 255, 0.2), inset 0 -2px 4px rgba(0, 0, 0, 0.3)',
              }}
            >
              {/* Líneas decorativas tipo panel */}
              <div className="absolute top-4 left-4 right-4 h-0.5 bg-gray-600/30" />
              <div className="absolute bottom-4 left-4 right-4 h-0.5 bg-gray-600/30" />
              <div className="absolute left-4 top-4 bottom-4 w-0.5 bg-gray-600/30" />
              <div className="absolute right-4 top-4 bottom-4 w-0.5 bg-gray-600/30" />
            </div>

            {/* Ojos del robot */}
            <div className="absolute top-8 left-1/2 transform -translate-x-1/2 flex gap-6">
              {/* Ojo izquierdo */}
              <motion.div
                className="relative"
                animate={
                  eyeExpression === 'wide'
                    ? { scale: [1, 1.15, 1] }
                    : eyeExpression === 'squint'
                    ? { scale: [1, 0.7, 1] }
                    : {}
                }
                transition={{ duration: 0.3 }}
              >
                {/* Carcasa del ojo */}
                <div 
                  className="w-12 h-12 rounded-full relative overflow-hidden"
                  style={{
                    background: 'linear-gradient(135deg, #1a202c 0%, #2d3748 100%)',
                    boxShadow: `
                      inset 0 2px 8px rgba(0, 0, 0, 0.5),
                      0 2px 4px rgba(0, 0, 0, 0.3),
                      0 0 0 2px rgba(0, 0, 0, 0.2)
                    `,
                  }}
                >
                  {/* Párpado superior */}
                  <AnimatePresence>
                    {eyesClosed && (
                      <motion.div
                        initial={{ y: -24 }}
                        animate={{ y: 0 }}
                        exit={{ y: -24 }}
                        transition={{ duration: 0.15 }}
                        className="absolute top-0 left-0 right-0 h-6 rounded-t-full z-20"
                        style={{
                          background: 'linear-gradient(135deg, #1a202c 0%, #2d3748 100%)',
                          boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.3)',
                        }}
                      />
                    )}
                  </AnimatePresence>

                  {/* Iris y pupila */}
                  {!eyesClosed && (
                    <motion.div
                      className="absolute inset-2 rounded-full flex items-center justify-center"
                      animate={
                        state === 'typing-email'
                          ? { x: [0, 3, 0], y: [0, -2, 0] }
                          : state === 'typing-password'
                          ? { scale: [1, 0.8, 1] }
                          : state === 'error'
                          ? { x: [0, -2, 0], y: [0, 2, 0] }
                          : state === 'success'
                          ? { scale: [1, 1.2, 1] }
                          : {}
                      }
                      transition={{ duration: 0.4, repeat: Infinity }}
                    >
                      {/* Iris */}
                      <div 
                        className="w-8 h-8 rounded-full relative"
                        style={{
                          background: state === 'success' 
                            ? 'radial-gradient(circle, #10b981 0%, #059669 100%)'
                            : state === 'error'
                            ? 'radial-gradient(circle, #ef4444 0%, #dc2626 100%)'
                            : 'radial-gradient(circle, #3b82f6 0%, #2563eb 100%)',
                          boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.3), 0 1px 2px rgba(0, 0, 0, 0.2)',
                        }}
                      >
                        {/* Pupila */}
                        <div 
                          className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-4 h-4 rounded-full bg-gray-900"
                          style={{
                            boxShadow: 'inset 0 1px 2px rgba(0, 0, 0, 0.5)',
                          }}
                        />
                        {/* Brillo en el ojo */}
                        <div 
                          className="absolute top-1 left-2 w-2 h-2 rounded-full bg-white/80"
                          style={{
                            filter: 'blur(1px)',
                          }}
                        />
                      </div>
                    </motion.div>
                  )}

                  {/* Párpado inferior */}
                  <AnimatePresence>
                    {eyesClosed && (
                      <motion.div
                        initial={{ y: 24 }}
                        animate={{ y: 0 }}
                        exit={{ y: 24 }}
                        transition={{ duration: 0.15 }}
                        className="absolute bottom-0 left-0 right-0 h-6 rounded-b-full z-20"
                        style={{
                          background: 'linear-gradient(135deg, #1a202c 0%, #2d3748 100%)',
                          boxShadow: 'inset 0 -2px 4px rgba(0, 0, 0, 0.3)',
                        }}
                      />
                    )}
                  </AnimatePresence>
                </div>
              </motion.div>

              {/* Ojo derecho */}
              <motion.div
                className="relative"
                animate={
                  eyeExpression === 'wide'
                    ? { scale: [1, 1.15, 1] }
                    : eyeExpression === 'squint'
                    ? { scale: [1, 0.7, 1] }
                    : {}
                }
                transition={{ duration: 0.3, delay: 0.05 }}
              >
                {/* Carcasa del ojo */}
                <div 
                  className="w-12 h-12 rounded-full relative overflow-hidden"
                  style={{
                    background: 'linear-gradient(135deg, #1a202c 0%, #2d3748 100%)',
                    boxShadow: `
                      inset 0 2px 8px rgba(0, 0, 0, 0.5),
                      0 2px 4px rgba(0, 0, 0, 0.3),
                      0 0 0 2px rgba(0, 0, 0, 0.2)
                    `,
                  }}
                >
                  {/* Párpado superior */}
                  <AnimatePresence>
                    {eyesClosed && (
                      <motion.div
                        initial={{ y: -24 }}
                        animate={{ y: 0 }}
                        exit={{ y: -24 }}
                        transition={{ duration: 0.15 }}
                        className="absolute top-0 left-0 right-0 h-6 rounded-t-full z-20"
                        style={{
                          background: 'linear-gradient(135deg, #1a202c 0%, #2d3748 100%)',
                          boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.3)',
                        }}
                      />
                    )}
                  </AnimatePresence>

                  {/* Iris y pupila */}
                  {!eyesClosed && (
                    <motion.div
                      className="absolute inset-2 rounded-full flex items-center justify-center"
                      animate={
                        state === 'typing-email'
                          ? { x: [0, 3, 0], y: [0, -2, 0] }
                          : state === 'typing-password'
                          ? { scale: [1, 0.8, 1] }
                          : state === 'error'
                          ? { x: [0, 2, 0], y: [0, 2, 0] }
                          : state === 'success'
                          ? { scale: [1, 1.2, 1] }
                          : {}
                      }
                      transition={{ duration: 0.4, repeat: Infinity, delay: 0.1 }}
                    >
                      {/* Iris */}
                      <div 
                        className="w-8 h-8 rounded-full relative"
                        style={{
                          background: state === 'success' 
                            ? 'radial-gradient(circle, #10b981 0%, #059669 100%)'
                            : state === 'error'
                            ? 'radial-gradient(circle, #ef4444 0%, #dc2626 100%)'
                            : 'radial-gradient(circle, #3b82f6 0%, #2563eb 100%)',
                          boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.3), 0 1px 2px rgba(0, 0, 0, 0.2)',
                        }}
                      >
                        {/* Pupila */}
                        <div 
                          className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-4 h-4 rounded-full bg-gray-900"
                          style={{
                            boxShadow: 'inset 0 1px 2px rgba(0, 0, 0, 0.5)',
                          }}
                        />
                        {/* Brillo en el ojo */}
                        <div 
                          className="absolute top-1 left-2 w-2 h-2 rounded-full bg-white/80"
                          style={{
                            filter: 'blur(1px)',
                          }}
                        />
                      </div>
                    </motion.div>
                  )}

                  {/* Párpado inferior */}
                  <AnimatePresence>
                    {eyesClosed && (
                      <motion.div
                        initial={{ y: 24 }}
                        animate={{ y: 0 }}
                        exit={{ y: 24 }}
                        transition={{ duration: 0.15 }}
                        className="absolute bottom-0 left-0 right-0 h-6 rounded-b-full z-20"
                        style={{
                          background: 'linear-gradient(135deg, #1a202c 0%, #2d3748 100%)',
                          boxShadow: 'inset 0 -2px 4px rgba(0, 0, 0, 0.3)',
                        }}
                      />
                    )}
                  </AnimatePresence>
                </div>
              </motion.div>
            </div>

            {/* Boca/Expresión */}
            <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2">
              <AnimatePresence mode="wait">
                {state === 'error' && (
                  <motion.div
                    key="sad"
                    initial={{ scale: 0, rotate: 180 }}
                    animate={{ scale: 1, rotate: 0 }}
                    exit={{ scale: 0 }}
                    className="w-12 h-6 border-2 border-red-500 rounded-full"
                    style={{ borderTop: 'none' }}
                  />
                )}
                {state === 'success' && (
                  <motion.div
                    key="happy"
                    initial={{ scale: 0, rotate: -180 }}
                    animate={{ scale: 1, rotate: 0 }}
                    exit={{ scale: 0 }}
                    className="w-12 h-8 border-3 border-green-500 rounded-full"
                    style={{ borderBottom: 'none' }}
                  />
                )}
                {(state === 'idle' || state === 'typing-email' || state === 'typing-password') && (
                  <motion.div
                    key="neutral"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="w-10 h-1 bg-gray-400 rounded-full"
                  />
                )}
              </AnimatePresence>
            </div>

            {/* Antenas decorativas */}
            <div className="absolute -top-2 left-1/2 transform -translate-x-1/2 flex gap-8">
              <div className="w-1 h-3 bg-gray-600 rounded-full" />
              <div className="w-1 h-3 bg-gray-600 rounded-full" />
            </div>
          </motion.div>

          {/* Partículas de celebración cuando es éxito */}
          <AnimatePresence>
            {state === 'success' && (
              <>
                {[...Array(8)].map((_, i) => (
                  <motion.div
                    key={i}
                    initial={{ scale: 0, x: 0, y: 0, opacity: 1 }}
                    animate={{
                      scale: [0, 1.2, 0],
                      x: Math.cos((i * Math.PI * 2) / 8) * 50,
                      y: Math.sin((i * Math.PI * 2) / 8) * 50,
                      opacity: [1, 1, 0],
                    }}
                    exit={{ scale: 0, opacity: 0 }}
                    transition={{
                      duration: 1.2,
                      delay: i * 0.1,
                      repeat: 1,
                      ease: 'easeOut',
                    }}
                    className="absolute top-1/2 left-1/2 w-3 h-3 rounded-full"
                    style={{
                      background: ['#fbbf24', '#f59e0b', '#ef4444', '#10b981', '#3b82f6', '#8b5cf6', '#ec4899', '#14b8a6'][i],
                      boxShadow: `0 0 12px ${['#fbbf24', '#f59e0b', '#ef4444', '#10b981', '#3b82f6', '#8b5cf6', '#ec4899', '#14b8a6'][i]}80`,
                    }}
                  />
                ))}
              </>
            )}
          </AnimatePresence>
        </div>
      </motion.div>

      {/* Mensaje de estado */}
      <AnimatePresence>
        {state === 'error' && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="text-center mt-3"
          >
            <p className="text-sm font-semibold text-red-500">¡Ups! Algo salió mal</p>
            <p className="text-xs text-red-400 mt-1">Intenta nuevamente</p>
          </motion.div>
        )}
        {state === 'success' && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="text-center mt-3"
          >
            <p className="text-sm font-semibold text-green-500">¡Bienvenido!</p>
            <p className="text-xs text-green-400 mt-1">Redirigiendo...</p>
          </motion.div>
        )}
        {state === 'typing-email' && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="text-xs text-blue-500 text-center mt-2"
          >
            👀 Revisando tu email...
          </motion.p>
        )}
        {state === 'typing-password' && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="text-xs text-purple-500 text-center mt-2"
          >
            🔒 Verificando contraseña...
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  );
}
