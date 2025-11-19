/**
 * Store de Zustand para configuraciones de la tienda
 */
import { create } from 'zustand';
import { api, Configuracion } from '@/lib/api';

interface ConfigState {
  config: Configuracion | null;
  isLoading: boolean;
  error: string | null;
  
  // Acciones
  loadConfig: () => Promise<void>;
  getColorPrimary: () => string;
  getLogo: () => string | null;
}

export const useConfigStore = create<ConfigState>((set, get) => ({
  config: null,
  isLoading: false,
  error: null,

  loadConfig: async () => {
    set({ isLoading: true, error: null });
    try {
      const config = await api.getConfiguraciones();
      set({ config, isLoading: false });
      
      // Aplicar color principal como variable CSS
      if (typeof document !== 'undefined' && config.color_principal) {
        document.documentElement.style.setProperty('--color-primary', config.color_principal);
      }
    } catch (error: any) {
      set({
        error: error.message || 'Error al cargar configuraciones',
        isLoading: false,
      });
    }
  },

  getColorPrimary: () => {
    const { config } = get();
    return config?.color_principal || '#2563eb';
  },

  getLogo: () => {
    const { config } = get();
    return config?.logo || null;
  },
}));

