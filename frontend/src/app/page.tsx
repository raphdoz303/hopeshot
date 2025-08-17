import StatusBanner from '../components/StatusBanner'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50 flex flex-col items-center justify-center p-8">
      {/* Main header with emoji */}
      <h1 className="text-6xl font-bold text-gray-800 mb-4 text-center">
        🌟 HopeShot
      </h1>
      
      {/* Subtitle explaining what HopeShot does */}
      <p className="text-xl text-gray-600 mb-8 text-center max-w-2xl">
        A positive news web app experiment - bringing you constructive and hopeful stories from around the world
      </p>
      
      {/* Now using our custom StatusBanner component! */}
      <div className="space-y-4">
        <StatusBanner 
          status="development" 
          message="In Development - Building something amazing step by step!" 
          emoji="🚧"
        />
        
        {/* Let's add a second banner to show the reusability! */}
        <StatusBanner 
          status="success" 
          message="Documentation system is working perfectly!" 
          emoji="✅"
        />
      </div>
    </div>
  )
}
