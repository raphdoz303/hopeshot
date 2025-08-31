// app/explore/page.tsx
'use client'
import { useState, useEffect } from 'react'
import VerticalNewsCard from '../../components/VerticalNewsCard'

// Interface for category from API
interface Category {
  id: number
  name: string
  filter_name: string
  emoji: string
  description: string
  color: string
  accent: string
}

// Mock data for now - we'll connect to your API later
const mockArticles = [
  {
    title: "Revolutionary Gene Therapy Restores Vision in Blind Patients",
    description: "Scientists at Johns Hopkins have successfully restored partial vision to patients with inherited blindness using a groundbreaking gene therapy approach.",
    url: "https://example.com/gene-therapy-breakthrough",
    source: { name: "AFP" },
    publishedAt: "2025-08-29T10:30:00Z",
    gemini_analysis: {
      categories: ["health", "science tech"],
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
      categories: ["social progress", "environment"],
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
      categories: ["science tech", "environment"],
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
      categories: ["education", "science tech", "health"],
      geographical_impact_level: "Regional" as const,
      geographical_impact_location_names: ["Kenya", "Africa"]
    }
  }
]

export default function ExplorePage() {
  const [articles, setArticles] = useState(mockArticles)
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedCategories, setSelectedCategories] = useState<string[]>([])
  const [selectedImpact, setSelectedImpact] = useState<string[]>(['Global', 'Regional'])

  // Fetch categories from API
  useEffect(() => {
    console.log('Fetching categories from API...')
    const fetchCategories = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/categories')
        const data = await response.json()
        
        console.log('Categories response:', data)
        
        if (data.status === 'success') {
          setCategories(data.categories)
          console.log('Categories set:', data.categories)
        }
      } catch (error) {
        console.error('Failed to fetch categories:', error)
      }
    }

    fetchCategories()
  }, [])

  const toggleCategory = (categoryName: string) => {
    setSelectedCategories(prev => 
      prev.includes(categoryName) 
        ? prev.filter(cat => cat !== categoryName)
        : [...prev, categoryName]
    )
  }

  const toggleImpact = (impact: string) => {
    setSelectedImpact(prev => 
      prev.includes(impact) 
        ? prev.filter(imp => imp !== impact)
        : [...prev, impact]
    )
  }

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
                Categories ({categories.length} available)
              </label>
              <div className="flex flex-wrap gap-2">
                {categories.length > 0 ? categories.map((category) => {
                  const isSelected = selectedCategories.includes(category.name)
                  return (
                    <button
                      key={category.id}
                      onClick={() => toggleCategory(category.name)}
                      className="flex items-center gap-2 px-3 py-2 rounded-full border text-sm font-medium transition-colors"
                      style={{
                        borderColor: isSelected ? category.accent : 'var(--neutral-300)',
                        backgroundColor: isSelected ? category.color : 'var(--neutral-50)',
                        color: isSelected ? category.accent : 'var(--neutral-700)'
                      }}
                    >
                      <span>{category.emoji}</span>
                      <span>{category.filter_name}</span>
                    </button>
                  )
                }) : (
                  <p className="text-sm" style={{ color: 'var(--neutral-600)' }}>
                    Loading categories...
                  </p>
                )}
              </div>
            </div>

            {/* Impact level filters */}
            <div>
              <label className="text-sm font-medium mb-3 block" style={{ color: 'var(--neutral-900)' }}>
                Impact Level
              </label>
              <div className="flex gap-2">
                {['Global', 'Regional', 'Local'].map((impact) => {
                  const isSelected = selectedImpact.includes(impact)
                  return (
                    <button
                      key={impact}
                      onClick={() => toggleImpact(impact)}
                      className="flex items-center gap-2 px-3 py-2 rounded-full border text-sm font-medium transition-colors"
                      style={{
                        borderColor: isSelected ? 'var(--sky-500)' : 'var(--neutral-300)',
                        backgroundColor: isSelected ? 'var(--sky-50)' : 'var(--neutral-50)',
                        color: isSelected ? 'var(--sky-700)' : 'var(--neutral-700)'
                      }}
                    >
                      <span>{impact === 'Global' ? '🌍' : impact === 'Regional' ? '🗺️' : '📍'}</span>
                      <span>{impact}</span>
                    </button>
                  )
                })}
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
            {articles.length} results • last 7 days • 
            {selectedCategories.length > 0 
              ? ` categories: ${selectedCategories.join(', ')}` 
              : ' all categories'}
            {selectedImpact.length > 0 && selectedImpact.length < 3 
              ? ` • ${selectedImpact.join(', ').toLowerCase()} impact` 
              : ''}
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