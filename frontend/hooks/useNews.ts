// hooks/useNews.ts
// Custom hook for managing news data, loading states, and filtering

import { useState, useEffect, useCallback } from 'react'
import { apiService, Article, Category, NewsFilters, transformers } from '../services/api'

interface UseNewsResult {
  // Data
  articles: Article[]
  categories: Category[]
  filteredArticles: Article[]
  
  // Loading states
  loading: boolean
  categoriesLoading: boolean
  error: string | null
  
  // Filter states
  selectedCategories: string[]
  selectedImpacts: string[]
  searchQuery: string
  
  // Actions
  setSelectedCategories: (categories: string[]) => void
  setSelectedImpacts: (impacts: string[]) => void
  setSearchQuery: (query: string) => void
  toggleCategory: (categoryName: string) => void
  toggleImpact: (impact: string) => void
  refreshNews: () => Promise<void>
  
  // Meta info
  totalArticles: number
  isFiltered: boolean
}

export function useNews(initialPageSize: number = 20): UseNewsResult {
  // Data states
  const [articles, setArticles] = useState<Article[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(false)
  const [categoriesLoading, setCategoriesLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  // Filter states
  const [selectedCategories, setSelectedCategories] = useState<string[]>([])
  const [selectedImpacts, setSelectedImpacts] = useState<string[]>(['Global', 'Regional'])
  const [searchQuery, setSearchQuery] = useState('')

  // Fetch categories on mount
  useEffect(() => {
    const fetchCategories = async () => {
      setCategoriesLoading(true)
      try {
        const response = await apiService.getCategories()
        
        if (response.status === 'success') {
          setCategories(response.categories)
          console.log(`Loaded ${response.categories.length} categories from API`)
        } else {
          throw new Error(response.message || 'Failed to fetch categories')
        }
      } catch (err) {
        console.error('Categories fetch error:', err)
        setError(`Failed to load categories: ${err}`)
      } finally {
        setCategoriesLoading(false)
      }
    }

    fetchCategories()
  }, [])

  // Fetch news articles
  const fetchNews = useCallback(async (filters: NewsFilters = {}) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await apiService.getNews({
        pageSize: initialPageSize,
        language: 'en',
        ...filters
      })
      
      if (response.status === 'success') {
        // Normalize articles to ensure consistent data structure
        const normalizedArticles = response.articles.map(transformers.normalizeArticle)
        setArticles(normalizedArticles)
        
        console.log(`Loaded ${normalizedArticles.length} articles from API`)
        console.log('Backend metadata:', {
          gemini_analyzed: response.gemini_analyzed,
          database_inserted: response.database_inserted,
          sources_used: response.sourcesUsed
        })
      } else {
        throw new Error(response.message || 'Failed to fetch news')
      }
    } catch (err) {
      console.error('News fetch error:', err)
      setError(`Failed to load news: ${err}`)
    } finally {
      setLoading(false)
    }
  }, [initialPageSize])

  // Initial news fetch
  useEffect(() => {
    fetchNews()
  }, [fetchNews])

  // Refresh function for manual reload
  const refreshNews = useCallback(async () => {
    await fetchNews({ 
      q: searchQuery || undefined,
      pageSize: initialPageSize 
    })
  }, [fetchNews, searchQuery, initialPageSize])

  // Filter articles based on current selections
  const filteredArticles = transformers.filterArticles(
    articles, 
    selectedCategories, 
    selectedImpacts
  )

  // Sort by date (newest first)
  const sortedFilteredArticles = transformers.sortArticles(filteredArticles, 'date')

  // Toggle functions for cleaner state management
  const toggleCategory = useCallback((categoryName: string) => {
    setSelectedCategories(prev => 
      prev.includes(categoryName) 
        ? prev.filter(cat => cat !== categoryName)
        : [...prev, categoryName]
    )
  }, [])

  const toggleImpact = useCallback((impact: string) => {
    setSelectedImpacts(prev => 
      prev.includes(impact) 
        ? prev.filter(imp => imp !== impact)
        : [...prev, impact]
    )
  }, [])

  // Computed properties
  const totalArticles = articles.length
  const isFiltered = selectedCategories.length > 0 || 
                    selectedImpacts.length < 3 || 
                    searchQuery.length > 0

  return {
    // Data
    articles,
    categories,
    filteredArticles: sortedFilteredArticles,
    
    // Loading states
    loading,
    categoriesLoading,
    error,
    
    // Filter states
    selectedCategories,
    selectedImpacts,
    searchQuery,
    
    // Actions
    setSelectedCategories,
    setSelectedImpacts,
    setSearchQuery,
    toggleCategory,
    toggleImpact,
    refreshNews,
    
    // Meta info
    totalArticles,
    isFiltered
  }
}