'use client';

import { useEffect } from 'react';
import { useConfigStore } from '@/stores/configStore';
import { useAuthStore } from '@/stores/authStore';

export default function ConfigProvider({ children }: { children: React.ReactNode }) {
  const { loadConfig } = useConfigStore();
  const { checkAuth } = useAuthStore();

  useEffect(() => {
    loadConfig();
    checkAuth();
  }, [loadConfig, checkAuth]);

  return <>{children}</>;
}

