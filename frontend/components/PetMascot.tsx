'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface PetMascotProps {
  state: 'idle' | 'typing-email' | 'typing-password' | 'error' | 'success';
  className?: string;
}

export default function PetMascot({ state, className = '' }: PetMascotProps) {
  const [mood, setMood] = useState<'happy' | 'curious' | 'shy' | 'sad' | 'excited'>('happy');
  const [eyeDirection, setEyeDirection] = useState({ x: 0, y: 0 });

  useEffect(() => {
    switch (state) {
      case 'typing-email':
        setMood('curious');
        break;
      case 'typing-password':
        setMood('shy');
        break;
      case 'error':
        setMood('sad');
        break;
      case 'success':
        setMood('excited');
        break;
      default:
        setMood('happy');
    }
  }, [state]);

  // Animaciones del cuerpo según el estado
  const bodyAnimations = {
    happy: {
      y: [0, -8, 0],
      rotate: [0, 2, -2, 0],
    },
    curious: {
      y: [0, -5, 0],
      x: [0, 3, -3, 0],
      rotate: [0, 5, -5, 0],
    },
    shy: {
      scale: [1, 0.92, 1],
      y: [0, 3, 0],
    },
    sad: {
      y: [0, 8, 0],
      rotate: [0, -8, 0],
    },
    excited: {
      scale: [1, 1.15, 1],
      rotate: [0, 15, -15, 15, 0],
      y: [0, -12, 0],
    },
  };

  return (
    <div className={`relative ${className}`}>
      <motion.div
        animate={bodyAnimations[mood]}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          repeatType: 'reverse',
          ease: 'easeInOut',
        }}
        className="relative w-32 h-32 mx-auto"
      >
        {/* Yeti Mascot */}
        <div className="relative w-full h-full">
          {/* Cuerpo principal del Yeti */}
          <motion.div
            className="absolute inset-0 rounded-full"
            style={{
              background: 'linear-gradient(135deg, #a8d8ea 0%, #7bb3d3 50%, #5a9fc7 100%)',
              boxShadow: '0 10px 30px rgba(90, 159, 199, 0.4), inset 0 -5px 15px rgba(0,0,0,0.1)',
            }}
          >
            {/* Pelaje/textura superior */}
            <div 
              className="absolute top-0 left-0 right-0 h-1/3 rounded-t-full"
              style={{
                background: 'linear-gradient(180deg, rgba(255,255,255,0.3) 0%, transparent 100%)',
              }}
            />
            
            {/* Ojos grandes y expresivos */}
            <div className="absolute top-6 left-1/2 transform -translate-x-1/2 flex gap-4">
              {/* Ojo izquierdo */}
              <motion.div
                className="relative"
                animate={
                  state === 'typing-email'
                    ? { scale: [1, 1.15, 1] }
                    : state === 'typing-password'
                    ? { scale: [1, 0.7, 1], opacity: [1, 0.4, 1] }
                    : state === 'error'
                    ? { y: [0, 3, 0], rotate: [0, -5, 0] }
                    : state === 'success'
                    ? { scale: [1, 1.2, 1] }
                    : {}
                }
                transition={{ duration: 0.6, repeat: Infinity }}
              >
                <div className="w-8 h-8 bg-white rounded-full shadow-inner flex items-center justify-center overflow-hidden">
                  <motion.div
                    className="w-5 h-5 bg-blue-900 rounded-full"
                    animate={
                      state === 'typing-email'
                        ? { x: [0, 3, 0], y: [0, -2, 0] }
                        : state === 'typing-password'
                        ? { scale: [1, 0.3, 1] }
                        : state === 'error'
                        ? { x: [0, -2, 0], y: [0, 2, 0] }
                        : {}
                    }
                    transition={{ duration: 0.4, repeat: Infinity }}
                  />
                </div>
              </motion.div>

              {/* Ojo derecho */}
              <motion.div
                className="relative"
                animate={
                  state === 'typing-email'
                    ? { scale: [1, 1.15, 1] }
                    : state === 'typing-password'
                    ? { scale: [1, 0.7, 1], opacity: [1, 0.4, 1] }
                    : state === 'error'
                    ? { y: [0, 3, 0], rotate: [0, 5, 0] }
                    : state === 'success'
                    ? { scale: [1, 1.2, 1] }
                    : {}
                }
                transition={{ duration: 0.6, repeat: Infinity, delay: 0.1 }}
              >
                <div className="w-8 h-8 bg-white rounded-full shadow-inner flex items-center justify-center overflow-hidden">
                  <motion.div
                    className="w-5 h-5 bg-blue-900 rounded-full"
                    animate={
                      state === 'typing-email'
                        ? { x: [0, 3, 0], y: [0, -2, 0] }
                        : state === 'typing-password'
                        ? { scale: [1, 0.3, 1] }
                        : state === 'error'
                        ? { x: [0, 2, 0], y: [0, 2, 0] }
                        : {}
                    }
                    transition={{ duration: 0.4, repeat: Infinity, delay: 0.1 }}
                  />
                </div>
              </motion.div>
            </div>

            {/* Manos cubriendo ojos cuando escribe contraseña */}
            <AnimatePresence>
              {state === 'typing-password' && (
                <>
                  <motion.div
                    initial={{ x: -20, opacity: 0 }}
                    animate={{ x: 8, opacity: 1 }}
                    exit={{ x: -20, opacity: 0 }}
                    className="absolute top-4 left-4 w-10 h-10 rounded-full"
                    style={{
                      background: 'linear-gradient(135deg, #a8d8ea 0%, #7bb3d3 100%)',
                      boxShadow: '0 4px 10px rgba(0,0,0,0.2)',
                    }}
                  />
                  <motion.div
                    initial={{ x: 20, opacity: 0 }}
                    animate={{ x: -8, opacity: 1 }}
                    exit={{ x: 20, opacity: 0 }}
                    className="absolute top-4 right-4 w-10 h-10 rounded-full"
                    style={{
                      background: 'linear-gradient(135deg, #a8d8ea 0%, #7bb3d3 100%)',
                      boxShadow: '0 4px 10px rgba(0,0,0,0.2)',
                    }}
                  />
                </>
              )}
            </AnimatePresence>

            {/* Boca/Expresión */}
            <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
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
                    className="w-10 h-1 bg-blue-800 rounded-full"
                  />
                )}
              </AnimatePresence>
            </div>

            {/* Mejillas rosadas (solo en estados felices) */}
            {(state === 'idle' || state === 'success') && (
              <>
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute bottom-12 left-6 w-4 h-3 rounded-full bg-pink-300 opacity-60"
                />
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute bottom-12 right-6 w-4 h-3 rounded-full bg-pink-300 opacity-60"
                />
              </>
            )}

            {/* Detalles decorativos - pequeños círculos */}
            <div className="absolute top-3 left-3 w-2 h-2 bg-white/40 rounded-full" />
            <div className="absolute top-3 right-3 w-2 h-2 bg-white/40 rounded-full" />
          </motion.div>

          {/* Partículas de celebración cuando es éxito */}
          <AnimatePresence>
            {state === 'success' && (
              <>
                {[...Array(6)].map((_, i) => (
                  <motion.div
                    key={i}
                    initial={{ scale: 0, x: 0, y: 0, opacity: 1 }}
                    animate={{
                      scale: [0, 1, 0],
                      x: Math.cos((i * Math.PI * 2) / 6) * 40,
                      y: Math.sin((i * Math.PI * 2) / 6) * 40,
                      opacity: [1, 1, 0],
                    }}
                    exit={{ scale: 0, opacity: 0 }}
                    transition={{
                      duration: 1,
                      delay: i * 0.1,
                      repeat: 2,
                    }}
                    className="absolute top-1/2 left-1/2 w-3 h-3 rounded-full"
                    style={{
                      background: ['#fbbf24', '#f59e0b', '#ef4444', '#10b981', '#3b82f6', '#8b5cf6'][i],
                    }}
                  />
                ))}
              </>
            )}
          </AnimatePresence>
        </div>
      </motion.div>

      {/* Mensaje de estado mejorado */}
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
            🙈 No miro, no miro...
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  );
}
