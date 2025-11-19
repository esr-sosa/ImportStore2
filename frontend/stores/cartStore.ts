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
        try {
          // Obtener tipo de usuario autenticado
          const { useAuthStore } = await import('./authStore');
          const { user } = useAuthStore.getState();
          const tipo_precio = user?.tipo_usuario || 'MINORISTA';
          
          // Intentar agregar al backend si está autenticado
          try {
            const carrito = await api.agregarAlCarrito(variante_id, cantidad, tipo_precio);
            set({
              items: carrito.items || [],
              total_items: carrito.total_items || 0,
              total_ars: carrito.total_ars || 0,
              isLoading: false,
            });
          } catch (backendError: any) {
            // Si falla el backend (usuario no autenticado), agregar localmente
            const state = get();
            const existingItem = state.items.find(item => item.variante_id === variante_id);
            
            let newItems: CarritoItem[];
            if (existingItem) {
              newItems = state.items.map(item =>
                item.variante_id === variante_id
                  ? { ...item, cantidad: item.cantidad + cantidad }
                  : item
              );
            } else {
              // Necesitamos obtener el producto para crear el item
              try {
                const producto = await api.getProducto(variante_id, tipo_precio);
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
              } catch {
                throw backendError; // Si no podemos obtener el producto, lanzar error original
              }
            }
            
            const total_items = newItems.reduce((sum, item) => sum + item.cantidad, 0);
            const total_ars = newItems.reduce((sum, item) => sum + (item.precio_unitario_ars * item.cantidad), 0);
            
            set({
              items: newItems,
              total_items,
              total_ars,
              isLoading: false,
            });
          }
        } catch (error: any) {
          set({
            error: error.message || 'Error al agregar al carrito',
            isLoading: false,
          });
          throw error;
        }
      },

      eliminarItem: async (item_index) => {
        set({ isLoading: true, error: null });
        try {
          // Intentar eliminar del backend
          try {
            await api.eliminarDelCarrito(item_index);
            const carrito = await api.getCarrito();
            set({
              items: carrito.items || [],
              total_items: carrito.total_items || 0,
              total_ars: carrito.total_ars || 0,
              isLoading: false,
            });
          } catch {
            // Si falla, eliminar localmente
            const state = get();
            const newItems = state.items.filter((_, index) => index !== item_index);
            const total_items = newItems.reduce((sum, item) => sum + item.cantidad, 0);
            const total_ars = newItems.reduce((sum, item) => sum + (item.precio_unitario_ars * item.cantidad), 0);
            
            set({
              items: newItems,
              total_items,
              total_ars,
              isLoading: false,
            });
          }
        } catch (error: any) {
          set({
            error: error.message || 'Error al eliminar del carrito',
            isLoading: false,
          });
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
        if (item) {
          // Intentar actualizar en backend
          try {
            await get().eliminarItem(item_index);
            await get().agregarItem(item.variante_id, cantidad);
          } catch {
            // Si falla, actualizar localmente
            const newItems = items.map((it, idx) =>
              idx === item_index ? { ...it, cantidad } : it
            );
            const total_items = newItems.reduce((sum, item) => sum + item.cantidad, 0);
            const total_ars = newItems.reduce((sum, item) => sum + (item.precio_unitario_ars * item.cantidad), 0);
            
            set({
              items: newItems,
              total_items,
              total_ars,
            });
          }
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
