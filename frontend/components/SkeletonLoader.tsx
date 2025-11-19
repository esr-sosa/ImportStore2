'use client';

interface SkeletonLoaderProps {
  type?: 'product' | 'text' | 'image' | 'card';
  count?: number;
}

export default function SkeletonLoader({ type = 'product', count = 1 }: SkeletonLoaderProps) {
  if (type === 'product') {
    return (
      <>
        {[...Array(count)].map((_, i) => (
          <div key={i} className="bg-white rounded-2xl overflow-hidden shadow-sm border border-gray-100 animate-pulse">
            <div className="aspect-square bg-gray-200" />
            <div className="p-4 space-y-3">
              <div className="h-4 bg-gray-200 rounded w-3/4" />
              <div className="h-3 bg-gray-200 rounded w-1/2" />
              <div className="h-6 bg-gray-200 rounded w-1/3" />
            </div>
          </div>
        ))}
      </>
    );
  }

  if (type === 'card') {
    return (
      <div className="bg-white rounded-2xl p-6 shadow-sm animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/4 mb-4" />
        <div className="space-y-2">
          <div className="h-4 bg-gray-200 rounded" />
          <div className="h-4 bg-gray-200 rounded w-5/6" />
          <div className="h-4 bg-gray-200 rounded w-4/6" />
        </div>
      </div>
    );
  }

  if (type === 'image') {
    return <div className="aspect-square bg-gray-200 rounded-2xl animate-pulse" />;
  }

  return <div className="h-4 bg-gray-200 rounded animate-pulse" />;
}

