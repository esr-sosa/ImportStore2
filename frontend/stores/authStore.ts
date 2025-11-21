/**
 * Store de Zustand para autenticación con JWT
 */
import { create } from 'zustand';
import { api, Usuario } from '@/lib/api';

interface AuthState {
  user: Usuario | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  
  // Acciones
  login: (username: string, password: string) => Promise<void>;
  registro: (data: {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
    tipo_usuario: 'MINORISTA' | 'MAYORISTA';
    first_name?: string;
    last_name?: string;
    telefono?: string;
  }) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
  actualizarPerfil: (data: Partial<Usuario>) => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoading: true,
  isAuthenticated: false,

  login: async (username, password) => {
    try {
      const { user } = await api.login(username, password);
      set({
        user,
        isAuthenticated: true,
        isLoading: false,
      });
      // Sincronizar carrito con backend después de login
      try {
        const { useCartStore } = await import('./cartStore');
        await useCartStore.getState().sincronizarConBackend();
      } catch {
        // Ignorar errores de sincronización
      }
    } catch (error: any) {
      set({ isLoading: false });
      throw error;
    }
  },

  registro: async (data) => {
    try {
      const { user } = await api.registro(data);
      // Sincronizar carrito con backend después de registro
      try {
        const { useCartStore } = await import('./cartStore');
        await useCartStore.getState().sincronizarConBackend();
      } catch {
        // Ignorar errores de sincronización
      }
      set({
        user,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch (error: any) {
      set({ isLoading: false });
      throw error;
    }
  },

  logout: async () => {
    try {
      await api.logout();
      set({
        user: null,
        isAuthenticated: false,
      });
    } catch (error) {
      // Aún así, limpiamos el estado local
      set({
        user: null,
        isAuthenticated: false,
      });
    }
  },

  checkAuth: async () => {
    set({ isLoading: true });
    try {
      const user = await api.getUsuarioActual();
      set({
        user,
        isAuthenticated: !!user,
        isLoading: false,
      });
    } catch {
      set({
        user: null,
        isAuthenticated: false,
        isLoading: false,
      });
    }
  },

  actualizarPerfil: async (data) => {
    try {
      const response = await api.actualizarPerfil(data);
      if (response.success && response.user) {
        set({ user: response.user });
      }
    } catch (error) {
      throw error;
    }
  },
}));
