'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { FiFilter, FiX } from 'react-icons/fi';
import { api, Producto, Categoria } from '@/lib/api';
import ProductCard from '@/components/ProductCard';
import { useAuthStore } from '@/stores/authStore';

export default function ProductosPage() {
  const searchParams = useSearchParams();
  const { user } = useAuthStore();
  const [productos, setProductos] = useState<Producto[]>([]);
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    categoria: searchParams.get('categoria') || '',
    q: searchParams.get('q') || '',
    min_precio: '',
    max_precio: '',
    solo_disponibles: true,
    ordenar: 'recientes',
  });
  const [paginacion, setPaginacion] = useState({
    page: 1,
    total_pages: 1,
    has_next: false,
    has_previous: false,
  });
  const [precioRange, setPrecioRange] = useState({ min: 0, max: 1000000 });

  useEffect(() => {
    loadCategorias();
    // Calcular rango de precios inicial
    calcularRangoPrecios();
  }, []);

  useEffect(() => {
    loadProductos();
  }, [filters, paginacion.page, user]);

  const loadCategorias = async () => {
    try {
      const cats = await api.getCategorias();
      setCategorias(cats);
    } catch (error) {
      console.error('Error cargando categorías:', error);
    }
  };

  const calcularRangoPrecios = async () => {
    try {
      const tipo_precio = user?.tipo_usuario || 'MINORISTA';
      const response = await api.getProductos({
        tipo_precio,
        page_size: 100, // Obtener más productos para calcular rango
      });
      
      const precios = response.productos
        .map(p => p.precios.final.ars)
        .filter(p => p !== null && p !== undefined) as number[];
      
      if (precios.length > 0) {
        setPrecioRange({
          min: Math.floor(Math.min(...precios)),
          max: Math.ceil(Math.max(...precios)),
        });
        // Establecer valores iniciales de filtro
        if (!filters.min_precio && !filters.max_precio) {
          setFilters(prev => ({
            ...prev,
            min_precio: Math.floor(Math.min(...precios)).toString(),
            max_precio: Math.ceil(Math.max(...precios)).toString(),
          }));
        }
      }
    } catch (error) {
      console.error('Error calculando rango de precios:', error);
    }
  };

  const loadProductos = async () => {
    setIsLoading(true);
    try {
      // Usar tipo_usuario del usuario autenticado
      const tipo_precio = user?.tipo_usuario || 'MINORISTA';
      
      const params: any = {
        ...filters,
        tipo_precio,
        page: paginacion.page,
        page_size: 20,
      };
      
      // Limpiar parámetros vacíos
      Object.keys(params).forEach((key) => {
        if (params[key] === '' || params[key] === null) {
          delete params[key];
        }
      });
      
      // Convertir precios a números
      if (params.min_precio) params.min_precio = parseFloat(params.min_precio);
      if (params.max_precio) params.max_precio = parseFloat(params.max_precio);
      
      const response = await api.getProductos(params);
      setProductos(response.productos);
      setPaginacion(response.paginacion);
    } catch (error) {
      console.error('Error cargando productos:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (key: string, value: string | boolean) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
    setPaginacion((prev) => ({ ...prev, page: 1 }));
  };

  const limpiarFiltros = () => {
    setFilters({
      categoria: '',
      q: '',
      min_precio: precioRange.min.toString(),
      max_precio: precioRange.max.toString(),
      solo_disponibles: true,
      ordenar: 'recientes',
    });
    setPaginacion((prev) => ({ ...prev, page: 1 }));
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Catálogo de Productos</h1>
          <p className="text-gray-600">Encontrá los mejores productos premium</p>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar Filtros */}
          <aside className="lg:w-80 flex-shrink-0">
            <div className="bg-white rounded-2xl p-6 shadow-sm sticky top-24">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-gray-900">Filtros</h2>
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className="lg:hidden"
                >
                  {showFilters ? <FiX className="w-5 h-5" /> : <FiFilter className="w-5 h-5" />}
                </button>
              </div>

              <div className={`space-y-6 ${showFilters ? 'block' : 'hidden lg:block'}`}>
                {/* Buscar */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Buscar
                  </label>
                  <input
                    type="text"
                    value={filters.q}
                    onChange={(e) => handleFilterChange('q', e.target.value)}
                    placeholder="Nombre, SKU..."
                    className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                  />
                </div>

                {/* Categorías */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Categoría
                  </label>
                  <select
                    value={filters.categoria}
                    onChange={(e) => handleFilterChange('categoria', e.target.value)}
                    className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                  >
                    <option value="">Todas las categorías</option>
                    {categorias.map((cat) => (
                      <option key={cat.id} value={cat.id}>
                        {cat.nombre} ({cat.productos_count})
                      </option>
                    ))}
                  </select>
                </div>

                {/* Rango de Precio - Slider */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Rango de Precio (ARS)
                  </label>
                  <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-2">
                      <div>
                        <label className="text-xs text-gray-500 mb-1 block">Mínimo</label>
                        <input
                          type="number"
                          value={filters.min_precio}
                          onChange={(e) => handleFilterChange('min_precio', e.target.value)}
                          min={precioRange.min}
                          max={precioRange.max}
                          className="w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm text-gray-900 bg-white"
                          placeholder={precioRange.min.toString()}
                        />
                      </div>
                      <div>
                        <label className="text-xs text-gray-500 mb-1 block">Máximo</label>
                        <input
                          type="number"
                          value={filters.max_precio}
                          onChange={(e) => handleFilterChange('max_precio', e.target.value)}
                          min={precioRange.min}
                          max={precioRange.max}
                          className="w-full px-3 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm text-gray-900 bg-white"
                          placeholder={precioRange.max.toString()}
                        />
                      </div>
                    </div>
                    {precioRange.max > precioRange.min && (
                      <div className="px-2">
                        <input
                          type="range"
                          min={precioRange.min}
                          max={precioRange.max}
                          value={filters.max_precio || precioRange.max}
                          onChange={(e) => handleFilterChange('max_precio', e.target.value)}
                          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                        />
                      </div>
                    )}
                  </div>
                </div>

                {/* Disponibilidad */}
                <div>
                  <label className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={filters.solo_disponibles}
                      onChange={(e) => handleFilterChange('solo_disponibles', e.target.checked)}
                      className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <span className="text-sm font-medium text-gray-700">Solo disponibles</span>
                  </label>
                </div>

                {/* Ordenar */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Ordenar por
                  </label>
                  <select
                    value={filters.ordenar}
                    onChange={(e) => handleFilterChange('ordenar', e.target.value)}
                    className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
                  >
                    <option value="recientes">Más recientes</option>
                    <option value="precio_asc">Precio: menor a mayor</option>
                    <option value="precio_desc">Precio: mayor a menor</option>
                    <option value="nombre">Nombre A-Z</option>
                  </select>
                </div>

                {/* Limpiar filtros */}
                <button
                  onClick={limpiarFiltros}
                  className="w-full px-4 py-2 text-sm text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Limpiar Filtros
                </button>
              </div>
            </div>
          </aside>

          {/* Productos */}
          <div className="flex-1">
            {isLoading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="bg-white rounded-2xl h-96 animate-pulse" />
                ))}
              </div>
            ) : productos.length > 0 ? (
              <>
                <div className="mb-4 text-sm text-gray-600">
                  Mostrando {productos.length} de {paginacion.total_items} productos
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                  {productos.map((producto, index) => (
                    <ProductCard key={producto.id} product={producto} index={index} />
                  ))}
                </div>

                {/* Paginación */}
                {paginacion.total_pages > 1 && (
                  <div className="flex justify-center items-center space-x-4">
                    <button
                      onClick={() =>
                        setPaginacion((prev) => ({ ...prev, page: prev.page - 1 }))
                      }
                      disabled={!paginacion.has_previous}
                      className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
                    >
                      Anterior
                    </button>
                    <span className="text-gray-600">
                      Página {paginacion.page} de {paginacion.total_pages}
                    </span>
                    <button
                      onClick={() =>
                        setPaginacion((prev) => ({ ...prev, page: prev.page + 1 }))
                      }
                      disabled={!paginacion.has_next}
                      className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
                    >
                      Siguiente
                    </button>
                  </div>
                )}
              </>
            ) : (
              <div className="bg-white rounded-2xl p-12 text-center">
                <p className="text-gray-500 text-lg">No se encontraron productos</p>
                <p className="text-gray-400 mt-2">Intenta con otros filtros</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
