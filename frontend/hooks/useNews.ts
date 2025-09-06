// hooks/useNews.ts
// Custom hook for managing news data, loading states, and filtering

import { useState, useEffect, useCallback } from 'react'
import { apiService, Article, Category, NewsFilters, ArticleFilters, transformers } from '../services/api'

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
  geographicSearch: string
  
  // Actions
  setSelectedCategories: (categories: string[]) => void
  setSelectedImpacts: (impacts: string[]) => void
  setSearchQuery: (query: string) => void
  setGeographicSearch: (search: string) => void
  toggleCategory: (categoryName: string) => void
  toggleImpact: (impact: string) => void
  refreshNews: () => Promise<void>
  fetchFreshNews: () => Promise<void>
  
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
  const [geographicSearch, setGeographicSearch] = useState('')

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

  // Fetch articles from database (primary method)
  const fetchNews = useCallback(async () => {
    setLoading(true)
    setError(null)
    
    try {
      // Get accumulated articles from database
      const response = await apiService.getArticles({
        limit: 50  // Get more since database is fast
      })
      
      if (response.status === 'success') {
        // Normalize articles to ensure consistent data structure
        const normalizedArticles = response.articles.map(transformers.normalizeArticle)
        setArticles(normalizedArticles)
        
        console.log(`📚 Loaded ${normalizedArticles.length} articles from database`)
        console.log(`📊 Database contains ${response.database_stats.total_in_db} total articles`)
      } else {
        throw new Error(response.message || 'Failed to fetch articles from database')
      }
    } catch (err) {
      console.error('Database articles fetch error:', err)
      setError(`Failed to load articles from database: ${err}`)
    } finally {
      setLoading(false)
    }
  }, [])

  // Fetch fresh news from APIs (secondary method for getting new content)
  const fetchFreshNews = useCallback(async () => {
    setLoading(true)
    setError(null)
    
    try {
      // Get fresh articles from news APIs (triggers analysis and storage)
      const response = await apiService.getNews({
        pageSize: 20
      })
      
      if (response.status === 'success') {
        console.log(`🔄 Fetched ${response.articles.length} fresh articles`)
        console.log(`💾 Added ${response.database_inserted || 0} new articles to database`)
        
        // After fetching fresh, reload from database to show all accumulated articles
        await fetchNews()
      } else {
        throw new Error(response.message || 'Failed to fetch fresh news')
      }
    } catch (err) {
      console.error('Fresh news fetch error:', err)
      setError(`Error fetching fresh news: ${err}`)
    }
  }, [fetchNews])

  // Initial news fetch from database
  useEffect(() => {
    fetchNews()
  }, [fetchNews])

  // Enhanced filter logic with geographic search
  const filteredArticles = articles.filter(article => {
    // Category filtering
    const categoryMatch = selectedCategories.length === 0 || 
      article.gemini_analysis?.categories?.some(cat => 
        selectedCategories.includes(cat)
      )

    // Impact level filtering  
    const impactMatch = selectedImpacts.length === 0 ||
      (article.gemini_analysis?.geographical_impact_level && 
       selectedImpacts.includes(article.gemini_analysis.geographical_impact_level))

    // Geographic search filtering
    const geographicMatch = !geographicSearch || 
      article.gemini_analysis?.geographical_impact_location_names?.some(location =>
        location.toLowerCase().includes(geographicSearch.toLowerCase())
      )

    return categoryMatch && impactMatch && geographicMatch
  })

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
                    selectedImpacts.length < 4 || 
                    searchQuery.length > 0 ||
                    geographicSearch.length > 0

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
    geographicSearch,
    
    // Actions
    setSelectedCategories,
    setSelectedImpacts,
    setSearchQuery,
    setGeographicSearch,
    toggleCategory,
    toggleImpact,
    refreshNews: fetchNews,
    fetchFreshNews,
    
    // Meta info
    totalArticles,
    isFiltered
  }
}