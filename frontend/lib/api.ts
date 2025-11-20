/**
 * Cliente API para consumir el backend Django con JWT
 */
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Configurar axios
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token JWT a las requests
apiClient.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para refrescar token cuando expire
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const { data } = await axios.post(`${API_URL}/api/auth/token/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = data;
          localStorage.setItem('access_token', access);
          originalRequest.headers.Authorization = `Bearer ${access}`;

          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        // Si falla el refresh, limpiar tokens y redirigir a login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Tipos de datos
export interface Configuracion {
  nombre_comercial: string;
  lema: string;
  logo: string | null;
  color_principal: string;
  whatsapp: string;
  email: string;
  telefono: string;
  direccion: string;
  horarios: {
    lunes_viernes: string;
    sabados: string;
    domingos: string;
  };
  redes_sociales: {
    instagram: string;
    facebook: string;
  };
  envios: {
    disponibles: boolean;
    costo_local: number | null;
    costo_nacional: number | null;
  };
  metodos_pago: {
    efectivo: boolean;
    transferencia: boolean;
    tarjeta: boolean;
  };
}

export interface Categoria {
  id: number;
  nombre: string;
  descripcion: string;
  productos_count: number;
  parent: number | null;
}

export interface Proveedor {
  id: number;
  nombre: string;
  productos_count: number;
}

export interface Atributos {
  atributos_1: string[];
  atributos_2: string[];
}

export interface Producto {
  id: number;
  sku: string;
  nombre: string;
  nombre_variante: string;
  descripcion: string;
  categoria: {
    id: number | null;
    nombre: string | null;
  };
  atributos: {
    atributo_1: string;
    atributo_2: string;
    display: string;
  };
  stock: {
    actual: number;
    minimo: number;
    disponible: boolean;
  };
  precios: {
    minorista: {
      ars: number | null;
      usd: number | null;
    };
    mayorista: {
      ars: number | null;
      usd: number | null;
    };
    final: {
      ars: number | null;
      usd: number | null;
      tipo: string;
    };
  };
  imagenes: (string | null)[];
  codigo_barras: string;
  qr_code: string;
  activo: boolean;
  relacionados?: Producto[];
}

export interface CarritoItem {
  variante_id: number;
  sku: string;
  nombre: string;
  descripcion: string;
  cantidad: number;
  precio_unitario_ars: number;
  stock_actual: number;
}

export interface Carrito {
  items: CarritoItem[];
  total_items: number;
  total_ars: number;
}

export interface Usuario {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  tipo_usuario: 'MINORISTA' | 'MAYORISTA';
  is_staff: boolean;
  documento?: string;  // DNI
  telefono?: string;
  direccion?: string;
  ciudad?: string;
}

export interface DireccionEnvio {
  id: number;
  nombre: string;
  telefono: string;
  direccion: string;
  ciudad: string;
  codigo_postal?: string;
  provincia?: string;
  pais: string;
  es_principal: boolean;
}

export interface Favorito {
  id: number;
  variante_id: number;
  producto_nombre: string;
  sku: string;
  creado: string;
}

export interface Pedido {
  id: string;
  fecha: string;
  cliente_nombre: string;
  total_ars: number;
  status: string;
  status_display?: string;
  metodo_pago: string;
  metodo_pago_display?: string;
  items_count: number;
  origen?: string;
  origen_display?: string;
  motivo_cancelacion?: string;
}

// Funciones API
export const api = {
  // Configuraciones
  async getConfiguraciones(): Promise<Configuracion> {
    const { data } = await apiClient.get('/api/configuraciones/');
    return data;
  },

  // Categorías
  async getCategorias(): Promise<Categoria[]> {
    const { data } = await apiClient.get('/api/categorias/');
    return data.categorias;
  },

  // Proveedores (Marcas)
  async getProveedores(): Promise<Proveedor[]> {
    const { data } = await apiClient.get('/api/proveedores/');
    return data.proveedores;
  },

  // Atributos
  async getAtributos(): Promise<Atributos> {
    const { data } = await apiClient.get('/api/atributos/');
    return data;
  },

  // Productos
  async getProductos(params?: {
    categoria?: number;
    proveedor?: number;
    atributo_1?: string;
    atributo_2?: string;
    q?: string;
    tipo_precio?: string;
    min_precio?: number;
    max_precio?: number;
    solo_disponibles?: boolean;
    ordenar?: string;
    page?: number;
    page_size?: number;
  }): Promise<{
    productos: Producto[];
    paginacion: {
      page: number;
      page_size: number;
      total_pages: number;
      total_items: number;
      has_next: boolean;
      has_previous: boolean;
    };
  }> {
    const { data } = await apiClient.get('/api/productos/', { params });
    return data;
  },

  async getProductoDestacados(tipo_precio?: string): Promise<Producto[]> {
    const { data } = await apiClient.get('/api/productos/destacados/', {
      params: { tipo_precio },
    });
    return data.productos;
  },

  async getProducto(id: number, tipo_precio?: string): Promise<Producto> {
    const { data } = await apiClient.get(`/api/productos/${id}/`, {
      params: { tipo_precio },
    });
    return data;
  },

  // Autenticación JWT
  async login(username: string, password: string): Promise<{ user: Usuario; tokens: { access: string; refresh: string } }> {
    const { data } = await apiClient.post('/api/auth/login/', {
      username,
      password,
    });
    
    if (data.success && data.tokens) {
      // Guardar tokens
      localStorage.setItem('access_token', data.tokens.access);
      localStorage.setItem('refresh_token', data.tokens.refresh);
      return { user: data.user, tokens: data.tokens };
    }
    throw new Error(data.error || 'Error al iniciar sesión');
  },

  async registro(data: {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
    first_name?: string;
    last_name?: string;
    telefono?: string;
    dni: string;  // DNI obligatorio
  }): Promise<{ user: Usuario; tokens: { access: string; refresh: string } }> {
    const response = await apiClient.post('/api/auth/registro/', data);
    
    if (response.data.success && response.data.tokens) {
      // Guardar tokens
      localStorage.setItem('access_token', response.data.tokens.access);
      localStorage.setItem('refresh_token', response.data.tokens.refresh);
      return { user: response.data.user, tokens: response.data.tokens };
    }
    throw new Error(response.data.error || 'Error al registrar');
  },

  async getUsuarioActual(): Promise<Usuario | null> {
    try {
      const { data } = await apiClient.get('/api/auth/usuario/');
      return data.user;
    } catch {
      return null;
    }
  },

  async logout(): Promise<void> {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  async actualizarPerfil(data: Partial<Usuario & { telefono?: string; direccion?: string; ciudad?: string }>): Promise<Usuario> {
    const { data: response } = await apiClient.put('/api/auth/perfil/', data);
    return response.user;
  },

  // Carrito
  async getCarrito(): Promise<Carrito> {
    const { data } = await apiClient.get('/api/carrito/');
    return {
      items: data.items || [],
      total_items: data.total_items || 0,
      total_ars: data.total_ars || 0,
    };
  },

  async agregarAlCarrito(
    variante_id: number,
    cantidad: number = 1,
    tipo_precio?: string
  ): Promise<Carrito> {
    const { data } = await apiClient.post('/api/carrito/', {
      variante_id,
      cantidad,
      tipo_precio,
    });
    if (data.success) {
      return {
        items: data.items || [],
        total_items: data.total_items || 0,
        total_ars: data.total_ars || 0,
      };
    }
    throw new Error(data.error || 'Error al agregar al carrito');
  },

  async eliminarDelCarrito(item_index: number): Promise<void> {
    await apiClient.delete(`/api/carrito/item/${item_index}/`);
  },

  async limpiarCarrito(): Promise<void> {
    await apiClient.post('/api/carrito/limpiar/');
  },

  // Pedidos
  async crearPedido(pedido: {
    cliente_nombre: string;
    cliente_documento?: string;
    metodo_pago: string;
    nota?: string;
  }): Promise<{ venta_id: string; total: number }> {
    const { data } = await apiClient.post('/api/pedido/', pedido);
    if (data.success) {
      return {
        venta_id: data.venta_id,
        total: data.total,
      };
    }
    throw new Error(data.error || 'Error al crear el pedido');
  },

  // Direcciones
  async getDirecciones(): Promise<DireccionEnvio[]> {
    const { data } = await apiClient.get('/api/direcciones/');
    return data.direcciones;
  },

  async crearDireccion(direccion: Omit<DireccionEnvio, 'id'>): Promise<DireccionEnvio> {
    const { data } = await apiClient.post('/api/direcciones/', direccion);
    return data.direccion;
  },

  // Favoritos
  async getFavoritos(): Promise<Favorito[]> {
    const { data } = await apiClient.get('/api/favoritos/');
    return data.favoritos;
  },

  async agregarFavorito(variante_id: number): Promise<void> {
    await apiClient.post(`/api/favoritos/${variante_id}/`);
  },

  async eliminarFavorito(variante_id: number): Promise<void> {
    await apiClient.delete(`/api/favoritos/${variante_id}/`);
  },

  // Historial
  async getPedidos(): Promise<{ pedidos: Pedido[] }> {
    const { data } = await apiClient.get('/api/historial/');
    return { pedidos: data.pedidos || [] };
  },

  async getPedido(id: string): Promise<Pedido> {
    const { data } = await apiClient.get(`/api/pedidos/${id}/`);
    return data;
  },
};

export default apiClient;
