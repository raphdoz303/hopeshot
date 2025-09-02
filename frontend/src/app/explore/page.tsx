// app/explore/page.tsx
'use client'
import VerticalNewsCard from '../../components/VerticalNewsCard'
import { useNews } from '../../../hooks/useNews'
import { Article, Category } from '../../../services/api'

export default function ExplorePage() {
  const {
    filteredArticles,
    categories,
    loading,
    categoriesLoading,
    error,
    selectedCategories,
    selectedImpacts,
    toggleCategory,
    toggleImpact,
    refreshNews,
    totalArticles,
    isFiltered
  } = useNews(20)

  // Loading state
  if (loading && filteredArticles.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-sky-growth">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-sky-500 mx-auto"></div>
            <p className="mt-4 text-lg" style={{ color: 'var(--neutral-600)' }}>
              Loading positive news...
            </p>
          </div>
        </div>
      </div>
    )
  }

  // Error state
  if (error && filteredArticles.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-sky-growth">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="text-center">
            <p className="text-lg font-medium" style={{ color: 'var(--neutral-900)' }}>
              Unable to load news
            </p>
            <p className="mt-2 text-sm" style={{ color: 'var(--neutral-600)' }}>
              {error}
            </p>
            <button
              onClick={refreshNews}
              className="mt-4 px-4 py-2 rounded-lg font-medium"
              style={{ 
                backgroundColor: 'var(--sky-500)',
                color: 'white'
              }}
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-sky-growth">
      {/* Header */}
      <div className="bg-white border-b" style={{ borderBottomColor: 'var(--neutral-100)' }}>
        <div className="max-w-6xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold" style={{ color: 'var(--neutral-900)' }}>
                Explore Positive News
              </h1>
              <p className="text-sm mt-1" style={{ color: 'var(--neutral-600)' }}>
                Discover constructive stories from around the world
              </p>
            </div>
            
            {/* Refresh button */}
            <button
              onClick={refreshNews}
              disabled={loading}
              className="flex items-center gap-2 px-3 py-2 rounded-lg border text-sm font-medium transition-colors"
              style={{
                borderColor: 'var(--neutral-300)',
                color: loading ? 'var(--neutral-400)' : 'var(--neutral-700)'
              }}
            >
              <span className={loading ? 'animate-spin' : ''}>↻</span>
              {loading ? 'Loading...' : 'Refresh'}
            </button>
          </div>
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
                {categoriesLoading ? (
                  <div className="flex items-center gap-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-sky-500"></div>
                    <span className="text-sm" style={{ color: 'var(--neutral-600)' }}>
                      Loading categories...
                    </span>
                  </div>
                ) : categories.length > 0 ? categories.map((category: Category) => {
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
                    No categories available
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
                  const isSelected = selectedImpacts.includes(impact)
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
            {filteredArticles.length} of {totalArticles} results • last 7 days • 
            {selectedCategories.length > 0 
              ? ` categories: ${selectedCategories.join(', ')}` 
              : ' all categories'}
            {selectedImpacts.length > 0 && selectedImpacts.length < 3 
              ? ` • ${selectedImpacts.join(', ').toLowerCase()} impact` 
              : ''}
          </p>
        </div>

        {/* No results state */}
        {filteredArticles.length === 0 && !loading && (
          <div className="text-center py-12">
            <p className="text-lg font-medium" style={{ color: 'var(--neutral-900)' }}>
              No articles match your filters
            </p>
            <p className="text-sm mt-2" style={{ color: 'var(--neutral-600)' }}>
              Try adjusting your category or impact level selections
            </p>
            <button
              onClick={() => {
                // Clear all filters
                selectedCategories.forEach((cat: string) => toggleCategory(cat))
                selectedImpacts.forEach((impact: string) => {
                  if (!['Global', 'Regional'].includes(impact)) {
                    toggleImpact(impact)
                  }
                })
              }}
              className="mt-4 px-4 py-2 rounded-lg font-medium"
              style={{ 
                backgroundColor: 'var(--sky-500)',
                color: 'white'
              }}
            >
              Clear Filters
            </button>
          </div>
        )}

        {/* Article grid - responsive 1/2/3 columns */}
        {filteredArticles.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredArticles.map((article: Article, index: number) => (
              <VerticalNewsCard 
                key={`${article.url}-${index}`} 
                article={article} 
                categories={categories}
              />
            ))}
          </div>
        )}

        {/* Loading more indicator */}
        {loading && filteredArticles.length > 0 && (
          <div className="text-center mt-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-sky-500 mx-auto"></div>
            <p className="mt-2 text-sm" style={{ color: 'var(--neutral-600)' }}>
              Refreshing articles...
            </p>
          </div>
        )}

        {/* Pagination placeholder */}
        {filteredArticles.length > 0 && !loading && (
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
        )}
      </div>
    </div>
  )
}