// components/VerticalNewsCard.tsx
import React from 'react'
import { Category } from '../../services/api'

import { Article } from '../../services/api'  // Use shared interface instead of local one

interface VerticalNewsCardProps {
  article: Article
  categories: Category[]  // Pass categories from parent component
}

export default function VerticalNewsCard({ article, categories }: VerticalNewsCardProps) {
  // Helper function to find category data by name
  const getCategoryData = (categoryName: string) => {
    return categories.find(cat => cat.name === categoryName) || {
      name: categoryName,
      emoji: '📰', // Placeholder emoji for unknown categories
      color: '#F7F9FB',
      accent: '#475569'
    }
  }
  
  // Get primary category for accent color
  const primaryCategoryName = article.gemini_analysis?.categories?.[0] || 'unknown'
  const primaryCategory = getCategoryData(primaryCategoryName)
  
  // Format date
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  }

  // Get categories with placeholder if none exist
  const displayCategories = (article.gemini_analysis?.categories && article.gemini_analysis.categories.length > 0)
    ? article.gemini_analysis.categories 
    : ['unknown']

  return (
    <div className="bg-white rounded-2xl shadow-sm hover:shadow-lg transition-shadow duration-200 overflow-hidden flex flex-col h-full">
      {/* Top accent bar */}
      <div 
        className="h-1"
        style={{ backgroundColor: primaryCategory.accent }}
      />
      
      <div className="p-4 flex flex-col flex-grow">
        {/* Content area - grows to fill space */}
        <div className="flex-grow space-y-3">
          {/* Top meta section - geography and date */}
          <div className="flex items-start justify-between">
            {/* Left: Geography stack */}
            <div className="space-y-1">
              {/* M49 location emojis in grey background (replacing impact level) */}
              <div className="flex items-center gap-1 px-2 py-1 rounded-full text-xs"
                   style={{ backgroundColor: 'var(--neutral-50)' }}>
                {article.gemini_analysis?.geographical_impact_location_emojis?.slice(0, 3).map((emoji, index) => (
                  <span key={index} className="text-sm" title={article.gemini_analysis?.geographical_impact_location_names?.[index]}>
                    {emoji}
                  </span>
                ))}
                {(article.gemini_analysis?.geographical_impact_location_emojis?.length || 0) > 3 && (
                  <span className="text-xs ml-1" style={{ color: 'var(--neutral-600)' }}>
                    +{(article.gemini_analysis?.geographical_impact_location_emojis?.length || 0) - 3}
                  </span>
                )}
                {(!article.gemini_analysis?.geographical_impact_location_emojis || article.gemini_analysis.geographical_impact_location_emojis.length === 0) && (
                  <span className="text-sm">🌍</span>
                )}
              </div>
              
              {/* Category emojis - moved to top */}
              <div className="flex items-center gap-1 ml-2">
                {displayCategories.slice(0, 3).map((categoryName, index) => {
                  const categoryData = getCategoryData(categoryName)
                  return (
                    <span key={index} className="text-lg" aria-label={categoryData.name} title={categoryData.name}>
                      {categoryData.emoji}
                    </span>
                  )
                })}
                {displayCategories.length > 3 && (
                  <span className="text-xs ml-1" style={{ color: 'var(--neutral-600)' }}>
                    +{displayCategories.length - 3}
                  </span>
                )}
              </div>
            </div>
            
            {/* Right: Date (centered vertically to match geography section height) */}
            <div className="text-xs flex items-center h-full" style={{ color: 'var(--neutral-600)' }}>
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
        </div>
        
        {/* Footer - always at bottom, single row */}
        <div className="flex items-center justify-between pt-3 mt-auto border-t" style={{ borderTopColor: 'var(--neutral-100)' }}>
          <span className="text-sm truncate" style={{ color: 'var(--neutral-600)' }}>
            {article.source.name}
          </span>
          <a 
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm font-medium flex items-center gap-1 hover:underline flex-shrink-0 ml-2"
            style={{ color: 'var(--sky-700)' }}
          >
            Read more →
          </a>
        </div>
      </div>
    </div>
  )
}