import type { Metadata } from 'next';
import './globals.css';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ChatIA from '@/components/ChatIA';
import { Toaster } from 'react-hot-toast';
import ConfigProvider from '@/components/ConfigProvider';

export const metadata: Metadata = {
  title: 'ImportStore - E-commerce Premium',
  description: 'Tienda online premium de productos importados',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body>
        <ConfigProvider>
          <div className="min-h-screen flex flex-col">
            <Navbar />
            <main className="flex-grow">{children}</main>
            <Footer />
          </div>
          <Toaster position="top-right" />
          <ChatIA />
        </ConfigProvider>
      </body>
    </html>
  );
}

