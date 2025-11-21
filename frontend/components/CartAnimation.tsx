'use client';

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Image from 'next/image';

interface CartAnimationProps {
  productImage: string;
  productName: string;
  cartPosition: { x: number; y: number };
  onComplete: () => void;
}

export default function CartAnimation({
  productImage,
  productName,
  cartPosition,
  onComplete,
}: CartAnimationProps) {
  const [isAnimating, setIsAnimating] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsAnimating(false);
      setTimeout(onComplete, 100);
    }, 600);

    return () => clearTimeout(timer);
  }, [onComplete]);

  if (!isAnimating) return null;

  return (
    <div className="fixed inset-0 pointer-events-none z-50">
      <motion.div
        initial={{
          x: 0,
          y: 0,
          scale: 1,
          rotateZ: 0,
        }}
        animate={{
          x: cartPosition.x,
          y: cartPosition.y,
          scale: 0.3,
          rotateZ: 360,
        }}
        transition={{
          duration: 0.6,
          ease: [0.68, -0.55, 0.265, 1.55],
        }}
        className="absolute"
        style={{
          left: '50%',
          top: '50%',
          transform: 'translate(-50%, -50%)',
        }}
      >
        <div className="relative w-20 h-20 rounded-lg overflow-hidden shadow-2xl border-2 border-white">
          <Image
            src={productImage}
            alt={productName}
            fill
            className="object-cover"
            sizes="80px"
          />
        </div>
      </motion.div>
    </div>
  );
}

// Hook para obtener la posición del carrito
export function useCartPosition() {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const updatePosition = () => {
      const cartButton = document.querySelector('[data-cart-button]');
      if (cartButton) {
        const rect = cartButton.getBoundingClientRect();
        setPosition({
          x: rect.left + rect.width / 2 - window.innerWidth / 2,
          y: rect.top + rect.height / 2 - window.innerHeight / 2,
        });
      }
    };

    updatePosition();
    window.addEventListener('resize', updatePosition);
    window.addEventListener('scroll', updatePosition);

    return () => {
      window.removeEventListener('resize', updatePosition);
      window.removeEventListener('scroll', updatePosition);
    };
  }, []);

  return position;
}

