'use client';

import { useEffect } from 'react';
import { useConfigStore } from '@/stores/configStore';
import { useAuthStore } from '@/stores/authStore';

export default function ConfigProvider({ children }: { children: React.ReactNode }) {
  const { loadConfig } = useConfigStore();
  const { checkAuth } = useAuthStore();

  useEffect(() => {
    // Cargar en background sin bloquear el render
    loadConfig();
    checkAuth();
  }, [loadConfig, checkAuth]);

  // Renderizar inmediatamente sin esperar (evita flash y hace todo más rápido)
  return <>{children}</>;
}

