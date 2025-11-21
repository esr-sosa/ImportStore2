import type { Metadata } from 'next';
import { Inter, Poppins } from 'next/font/google';
import './globals.css';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import ChatIA from '@/components/ChatIA';
import { Toaster } from 'react-hot-toast';
import ConfigProvider from '@/components/ConfigProvider';

// Fuentes premium
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const poppins = Poppins({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700', '800'],
  variable: '--font-poppins',
  display: 'swap',
});

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
    <html lang="es" className={`${inter.variable} ${poppins.variable}`}>
      <body className="font-sans antialiased">
        <ConfigProvider>
          <div className="min-h-screen flex flex-col bg-gradient-to-b from-gray-50 to-white">
            <Navbar />
            <main className="flex-grow">{children}</main>
            <Footer />
          </div>
          <Toaster 
            position="top-right" 
            toastOptions={{
              style: {
                fontFamily: 'var(--font-poppins)',
                borderRadius: '12px',
                padding: '16px',
              },
            }}
          />
          <ChatIA />
        </ConfigProvider>
      </body>
    </html>
  );
}

