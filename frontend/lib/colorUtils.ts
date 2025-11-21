/**
 * Utilidades para trabajar con colores y contraste
 */

/**
 * Convierte un color HEX a RGB
 */
function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      }
    : null;
}

/**
 * Calcula la luminancia relativa de un color (según WCAG)
 * Retorna un valor entre 0 (negro) y 1 (blanco)
 */
function getLuminance(hex: string): number {
  const rgb = hexToRgb(hex);
  if (!rgb) return 0.5; // Default si no se puede parsear

  const [r, g, b] = [rgb.r, rgb.g, rgb.b].map((val) => {
    val = val / 255;
    return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
  });

  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

/**
 * Determina si un color es claro u oscuro
 * Retorna true si el color es claro (necesita texto oscuro)
 * Retorna false si el color es oscuro (necesita texto claro)
 */
export function isLightColor(hex: string): boolean {
  const luminance = getLuminance(hex);
  return luminance > 0.5;
}

/**
 * Obtiene la clase de texto apropiada según el color de fondo
 */
export function getTextColorClass(backgroundColor: string): string {
  return isLightColor(backgroundColor) ? 'text-gray-900' : 'text-white';
}

/**
 * Obtiene el color de texto apropiado como estilo inline
 */
export function getTextColorStyle(backgroundColor: string): { color: string } {
  return {
    color: isLightColor(backgroundColor) ? '#111827' : '#ffffff',
  };
}

