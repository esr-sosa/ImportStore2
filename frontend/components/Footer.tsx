'use client';

import Link from 'next/link';
import { FiInstagram, FiPhone, FiMail, FiMapPin } from 'react-icons/fi';
import { useConfigStore } from '@/stores/configStore';

export default function Footer() {
  const { config } = useConfigStore();
  const colorPrimary = config?.color_principal || '#2563eb';

  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <h3 className="text-2xl font-bold text-white mb-4">
              {config?.nombre_comercial || 'ImportStore'}
            </h3>
            {config?.lema && (
              <p className="text-gray-400 mb-4">{config.lema}</p>
            )}
            <div className="flex space-x-4">
              {config?.redes_sociales?.instagram && (
                <a
                  href={`https://instagram.com/${config.redes_sociales.instagram}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-2 rounded-full bg-gray-800 hover:bg-gray-700 transition-colors"
                >
                  <FiInstagram className="w-5 h-5" />
                </a>
              )}
              {config?.redes_sociales?.facebook && (
                <a
                  href={config.redes_sociales.facebook}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-2 rounded-full bg-gray-800 hover:bg-gray-700 transition-colors"
                >
                  <FiInstagram className="w-5 h-5" />
                </a>
              )}
            </div>
          </div>

          {/* Links */}
          <div>
            <h4 className="text-white font-semibold mb-4">Enlaces</h4>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="hover:text-white transition-colors">
                  Inicio
                </Link>
              </li>
              <li>
                <Link href="/productos" className="hover:text-white transition-colors">
                  Productos
                </Link>
              </li>
              <li>
                <Link href="/categorias" className="hover:text-white transition-colors">
                  Categorías
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-white font-semibold mb-4">Contacto</h4>
            <ul className="space-y-3">
              {config?.telefono && (
                <li className="flex items-center space-x-2">
                  <FiPhone className="w-4 h-4" />
                  <a href={`tel:${config.telefono}`} className="hover:text-white transition-colors">
                    {config.telefono}
                  </a>
                </li>
              )}
              {config?.whatsapp && (
                <li className="flex items-center space-x-2">
                  <FiPhone className="w-4 h-4" />
                  <a
                    href={`https://wa.me/${config.whatsapp.replace(/\D/g, '')}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-white transition-colors"
                  >
                    WhatsApp
                  </a>
                </li>
              )}
              {config?.email && (
                <li className="flex items-center space-x-2">
                  <FiMail className="w-4 h-4" />
                  <a href={`mailto:${config.email}`} className="hover:text-white transition-colors">
                    {config.email}
                  </a>
                </li>
              )}
              {config?.direccion && (
                <li className="flex items-start space-x-2">
                  <FiMapPin className="w-4 h-4 mt-1" />
                  <span className="text-sm">{config.direccion}</span>
                </li>
              )}
            </ul>
          </div>
        </div>

        {/* Horarios */}
        {config?.horarios && (
          <div className="mt-8 pt-8 border-t border-gray-800">
            <h4 className="text-white font-semibold mb-4">Horarios</h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              {config.horarios.lunes_viernes && (
                <div>
                  <span className="font-medium">Lunes a Viernes:</span>{' '}
                  {config.horarios.lunes_viernes}
                </div>
              )}
              {config.horarios.sabados && (
                <div>
                  <span className="font-medium">Sábados:</span> {config.horarios.sabados}
                </div>
              )}
              {config.horarios.domingos && (
                <div>
                  <span className="font-medium">Domingos:</span> {config.horarios.domingos}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Copyright */}
        <div className="mt-8 pt-8 border-t border-gray-800 text-center text-sm text-gray-400">
          <p>
            © {new Date().getFullYear()} {config?.nombre_comercial || 'ImportStore'}. Todos los
            derechos reservados.
          </p>
        </div>
      </div>
    </footer>
  );
}

