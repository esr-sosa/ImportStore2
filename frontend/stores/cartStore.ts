/**
 * Store de Zustand para el carrito de compras
 * Con persistencia en localStorage y sincronización con backend
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { api, Carrito, CarritoItem } from '@/lib/api';

interface CartState {
  items: CarritoItem[];
  total_items: number;
  total_ars: number;
  isLoading: boolean;
  error: string | null;
  
  // Acciones
  loadCarrito: () => Promise<void>;
  agregarItem: (variante_id: number, cantidad?: number) => Promise<void>;
  eliminarItem: (item_index: number) => Promise<void>;
  limpiarCarrito: () => Promise<void>;
  actualizarCantidad: (item_index: number, cantidad: number) => Promise<void>;
  sincronizarConBackend: () => Promise<void>;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      total_items: 0,
      total_ars: 0,
      isLoading: false,
      error: null,

      loadCarrito: async () => {
        set({ isLoading: true, error: null });
        try {
          // Intentar cargar desde backend si el usuario está autenticado
          try {
            const carrito = await api.getCarrito();
            set({
              items: carrito.items || [],
              total_items: carrito.total_items || 0,
              total_ars: carrito.total_ars || 0,
              isLoading: false,
            });
          } catch (error: any) {
            // Si falla (usuario no autenticado), mantener items de localStorage
            const state = get();
            set({
              isLoading: false,
              // Mantener items existentes de localStorage
            });
          }
        } catch (error: any) {
          set({
            error: error.message || 'Error al cargar el carrito',
            isLoading: false,
          });
        }
      },

      agregarItem: async (variante_id, cantidad = 1) => {
        set({ isLoading: true, error: null });
        const state = get();
        const { useAuthStore } = await import('./authStore');
        const { user } = useAuthStore.getState();
        const tipo_precio = user?.tipo_usuario || 'MINORISTA';
        
        try {
          // PASO 1: Obtener información del producto para validar stock
          let producto;
          try {
            producto = await api.getProducto(variante_id, tipo_precio);
          } catch (error: any) {
            throw new Error('Producto no encontrado');
          }
          
          // PASO 2: Validar stock disponible
          if (!producto.stock.disponible || producto.stock.actual <= 0) {
            throw new Error('Producto sin stock disponible');
          }
          
          // PASO 3: Verificar cantidad solicitada vs stock disponible
          const existingItem = state.items.find(item => item.variante_id === variante_id);
          const cantidad_actual = existingItem ? existingItem.cantidad : 0;
          const cantidad_total = cantidad_actual + cantidad;
          
          if (cantidad_total > producto.stock.actual) {
            throw new Error(`Stock insuficiente. Disponible: ${producto.stock.actual}, solicitado: ${cantidad_total}`);
          }
          
          // PASO 4: Intentar agregar al backend primero (validación del servidor)
          try {
            const carrito = await api.agregarAlCarrito(variante_id, cantidad, tipo_precio);
            // Si éxito, actualizar con datos del backend
            set({
              items: carrito.items || [],
              total_items: carrito.total_items || 0,
              total_ars: carrito.total_ars || 0,
              isLoading: false,
            });
          } catch (backendError: any) {
            // Si el backend falla por autenticación, agregar localmente
            if (backendError.response?.status === 401) {
              // Usuario no autenticado - agregar localmente
              let newItems: CarritoItem[];
              
              if (existingItem) {
                newItems = state.items.map(item =>
                  item.variante_id === variante_id
                    ? { ...item, cantidad: item.cantidad + cantidad, stock_actual: producto.stock.actual }
                    : item
                );
              } else {
                const newItem: CarritoItem = {
                  variante_id: producto.id,
                  sku: producto.sku,
                  nombre: producto.nombre,
                  descripcion: producto.descripcion || producto.nombre,
                  cantidad: cantidad,
                  precio_unitario_ars: producto.precios.final.ars || 0,
                  stock_actual: producto.stock.actual,
                };
                newItems = [...state.items, newItem];
              }
              
              const total_items = newItems.reduce((sum, item) => sum + item.cantidad, 0);
              const total_ars = newItems.reduce((sum, item) => sum + (item.precio_unitario_ars * item.cantidad), 0);
              
              set({
                items: newItems,
                total_items,
                total_ars,
                isLoading: false,
              });
            } else {
              // Otro error del backend - lanzar para que se maneje arriba
              throw backendError;
            }
          }
        } catch (error: any) {
          const errorMessage = error.response?.data?.error || error.message || 'Error al agregar al carrito';
          set({
            error: errorMessage,
            isLoading: false,
          });
          throw new Error(errorMessage);
        }
      },

      eliminarItem: async (item_index) => {
        // ACTUALIZACIÓN OPTIMISTA: Eliminar inmediatamente de la UI
        const state = get();
        const newItems = state.items.filter((_, index) => index !== item_index);
        const total_items = newItems.reduce((sum, item) => sum + item.cantidad, 0);
        const total_ars = newItems.reduce((sum, item) => sum + (item.precio_unitario_ars * item.cantidad), 0);
        
        // Actualizar UI inmediatamente
        set({
          items: newItems,
          total_items,
          total_ars,
          isLoading: false,
        });
        
        // Sincronizar con backend en background
        try {
          await api.eliminarDelCarrito(item_index);
          const carrito = await api.getCarrito();
          set({
            items: carrito.items || newItems,
            total_items: carrito.total_items || total_items,
            total_ars: carrito.total_ars || total_ars,
          });
        } catch (error) {
          // Si falla, mantener estado local (ya actualizado)
          console.warn('Error sincronizando eliminación con backend:', error);
        }
      },

      limpiarCarrito: async () => {
        set({ isLoading: true, error: null });
        try {
          try {
            await api.limpiarCarrito();
          } catch {
            // Si falla, limpiar localmente
          }
          set({
            items: [],
            total_items: 0,
            total_ars: 0,
            isLoading: false,
          });
        } catch (error: any) {
          set({
            error: error.message || 'Error al limpiar el carrito',
            isLoading: false,
          });
        }
      },

      actualizarCantidad: async (item_index, cantidad) => {
        const { items } = get();
        if (cantidad <= 0) {
          await get().eliminarItem(item_index);
          return;
        }
        
        const item = items[item_index];
        if (!item) {
          throw new Error('Item no encontrado');
        }
        
        // Validar stock antes de actualizar
        if (cantidad > item.stock_actual) {
          throw new Error(`Stock insuficiente. Disponible: ${item.stock_actual}, solicitado: ${cantidad}`);
        }
        
        // Actualizar cantidad usando agregarItem que ya valida stock
        try {
          // Calcular diferencia de cantidad
          const diferencia = cantidad - item.cantidad;
          if (diferencia > 0) {
            // Agregar más cantidad
            await get().agregarItem(item.variante_id, diferencia);
          } else if (diferencia < 0) {
            // Reducir cantidad - eliminar y volver a agregar con nueva cantidad
            await get().eliminarItem(item_index);
            if (cantidad > 0) {
              await get().agregarItem(item.variante_id, cantidad);
            }
          }
        } catch (error: any) {
          throw error;
        }
      },

      sincronizarConBackend: async () => {
        // Sincronizar carrito local con backend cuando el usuario se autentica
        const { items } = get();
        if (items.length === 0) {
          await get().loadCarrito();
          return;
        }

        try {
          // Agregar todos los items locales al backend
          for (const item of items) {
            try {
              await api.agregarAlCarrito(item.variante_id, item.cantidad);
            } catch {
              // Ignorar errores individuales
            }
          }
          // Recargar desde backend
          await get().loadCarrito();
        } catch (error) {
          console.error('Error sincronizando carrito:', error);
        }
      },
    }),
    {
      name: 'cart-storage',
      partialize: (state) => ({
        items: state.items,
        total_items: state.total_items,
        total_ars: state.total_ars,
      }),
    }
  )
);
