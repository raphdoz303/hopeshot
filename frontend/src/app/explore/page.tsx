// app/explore/page.tsx
'use client'
import { useState, useEffect } from 'react'
import VerticalNewsCard from '../../components/VerticalNewsCard'

// Mock data for now - we'll connect to your API later
const mockArticles = [
  {
    title: "Revolutionary Gene Therapy Restores Vision in Blind Patients",
    description: "Scientists at Johns Hopkins have successfully restored partial vision to patients with inherited blindness using a groundbreaking gene therapy approach.",
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
    description: "Local volunteers in Detroit have created 50 new community gardens this year, providing fresh produce to food-insecure neighborhoods.",
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
    description: "Researchers have developed solar panels that convert 47% of sunlight into electricity, nearly doubling current rates.",
    url: "https://example.com/solar-breakthrough",
    source: { name: "NewsData" },
    publishedAt: "2025-08-27T09:15:00Z",
    gemini_analysis: {
      categories: ["technology", "environment", "science"],
      geographical_impact_level: "Global" as const,
      geographical_impact_location_names: ["Germany", "Europe"]
    }
  },
  {
    title: "Students Develop Low-Cost Water Purification System",
    description: "University students in Kenya have created an affordable water purification device that could help rural communities access clean drinking water.",
    url: "https://example.com/water-purification",
    source: { name: "AFP" },
    publishedAt: "2025-08-26T14:20:00Z",
    gemini_analysis: {
      categories: ["education", "technology", "health"],
      geographical_impact_level: "Regional" as const,
      geographical_impact_location_names: ["Kenya", "Africa"]
    }
  }
]

export default function ExplorePage() {
  const [articles, setArticles] = useState(mockArticles)
  const [loading, setLoading] = useState(false)

  return (
    <div className="min-h-screen bg-gradient-sky-growth">
      {/* Header */}
      <div className="bg-white border-b" style={{ borderBottomColor: 'var(--neutral-100)' }}>
        <div className="max-w-6xl mx-auto px-6 py-6">
          <h1 className="text-2xl font-bold" style={{ color: 'var(--neutral-900)' }}>
            🗞️ Explore Positive News
          </h1>
          <p className="text-sm mt-1" style={{ color: 'var(--neutral-600)' }}>
            Discover constructive stories from around the world
          </p>
        </div>
      </div>

      {/* Main content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Filters section */}
        <div className="bg-white rounded-2xl p-6 mb-8 border" style={{ borderColor: 'var(--neutral-100)' }}>
          <div className="space-y-4">
            {/* Category filters */}
            <div>
              <label className="text-sm font-medium mb-3 block" style={{ color: 'var(--neutral-900)' }}>
                Categories
              </label>
              <div className="flex flex-wrap gap-2">
                {['science', 'health', 'technology', 'environment', 'society', 'education'].map((category) => (
                  <button
                    key={category}
                    className="flex items-center gap-2 px-3 py-2 rounded-full border text-sm font-medium transition-colors"
                    style={{
                      borderColor: 'var(--neutral-300)',
                      backgroundColor: 'var(--neutral-50)',
                      color: 'var(--neutral-700)'
                    }}
                  >
                    <span>🔬</span> {/* We'll make this dynamic */}
                    <span className="capitalize">{category}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Impact level filters */}
            <div>
              <label className="text-sm font-medium mb-3 block" style={{ color: 'var(--neutral-900)' }}>
                Impact Level
              </label>
              <div className="flex gap-2">
                {['Global', 'Regional', 'Local'].map((impact) => (
                  <button
                    key={impact}
                    className="flex items-center gap-2 px-3 py-2 rounded-full border text-sm font-medium"
                    style={{
                      borderColor: 'var(--sky-300)',
                      backgroundColor: 'var(--sky-50)',
                      color: 'var(--sky-700)'
                    }}
                  >
                    <span>{impact === 'Global' ? '🌍' : impact === 'Regional' ? '🗺️' : '📍'}</span>
                    <span>{impact}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Date range */}
            <div>
              <label className="text-sm font-medium mb-3 block" style={{ color: 'var(--neutral-900)' }}>
                Time Range
              </label>
              <div className="flex gap-2">
                {['Last 7 days', 'Last 30 days', 'Custom'].map((range) => (
                  <button
                    key={range}
                    className="px-3 py-2 rounded-full border text-sm font-medium"
                    style={{
                      borderColor: range === 'Last 7 days' ? 'var(--growth-500)' : 'var(--neutral-300)',
                      backgroundColor: range === 'Last 7 days' ? 'var(--growth-50)' : 'var(--neutral-50)',
                      color: range === 'Last 7 days' ? 'var(--growth-700)' : 'var(--neutral-700)'
                    }}
                  >
                    {range}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Results meta */}
        <div className="mb-6">
          <p className="text-sm" style={{ color: 'var(--neutral-600)' }}>
            {articles.length} results • last 7 days • all categories
          </p>
        </div>

        {/* Article grid - responsive 1/2/3 columns */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {articles.map((article, index) => (
            <VerticalNewsCard key={index} article={article} />
          ))}
        </div>

        {/* Pagination placeholder */}
        <div className="flex justify-center mt-12">
          <div className="flex gap-2">
            <button 
              className="px-4 py-2 rounded-lg border text-sm font-medium"
              style={{ 
                borderColor: 'var(--neutral-300)',
                color: 'var(--neutral-600)' 
              }}
            >
              ← Previous
            </button>
            <button 
              className="px-4 py-2 rounded-lg text-sm font-medium"
              style={{ 
                backgroundColor: 'var(--sky-500)',
                color: 'white'
              }}
            >
              Next →
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}