// app/test-cards/page.tsx
import VerticalNewsCard from '../../components/VerticalNewsCard'

// Mock data matching your backend API structure
const mockArticles = [
  {
    title: "Revolutionary Gene Therapy Restores Vision in Blind Patients",
    description: "Scientists at Johns Hopkins have successfully restored partial vision to patients with inherited blindness using a groundbreaking gene therapy approach that could help millions worldwide.",
    url: "https://example.com/gene-therapy-breakthrough",
    source: { name: "AFP" },
    publishedAt: "2025-08-29T10:30:00Z",
    gemini_analysis: {
      categories: ["health", "science", "technology"],
      geographical_impact_level: "Global" as const,
      geographical_impact_location_names: ["USA", "World"]
    }
  },
  {
    title: "Community Garden Initiative Transforms Urban Food Access",
    description: "Local volunteers in Detroit have created 50 new community gardens this year, providing fresh produce to food-insecure neighborhoods while building stronger communities.",
    url: "https://example.com/community-gardens",
    source: { name: "NewsAPI" },
    publishedAt: "2025-08-28T15:45:00Z",
    gemini_analysis: {
      categories: ["society", "environment"],
      geographical_impact_level: "Local" as const,
      geographical_impact_location_names: ["Detroit", "USA"]
    }
  },
  {
    title: "New Solar Panel Technology Achieves Record Efficiency",
    description: "Researchers have developed solar panels that convert 47% of sunlight into electricity, nearly doubling current commercial efficiency rates.",
    url: "https://example.com/solar-breakthrough",
    source: { name: "NewsData" },
    publishedAt: "2025-08-27T09:15:00Z",
    gemini_analysis: {
      categories: ["technology", "environment", "science"],
      geographical_impact_level: "Global" as const,
      geographical_impact_location_names: ["Germany", "Europe"]
    }
  }
]

export default function CardTestPage() {
  return (
    <div className="min-h-screen bg-gradient-sky-growth p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">
          🧪 Article Card Testing
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mockArticles.map((article, index) => (
            <VerticalNewsCard key={index} article={article} />
          ))}
        </div>
      </div>
    </div>
  )
}