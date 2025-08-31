// app/page.tsx
'use client'
import { useState, useEffect } from 'react'
import Link from 'next/link'

// Mock data for top articles - we'll connect to real API later
const mockTopArticles = [
  {
    title: "Revolutionary Gene Therapy Restores Vision in Blind Patients",
    description: "Scientists at Johns Hopkins have successfully restored partial vision to patients with inherited blindness using a groundbreaking gene therapy approach that could help millions worldwide.",
    url: "https://example.com/gene-therapy-breakthrough",
    source: { name: "AFP" },
    publishedAt: "2025-08-29T10:30:00Z",
    gemini_analysis: {
      categories: ["health", "science tech"],
      geographical_impact_level: "Global" as const,
      geographical_impact_location_names: ["USA", "World"],
      overall_hopefulness: 0.9
    }
  },
  {
    title: "Community Gardens Transform Food Access in 50 Cities",
    description: "A grassroots movement has created over 500 new community gardens this year, providing fresh produce to food-insecure neighborhoods while building stronger, more connected communities.",
    url: "https://example.com/community-gardens",
    source: { name: "NewsAPI" },
    publishedAt: "2025-08-28T15:45:00Z",
    gemini_analysis: {
      categories: ["social progress", "environment"],
      geographical_impact_level: "Regional" as const,
      geographical_impact_location_names: ["USA"],
      overall_hopefulness: 0.8
    }
  },
  {
    title: "Students Develop Clean Water Solution for Rural Communities",
    description: "University students in Kenya have created an affordable water purification device that could help rural communities access clean drinking water, with plans to scale across Africa.",
    url: "https://example.com/water-purification",
    source: { name: "AFP" },
    publishedAt: "2025-08-27T14:20:00Z",
    gemini_analysis: {
      categories: ["education", "science tech", "human kindness"],
      geographical_impact_level: "Regional" as const,
      geographical_impact_location_names: ["Kenya", "Africa"],
      overall_hopefulness: 0.85
    }
  }
]

// Category colors (same as VerticalNewsCard)
const categoryColors = {
  "science tech": { bg: '#E6FBFF', text: '#006D7C', accent: '#00A7C4', emoji: '🔬' },
  "health": { bg: '#E9FBFB', text: '#0B4A4E', accent: '#0EA5A4', emoji: '🩺' },
  "environment": { bg: '#EAFBF1', text: '#14532D', accent: '#22C55E', emoji: '🌱' },
  "social progress": { bg: '#FFEDEF', text: '#7A2333', accent: '#E84E5A', emoji: '✊' },
  "education": { bg: '#F3F0FF', text: '#3C2E7E', accent: '#7C3AED', emoji: '📚' },
  "human kindness": { bg: '#EEF2FF', text: '#2F327A', accent: '#6366F1', emoji: '🤝' },
  "diplomacy": { bg: '#EEFDF4', text: '#0B552E', accent: '#12B981', emoji: '🕊️' },
  "culture": { bg: '#EAF6FF', text: '#103A66', accent: '#3BA3FF', emoji: '🎨' },
} as const

// Impact mapping
const impactMap = {
  Global: { emoji: '🌍', chip: '#1D6FD1' },
  Regional: { emoji: '🗺️', chip: '#22C55E' },
  National: { emoji: '🏛️', chip: '#22C55E' },
  Local: { emoji: '📍', chip: '#FFC53D' },
} as const

interface HorizontalHighlightCardProps {
  article: any
  rank: number
}

function HorizontalHighlightCard({ article, rank }: HorizontalHighlightCardProps) {
  const primaryCategory = article.gemini_analysis?.categories?.[0] || 'science tech'
  const categoryKey = primaryCategory as keyof typeof categoryColors
  const categoryConfig = categoryColors[categoryKey] || categoryColors["science tech"]
  
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric'
    })
  }

  return (
    <div className="bg-white rounded-2xl overflow-hidden border transition-all duration-200 hover:shadow-lg"
         style={{ borderColor: 'var(--neutral-100)' }}>
      {/* Top accent bar */}
      <div className="h-1" style={{ backgroundColor: categoryConfig.accent }} />
      
      <div className="flex h-48">
        {/* Left: Category illustration area */}
        <div className="w-32 flex items-center justify-center" 
             style={{ backgroundColor: categoryConfig.bg }}>
          <div className="w-20 h-20 rounded-full flex items-center justify-center"
               style={{ backgroundColor: categoryConfig.accent + '20' }}>
            <span className="text-3xl">{categoryConfig.emoji}</span>
          </div>
        </div>
        
        {/* Right: Content */}
        <div className="flex-1 p-6 flex flex-col justify-between">
          {/* Top section */}
          <div>
            {/* Meta row */}
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                {/* Rank badge */}
                <div className="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold"
                     style={{ backgroundColor: 'var(--sky-500)', color: 'white' }}>
                  {rank}
                </div>
                
                {/* Impact chip */}
                <div className="flex items-center gap-1 px-2 py-1 rounded-full border-l-2 text-xs"
                     style={{ 
                       backgroundColor: 'var(--neutral-50)',
                       borderLeftColor: impactMap[article.gemini_analysis?.geographical_impact_level || 'Global'].chip 
                     }}>
                  <span>{impactMap[article.gemini_analysis?.geographical_impact_level || 'Global'].emoji}</span>
                  <span style={{ color: 'var(--neutral-600)' }}>
                    {article.gemini_analysis?.geographical_impact_level || 'Global'}
                  </span>
                </div>
                
                {/* Location */}
                <span className="text-xs" style={{ color: 'var(--neutral-600)' }}>
                  {article.gemini_analysis?.geographical_impact_location_names?.[0] || 'World'}
                </span>
              </div>
              
              {/* Date */}
              <span className="text-xs" style={{ color: 'var(--neutral-600)' }}>
                {formatDate(article.publishedAt)}
              </span>
            </div>

            {/* Title */}
            <h2 className="text-xl font-bold mb-3 line-clamp-2 leading-tight"
                style={{ color: 'var(--neutral-900)' }}>
              {article.title}
            </h2>

            {/* Description */}
            <p className="text-sm line-clamp-2 mb-4" style={{ color: 'var(--neutral-600)' }}>
              {article.description}
            </p>
          </div>

          {/* Bottom section */}
          <div className="flex items-center justify-between">
            {/* Category emojis */}
            <div className="flex items-center gap-1">
              {article.gemini_analysis?.categories?.slice(0, 3).map((category: string, index: number) => {
                const catKey = category as keyof typeof categoryColors
                const catConfig = categoryColors[catKey] || categoryColors["science tech"]
                return (
                  <span key={index} className="text-lg" title={category}>
                    {catConfig.emoji}
                  </span>
                )
              })}
            </div>

            {/* Source and link */}
            <div className="flex items-center gap-3">
              <span className="text-sm" style={{ color: 'var(--neutral-600)' }}>
                {article.source.name}
              </span>
              <a 
                href={article.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm font-medium hover:underline"
                style={{ color: 'var(--sky-700)' }}
              >
                Read more →
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default function HomePage() {
  const [topArticles, setTopArticles] = useState(mockTopArticles)

  return (
    <div className="min-h-screen bg-gradient-sky-growth">
      {/* Hero Section */}
      <div className="text-center py-16 px-6">
        <h1 className="text-5xl font-bold mb-4" style={{ color: 'var(--neutral-900)' }}>
          🌟 HopeShot
        </h1>
        <p className="text-xl mb-8 max-w-2xl mx-auto" style={{ color: 'var(--neutral-600)' }}>
          Discover positive news and constructive stories that inspire hope and highlight human progress
        </p>
        
        <Link 
          href="/explore"
          className="inline-block px-6 py-3 rounded-full font-medium text-white transition-colors hover:opacity-90"
          style={{ backgroundColor: 'var(--sky-500)' }}
        >
          Explore All Stories →
        </Link>
      </div>

      {/* Best of Last 7 Days */}
      <div className="max-w-4xl mx-auto px-6 pb-16">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2" style={{ color: 'var(--neutral-900)' }}>
            Best of Last 7 Days
          </h2>
          <p className="text-lg" style={{ color: 'var(--neutral-600)' }}>
            Top positive stories that brought hope to the world this week
          </p>
        </div>

        {/* Article cards */}
        <div className="space-y-6">
          {topArticles.map((article, index) => (
            <HorizontalHighlightCard 
              key={index} 
              article={article} 
              rank={index + 1}
            />
          ))}
        </div>
      </div>
    </div>
  )
}