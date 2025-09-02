// components/VerticalNewsCard.tsx
import React from 'react'
import { Category } from '../../services/api'

// Impact level mapping (this stays the same)
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
  categories: Category[]  // Pass categories from parent component
}

export default function VerticalNewsCard({ article, categories }: VerticalNewsCardProps) {
  // Helper function to find category data by name
  const getCategoryData = (categoryName: string) => {
    return categories.find(cat => cat.name === categoryName) || {
      name: categoryName,
      emoji: '📰',
      color: '#F7F9FB',
      accent: '#475569'
    }
  }
  
  // Get primary category for accent color
  const primaryCategoryName = article.gemini_analysis?.categories?.[0] || 'culture'
  const primaryCategory = getCategoryData(primaryCategoryName)
  
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
        style={{ backgroundColor: primaryCategory.accent }}
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

        {/* Category emojis - now using real category data */}
        <div className="flex items-center gap-1">
          {article.gemini_analysis?.categories?.slice(0, 3).map((categoryName, index) => {
            const categoryData = getCategoryData(categoryName)
            return (
              <span key={index} className="text-lg" aria-label={categoryData.name}>
                {categoryData.emoji}
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