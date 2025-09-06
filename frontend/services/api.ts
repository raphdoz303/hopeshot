// services/api.ts
// Centralized API service for all backend communication

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// TypeScript interfaces matching backend responses
export interface Category {
  id: number
  name: string
  filter_name: string
  emoji: string
  description: string
  color: string
  accent: string
}

export interface GeminiAnalysis {
  categories: string[]
  geographical_impact_level: 'Global' | 'Regional' | 'National' | 'Local'
  geographical_impact_location_names: string[]
  geographical_impact_location_emojis: string[]  // ADD THIS LINE
  sentiment: string
  confidence_score: number
  emotions: {
    hope: number
    awe: number
    gratitude: number
    compassion: number
    relief: number
    joy: number
  }
  source_credibility: string
  overall_hopefulness: number
}

export interface Article {
  title: string
  description?: string
  url: string
  urlToImage?: string
  source: { 
    id?: string
    name: string 
  }
  author?: string
  publishedAt: string
  content?: string
  api_source: string
  gemini_analysis?: GeminiAnalysis
}

export interface NewsResponse {
  status: 'success' | 'error'
  query?: string
  totalSources?: number
  sourcesUsed?: string[]
  sourcesFailed?: string[]
  totalArticles: number
  crossSourceDuplicatesRemoved?: number
  gemini_analyzed?: boolean
  prompt_versions?: string[]
  database_inserted?: number
  sheets_logged?: boolean
  articles: Article[]
  message?: string
}

// NEW: Interface for database articles response
export interface ArticlesResponse {
  status: 'success' | 'error'
  source: string
  totalArticles: number
  articles: Article[]
  database_stats: {
    total_in_db: number
    categories_count: number
    locations_count: number
    recent_24h: number
  }
  filters_applied: {
    category?: string
    impact_level?: string
    limit: number
  }
  message?: string
}

export interface CategoriesResponse {
  status: 'success' | 'error'
  categories: Category[]
  total: number
  message?: string
}

// Filter parameters for news API
export interface NewsFilters {
  q?: string
  language?: string
  pageSize?: number
  categories?: string[]
  impactLevels?: string[]
  dateRange?: string
}

// NEW: Filter parameters for database articles
export interface ArticleFilters {
  limit?: number
  category?: string
  impact_level?: string
}

class ApiService {
  private baseURL: string

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
  }

  // Generic fetch wrapper with error handling
  private async fetchWithErrorHandling<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    try {
      const url = `${this.baseURL}${endpoint}`
      console.log(`🌐 API Call: ${url}`)
      
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      console.log(`✅ API Success:`, data)
      return data
    } catch (error) {
      console.error(`❌ API Error for ${endpoint}:`, error)
      throw error
    }
  }

  // Fetch all categories for filtering UI
  async getCategories(): Promise<CategoriesResponse> {
    return this.fetchWithErrorHandling<CategoriesResponse>('/api/categories')
  }

  // Fetch news articles with optional filtering (fresh API calls)
  async getNews(filters: NewsFilters = {}): Promise<NewsResponse> {
    const params = new URLSearchParams()
    
    // Add basic filters
    if (filters.q) params.append('q', filters.q)
    if (filters.language) params.append('language', filters.language)
    if (filters.pageSize) params.append('pageSize', filters.pageSize.toString())
    
    const queryString = params.toString()
    const endpoint = `/api/news${queryString ? `?${queryString}` : ''}`
    
    return this.fetchWithErrorHandling<NewsResponse>(endpoint)
  }

  // NEW: Fetch articles from database (accumulated articles)
  async getArticles(filters: ArticleFilters = {}): Promise<ArticlesResponse> {
    const params = new URLSearchParams()
    
    if (filters.limit) params.append('limit', filters.limit.toString())
    if (filters.category) params.append('category', filters.category)
    if (filters.impact_level) params.append('impact_level', filters.impact_level)
    
    const queryString = params.toString()
    const endpoint = `/api/articles${queryString ? `?${queryString}` : ''}`
    
    return this.fetchWithErrorHandling<ArticlesResponse>(endpoint)
  }

  // Test backend connection
  async testConnection(): Promise<{ status: string; message: string }> {
    return this.fetchWithErrorHandling('/api/test')
  }

  // Get system health info
  async getHealth(): Promise<any> {
    return this.fetchWithErrorHandling('/health')
  }
}

// Create singleton instance
export const apiService = new ApiService()

// Utility functions for data transformation
export const transformers = {
  // Ensure article has required fields with defaults
  normalizeArticle: (article: Partial<Article>): Article => ({
    title: article.title || 'Untitled Article',
    description: article.description || '',
    url: article.url || '#',
    urlToImage: article.urlToImage,
    source: article.source || { name: 'Unknown Source' },
    author: article.author,
    publishedAt: article.publishedAt || new Date().toISOString(),
    content: article.content,
    api_source: article.api_source || 'unknown',
    gemini_analysis: article.gemini_analysis
  }),

  // Filter articles based on user selections
  filterArticles: (
    articles: Article[], 
    selectedCategories: string[], 
    selectedImpacts: string[]
  ): Article[] => {
    return articles.filter(article => {
      // Category filtering
      const categoryMatch = selectedCategories.length === 0 || 
        article.gemini_analysis?.categories?.some(cat => 
          selectedCategories.includes(cat)
        )

      // Impact level filtering  
      const impactMatch = selectedImpacts.length === 0 ||
        (article.gemini_analysis?.geographical_impact_level && 
         selectedImpacts.includes(article.gemini_analysis.geographical_impact_level))

      return categoryMatch && impactMatch
    })
  },

  // Sort articles by various criteria
  sortArticles: (articles: Article[], sortBy: 'date' | 'hopefulness' | 'source') => {
    return [...articles].sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime()
        case 'hopefulness':
          const hopeA = a.gemini_analysis?.overall_hopefulness || 0
          const hopeB = b.gemini_analysis?.overall_hopefulness || 0
          return hopeB - hopeA
        case 'source':
          return a.source.name.localeCompare(b.source.name)
        default:
          return 0
      }
    })
  }
}

export default apiService