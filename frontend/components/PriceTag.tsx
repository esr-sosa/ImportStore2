'use client';

interface PriceTagProps {
  precio: number | null;
  precioUSD?: number | null;
  precioOriginal?: number | null;
  moneda?: 'ARS' | 'USD';
  size?: 'sm' | 'md' | 'lg';
  showDiscount?: boolean;
  showBoth?: boolean; // Mostrar USD y ARS juntos
}

export default function PriceTag({
  precio,
  precioUSD,
  precioOriginal,
  moneda = 'ARS',
  size = 'md',
  showDiscount = true,
  showBoth = false,
}: PriceTagProps) {
  if (!precio && !precioUSD) {
    return <span className="text-gray-500 text-sm">Precio no disponible</span>;
  }

  const tieneDescuento = precioOriginal && precioOriginal > (precio || precioUSD || 0);
  const porcentajeDescuento = tieneDescuento
    ? Math.round(((precioOriginal! - (precio || precioUSD || 0)) / precioOriginal!) * 100)
    : 0;

  const sizeClasses = {
    sm: 'text-sm',
    md: 'text-lg',
    lg: 'text-2xl',
  };

  const formatPrice = (amount: number, currency: 'ARS' | 'USD') => {
    if (currency === 'USD') {
      return `US$ ${amount.toLocaleString('es-AR', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
    }
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  // Si showBoth es true, mostrar USD y ARS juntos
  if (showBoth && precioUSD && precio) {
    return (
      <div className="flex flex-col">
        {tieneDescuento && showDiscount && precioOriginal && (
          <div className="flex items-center space-x-2 mb-1">
            <span className="text-xs text-gray-500 line-through">
              {formatPrice(precioOriginal, moneda)}
            </span>
            <span className="bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">
              -{porcentajeDescuento}%
            </span>
          </div>
        )}
        <div className="flex items-baseline gap-2 flex-wrap">
          <span className={`font-bold ${sizeClasses[size]} text-gray-900`}>
            {formatPrice(precioUSD, 'USD')}
          </span>
          <span className="text-gray-400 text-sm">·</span>
          <span className={`font-semibold ${sizeClasses[size] === 'text-2xl' ? 'text-lg' : sizeClasses[size] === 'text-lg' ? 'text-base' : 'text-sm'} text-gray-700`}>
            {formatPrice(precio, 'ARS')}
          </span>
        </div>
        <span className="text-xs text-gray-500 mt-1" title="Precio convertido con LolaBlue (fuente backend)">
          Precio convertido con LolaBlue
        </span>
      </div>
    );
  }

  // Mostrar solo un precio
  const precioMostrar = precio || precioUSD || 0;
  const monedaMostrar = precio ? 'ARS' : 'USD';

  return (
    <div className="flex flex-col">
      {tieneDescuento && showDiscount && precioOriginal && (
        <div className="flex items-center space-x-2 mb-1">
          <span className="text-xs text-gray-500 line-through">
            {formatPrice(precioOriginal, monedaMostrar)}
          </span>
          <span className="bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">
            -{porcentajeDescuento}%
          </span>
        </div>
      )}
      <span className={`font-bold ${sizeClasses[size]} text-gray-900`}>
        {formatPrice(precioMostrar, monedaMostrar)}
      </span>
    </div>
  );
}
