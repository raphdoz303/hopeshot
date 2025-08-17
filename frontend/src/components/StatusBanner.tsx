// src/components/StatusBanner.tsx
// A reusable status banner component - like a template for showing messages

interface StatusBannerProps {
  status: 'development' | 'success' | 'warning' | 'error'
  message: string
  emoji?: string  // Optional emoji (the ? makes it optional)
}

export default function StatusBanner({ status, message, emoji = '📋' }: StatusBannerProps) {
  // Define different colors for different status types (like different drum kits)
  const statusStyles = {
    development: 'bg-yellow-100 border-yellow-400 text-yellow-800',
    success: 'bg-green-100 border-green-400 text-green-800', 
    warning: 'bg-orange-100 border-orange-400 text-orange-800',
    error: 'bg-red-100 border-red-400 text-red-800'
  }

  return (
    <div className={`border rounded-lg px-6 py-3 text-center ${statusStyles[status]}`}>
      <p className="font-medium">
        {emoji} {message}
      </p>
    </div>
  )
}