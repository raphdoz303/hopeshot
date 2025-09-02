# HopeShot Parameters Reference

> **Purpose**: TypeScript interfaces, function signatures, and data types for errorless coding

## Core TypeScript Interfaces

### Article Interface
```typescript
interface Article {
  title: string
  description?: string
  url: string
  urlToImage?: string
  source: { id?: string; name: string }
  author?: string
  publishedAt: string
  content?: string
  api_source: string
  gemini_analysis?: GeminiAnalysis
}
```

### GeminiAnalysis Interface (Current)
```typescript
interface GeminiAnalysis {
  categories: string[]
  geographical_impact_level: 'Global' | 'Regional' | 'National' | 'Local'
  geographical_impact_m49_codes: number[]
  geographical_impact_location_names: string[]
  geographical_impact_location_emojis: string[]
  sentiment: string
  confidence_score: number
  emotions: {
    hope: number; awe: number; gratitude: number;
    compassion: number; relief: number; joy: number
  }
  source_credibility: string
  overall_hopefulness: number
}
```

### Category Interface
```typescript
interface Category {
  id: number
  name: string           // "science tech", "health"
  filter_name: string    // "Science & Tech", "Health"
  emoji: string          // "🔬", "🩺"
  description: string
  color: string          // "#E6FBFF"
  accent: string         // "#00A7C4"
}
```

### Location Interface (M49)
```typescript
interface Location {
  id: number
  name: string              // "United States", "Asia"
  m49_code: number          // 840, 142
  hierarchy_level: number   // 1-5 (global to country)
  parent_id?: number
  parent_m49_code?: number
  emoji?: string            // "🇺🇸", "🌍"
  iso_alpha2?: string       // "US", "VN"
  iso_alpha3?: string       // "USA", "VNM"
}
```

## Frontend Service Layer

### ApiService Class
```typescript
class ApiService {
  private async fetchWithErrorHandling<T>(endpoint: string): Promise<T>
  async getCategories(): Promise<CategoriesResponse>
  async getNews(filters?: NewsFilters): Promise<NewsResponse>
}
```

### useNews Hook Interface
```typescript
interface UseNewsResult {
  // Data
  articles: Article[]
  categories: Category[]
  filteredArticles: Article[]
  
  // States
  loading: boolean
  error: string | null
  selectedCategories: string[]
  selectedImpacts: string[]
  geographicSearch: string
  
  // Actions
  toggleCategory: (categoryName: string) => void
  toggleImpact: (impact: string) => void
  setGeographicSearch: (search: string) => void
  refreshNews: () => Promise<void>
}
```

### NewsFilters Interface
```typescript
interface NewsFilters {
  q?: string
  language?: string
  pageSize?: number
}
```

## Component Props

### VerticalNewsCard Props
```typescript
interface VerticalNewsCardProps {
  article: Article
  categories: Category[]  // Required for dynamic color lookup
}

// Helper function
const getCategoryData = (categoryName: string): Category => {
  return categories.find(cat => cat.name === categoryName) || defaultCategory
}
```

## Common M49 Codes
```typescript
const M49_EXAMPLES = {
  USA: 840, CANADA: 124, VIETNAM: 704, JAPAN: 392,
  ASIA: 142, EUROPE: 150, WORLD: 1
} as const
```

## Database Function Signatures

### DatabaseService Key Methods
```python
def get_location_names_and_emojis_by_m49(m49_codes: List[int]) -> tuple[List[str], List[str]]
def insert_article(article: Dict, gemini_analysis: Dict) -> Optional[int]
def get_all_categories() -> List[Dict[str, Any]]
```

### GeminiService Key Methods
```python
async def analyze_articles_batch(articles: List[Dict]) -> List[Dict]
def _process_geographic_analysis(analysis: Dict) -> Dict
```

## Event Handler Patterns
```typescript
// Button clicks with explicit types
onClick={() => toggleCategory(categoryName: string)}
onClick={(e: React.MouseEvent<HTMLButtonElement>) => handleClick()}

// Form inputs
onChange={(e: React.ChangeEvent<HTMLInputElement>) => setGeographicSearch(e.target.value)}
```

## Error Prevention Patterns

### TypeScript Explicit Types
```typescript
// ❌ Implicit any errors
articles.map((article, index) => ...)
categories.forEach(cat => ...)

// ✅ Explicit types
articles.map((article: Article, index: number) => ...)
categories.forEach((categoryName: string) => ...)
```

### Import Requirements
```typescript
// Required imports for type safety
import { Article, Category, GeminiAnalysis } from '../services/api'
import { useNews } from '../hooks/useNews'
```

---
*Parameters version: 0.12.0*