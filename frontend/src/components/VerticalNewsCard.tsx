// components/VerticalNewsCard.tsx
import React from 'react'

// Category configuration matching your design specs
const categoryColors = {
  science: { bg: '#E6FBFF', text: '#006D7C', accent: '#00A7C4', emoji: '🔬' },
  rights: { bg: '#FFEDEF', text: '#7A2333', accent: '#E84E5A', emoji: '✊' },
  society: { bg: '#EEF2FF', text: '#2F327A', accent: '#6366F1', emoji: '🧑‍🤝‍🧑' },
  environment: { bg: '#EAFBF1', text: '#14532D', accent: '#22C55E', emoji: '🌱' },
  health: { bg: '#E9FBFB', text: '#0B4A4E', accent: '#0EA5A4', emoji: '🩺' },
  education: { bg: '#F3F0FF', text: '#3C2E7E', accent: '#7C3AED', emoji: '📚' },
  economy: { bg: '#EEFDF4', text: '#0B552E', accent: '#12B981', emoji: '📈' },
  technology: { bg: '#EAF6FF', text: '#103A66', accent: '#3BA3FF', emoji: '🤖' },
} as const

// Impact level mapping
const impactMap = {
  Global: { emoji: '🌍', chip: '#1D6FD1' }, // sky-700
  Regional: { emoji: '🗺️', chip: '#22C55E' }, // growth-500
  National: { emoji: '🏛️', chip: '#22C55E' }, // growth-500
  Local: { emoji: '📍', chip: '#FFC53D' }, // sun-500
} as const

// Article interface matching your backend response
interface Article {
  title: string
  description?: string
  url: string
  source: { name: string }
  publishedAt: string
  gemini_analysis?: {
    categories: string[]
    geographical_impact_level: keyof typeof impactMap
    geographical_impact_location_names: string[]
  }
}

interface VerticalNewsCardProps {
  article: Article
}

export default function VerticalNewsCard({ article }: VerticalNewsCardProps) {
  // Get primary category for accent color
  const primaryCategory = article.gemini_analysis?.categories?.[0] || 'technology'
  const categoryKey = primaryCategory.toLowerCase() as keyof typeof categoryColors
  const categoryConfig = categoryColors[categoryKey] || categoryColors.technology
  
  // Format date
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  }

  return (
    <div className="bg-white rounded-2xl shadow-sm hover:shadow-lg transition-shadow duration-200 overflow-hidden">
      {/* Top accent bar */}
      <div 
        className="h-1"
        style={{ backgroundColor: categoryConfig.accent }}
      />
      
      <div className="p-4 space-y-3">
        {/* Top meta row - geography left, date right */}
        <div className="flex items-start justify-between">
          {/* Left: Geography stack */}
          <div className="space-y-1">
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
            
            {/* Geography location */}
            <div className="text-xs ml-2" style={{ color: 'var(--neutral-600)' }}>
              {article.gemini_analysis?.geographical_impact_location_names?.[0] || 'World'}
            </div>
          </div>
          
          {/* Right: Date (centered vertically) */}
          <div className="text-xs self-center" style={{ color: 'var(--neutral-600)' }}>
            {formatDate(article.publishedAt)}
          </div>
        </div>

        {/* Title */}
        <h3 className="text-lg font-semibold line-clamp-3 leading-tight" style={{ color: 'var(--neutral-900)' }}>
          {article.title}
        </h3>

        {/* Description if available */}
        {article.description && (
          <p className="text-sm line-clamp-2" style={{ color: 'var(--neutral-600)' }}>
            {article.description}
          </p>
        )}

        {/* Category emojis */}
        <div className="flex items-center gap-1">
          {article.gemini_analysis?.categories?.slice(0, 3).map((category, index) => {
            const catKey = category.toLowerCase() as keyof typeof categoryColors
            const catConfig = categoryColors[catKey] || categoryColors.technology
            return (
              <span key={index} className="text-lg" aria-label={category}>
                {catConfig.emoji}
              </span>
            )
          })}
          {(article.gemini_analysis?.categories?.length || 0) > 3 && (
            <span className="text-xs ml-1" style={{ color: 'var(--neutral-600)' }}>
              +{(article.gemini_analysis?.categories?.length || 0) - 3}
            </span>
          )}
        </div>

        {/* Footer with source and link */}
        <div className="flex items-center justify-between pt-2" style={{ borderTopColor: 'var(--neutral-100)', borderTopWidth: '1px' }}>
          <span className="text-sm" style={{ color: 'var(--neutral-600)' }}>{article.source.name}</span>
          <a 
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm font-medium flex items-center gap-1 hover:underline"
            style={{ color: 'var(--sky-700)' }}
          >
            Read more →
          </a>
        </div>
      </div>
    </div>
  )
}