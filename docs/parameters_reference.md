# HopeShot Parameters Reference Guide

## Core Data Types

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

### Category Interface
```typescript
interface Category {
  id: number
  name: string           // Internal: "science tech", "health"
  filter_name: string    // Display: "Science & Tech", "Health"
  emoji: string          // "🔬", "🩺"
  description: string
  color: string          // Background: "#E6FBFF"
  accent: string         // Border/text: "#00A7C4"
}
```

### GeminiAnalysis Interface (M49 Enhanced)
```typescript
interface GeminiAnalysis {
  categories: string[]
  geographical_impact_level: 'Global' | 'Regional' | 'National' | 'Local'
  geographical_impact_m49_codes: number[]        // NEW: Direct M49 codes [840, 392]
  geographical_impact_location_names: string[]   // UPDATED: Names from database lookup
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
```

### Location Interface (M49 Standard)
```typescript
interface Location {
  id: number
  name: string              // "United States", "Asia", "World"
  m49_code: number          // UN M49 standard: 840, 142, 001
  hierarchy_level: number   // 1=global, 2=continental, 3=regional, 4=sub-regional, 5=country
  impact_level: string      // "Global", "Continental", "Regional", "National"
  parent_id?: number        // Database FK to parent location
  parent_m49_code?: number  // M49 code of parent
  iso_alpha2?: string       // "US", "VN" (countries only)
  iso_alpha3?: string       // "USA", "VNM" (countries only)
  emoji?: string            // "🇺🇸", "🌏"
  aliases: string           // JSON array: ["USA", "United States"]
}
```

## Frontend Service Layer

### ApiService Parameters
```typescript
class ApiService {
  // Generic fetch wrapper
  private async fetchWithErrorHandling<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T>

  // Category fetching
  async getCategories(): Promise<CategoriesResponse>

  // News fetching with filters
  async getNews(filters: NewsFilters = {}): Promise<NewsResponse>
}
```

### NewsFilters Interface
```typescript
interface NewsFilters {
  q?: string              // Search query
  language?: string       // Language code
  pageSize?: number       // Results per page (1-100)
  categories?: string[]   // Category names for filtering (future)
  impactLevels?: string[] // Impact levels for filtering (future)
  dateRange?: string      // Date range selection (future)
}
```

### API Response Interfaces
```typescript
interface NewsResponse {
  status: 'success' | 'error'
  query?: string
  totalSources?: number
  sourcesUsed?: string[]
  totalArticles: number
  gemini_analyzed?: boolean
  database_inserted?: number
  articles: Article[]
  message?: string
}

interface CategoriesResponse {
  status: 'success' | 'error'
  categories: Category[]
  total: number
  message?: string
}
```

## Custom Hook Parameters

### useNews Hook Interface
```typescript
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
```

### Hook Parameters
```typescript
// Hook initialization
useNews(initialPageSize: number = 20): UseNewsResult

// Filter toggle functions
toggleCategory(categoryName: string): void
toggleImpact(impact: string): void

// Data refresh
refreshNews(): Promise<void>
```

## Component Props

### VerticalNewsCard Props (Enhanced)
```typescript
interface VerticalNewsCardProps {
  article: Article        // Required article object
  categories: Category[]  // NEW: Category data for dynamic emoji/color lookup
}

// Helper function within component
const getCategoryData = (categoryName: string): Category => {
  return categories.find(cat => cat.name === categoryName) || defaultCategory
}
```

### Impact Level Mapping
```typescript
const impactMap = {
  Global: { emoji: '🌍', chip: '#1D6FD1' },
  Regional: { emoji: '🗺️', chip: '#22C55E' },
  National: { emoji: '🏛️', chip: '#22C55E' },
  Local: { emoji: '📍', chip: '#FFC53D' },
} as const
```

## Backend Integration Parameters

### Database Fields (M49 Enhanced)
```sql
-- locations table (M49 standard)
m49_code: INTEGER           -- UN M49 standard: 840, 142, 001
hierarchy_level: INTEGER    -- 1=global, 2=continental, 3=regional, 4=sub-regional, 5=country
impact_level: TEXT          -- 'Global', 'Continental', 'Regional', 'National'
parent_id: INTEGER          -- FK to parent location
parent_m49_code: INTEGER    -- M49 code of parent
iso_alpha2: TEXT           -- "US", "VN" (countries only)
iso_alpha3: TEXT           -- "USA", "VNM" (countries only)
emoji: TEXT                -- "🇺🇸", "🌏"
aliases: TEXT              -- JSON array: ["USA", "United States"]

-- article_locations junction table (M49 direct storage)
article_id: INTEGER        -- FK to articles
m49_code: INTEGER          -- Direct M49 code storage (no conversion)

-- articles table (geographic columns removed)
geographical_impact_level: TEXT  -- Only impact level, no M49 codes
```

### API Endpoint Parameters
```bash
# GET /api/news
?q=string              # Search query
?language=en           # Language code
?pageSize=20           # Results per page (1-100)
# Future parameters:
?categories=health,tech # Category filtering (not implemented)
?impactLevels=Global   # Impact filtering (not implemented)
?m49_codes=840,392     # M49 code filtering (not implemented)

# GET /api/categories
# No parameters - returns all categories with visual metadata
```

## M49 Geographic Parameters

### M49 Code Examples
```typescript
// Common M49 codes for validation
const M49_CODES = {
  // Global
  WORLD: 1,
  
  // Continents  
  AFRICA: 2,
  ANTARCTICA: 10,
  ASIA: 142,
  EUROPE: 150,
  AMERICAS: 19,
  OCEANIA: 9,
  
  // Regions
  SOUTHEAST_ASIA: 35,
  WESTERN_EUROPE: 155,
  NORTH_AMERICA: 21,
  
  // Countries
  USA: 840,
  VIETNAM: 704,
  JAPAN: 392,
  FRANCE: 250,
  INDONESIA: 360,
  CHINA: 156
} as const
```

### M49 Processing Functions
```typescript
// GeminiService M49 processing
_process_geographic_analysis(analysis: Dict): Dict
_get_location_names_by_m49(m49_codes: List[int]): List[str]

// DatabaseService M49 operations  
get_location_names_by_m49(m49_codes: List[int]): List[str]
insert_article(article: Dict, gemini_analysis: Dict): Optional[int]
```

## Common Function Parameters

### Array Callbacks (TypeScript Enhanced)
```typescript
// Map operations
articles.map((article: Article, index: number) => ...)
categories.map((category: Category, index: number) => ...)
m49_codes.map((code: number, index: number) => ...)

// Filter operations  
articles.filter((article: Article) => ...)
categories.filter((category: Category) => ...)

// ForEach operations
selectedCategories.forEach((categoryName: string) => ...)
selectedImpacts.forEach((impactLevel: string) => ...)
m49_codes.forEach((code: number) => ...)
```

### Event Handlers
```typescript
// Button clicks with specific types
onClick={() => toggleCategory(categoryName: string)}
onClick={() => toggleImpact(impactLevel: string)}
onClick={(e: React.MouseEvent<HTMLButtonElement>) => handleClick()}

// Form inputs
onChange={(e: React.ChangeEvent<HTMLInputElement>) => ...}
onSubmit={(e: React.FormEvent<HTMLFormElement>) => ...}
```

### Transformers Utility Functions
```typescript
// Data transformation utilities
transformers = {
  normalizeArticle: (article: Partial<Article>) => Article,
  filterArticles: (
    articles: Article[], 
    selectedCategories: string[], 
    selectedImpacts: string[]
  ) => Article[],
  sortArticles: (articles: Article[], sortBy: 'date' | 'hopefulness' | 'source') => Article[]
}
```

## M49 Integration Patterns

### Gemini Analysis Processing
```python
# Input from Gemini (strings)
"geographical_impact_location": ["840", "392"]

# Processing in GeminiService
m49_codes = [int(code) for code in gemini_location_array]
location_names = self._get_location_names_by_m49(m49_codes)

# Output in analysis
{
  "geographical_impact_m49_codes": [840, 392],
  "geographical_impact_location_names": ["United States", "Japan"]
}
```

### Database Storage Pattern
```python
# Article insertion
article_id = insert_article(article, analysis)

# M49 junction table population
for m49_code in analysis.get('geographical_impact_m49_codes', []):
    cursor.execute(
        "INSERT INTO article_locations (article_id, m49_code) VALUES (?, ?)",
        (article_id, m49_code)
    )
```

### Location Name Resolution
```python
# Database lookup function
def get_location_names_by_m49(self, m49_codes: List[int]) -> List[str]:
    placeholders = ','.join('?' for _ in m49_codes)
    query = f"SELECT name FROM locations WHERE m49_code IN ({placeholders})"
    cursor.execute(query, m49_codes)
    return [row[0] for row in cursor.fetchall()]
```

## TypeScript Error Prevention

### Common Parameter Fixes
```typescript
// ❌ Implicit any errors
articles.map((article, index) => ...)
categories.forEach(cat => toggleCategory(cat))
m49_codes.filter(code => code > 100)

// ✅ Explicit types
articles.map((article: Article, index: number) => ...)
categories.forEach((cat: string) => toggleCategory(cat))
m49_codes.filter((code: number) => code > 100)
```

### Import Requirements
```typescript
// Required imports for type safety
import { Article, Category, GeminiAnalysis } from '../services/api'
import { useNews } from '../hooks/useNews'
```

## Naming Conventions

### Variables
- `article` - Single Article object
- `articles` - Array of Article objects  
- `category` - Single Category object
- `categories` - Array of Category objects
- `categoryName` - String identifier for category
- `impactLevel` - String identifier for impact level
- `m49Code` - Single M49 code (number)
- `m49Codes` - Array of M49 codes (number[])
- `locationNames` - Array of location names (string[])

### Functions
- `toggleCategory(categoryName: string)` - Toggle category selection
- `toggleImpact(impactLevel: string)` - Toggle impact selection
- `getCategoryData(categoryName: string)` - Find category metadata by name
- `getLocationNamesByM49(m49Codes: number[])` - Get location names from codes
- `fetchNews(filters?: NewsFilters)` - Get articles from API
- `refreshNews()` - Reload current articles

### State Variables
- `selectedCategories: string[]` - Active category filters (category names)
- `selectedImpacts: string[]` - Active impact filters (Global, Regional, Local)
- `loading: boolean` - API request in progress
- `categoriesLoading: boolean` - Categories API request in progress
- `error: string | null` - Error message or null
- `filteredArticles: Article[]` - Articles after client-side filtering

### Database Parameters
- `article_id: INTEGER` - Primary key for articles
- `category_id: INTEGER` - Primary key for categories
- `m49_code: INTEGER` - UN M49 standard geographic code
- `location_id: INTEGER` - Primary key for locations (used internally)
- `hierarchy_level: INTEGER` - M49 hierarchy level (1-5)

## M49 Code Reference

### Standard M49 Codes
```typescript
// Global and continental codes
const GLOBAL_M49 = {
  WORLD: 1,
  AFRICA: 2,
  ANTARCTICA: 10, 
  ASIA: 142,
  EUROPE: 150,
  AMERICAS: 19,
  OCEANIA: 9
} as const

// Regional codes (examples)
const REGIONAL_M49 = {
  SOUTHEAST_ASIA: 35,
  WESTERN_EUROPE: 155,
  NORTH_AMERICA: 21,
  SOUTH_AMERICA: 5
} as const

// Country codes (examples)
const COUNTRY_M49 = {
  USA: 840,
  CANADA: 124,
  VIETNAM: 704,
  JAPAN: 392,
  FRANCE: 250,
  INDONESIA: 360,
  CHINA: 156
} as const
```

### M49 Validation Patterns
```typescript
// Validate M49 code ranges
const isValidM49 = (code: number): boolean => {
  return code > 0 && code < 1000 && Number.isInteger(code)
}

// Check if code represents country (typically 3 digits)
const isCountryCode = (code: number): boolean => {
  return code >= 100 && code <= 999
}

// Check if code represents region/continent (typically 1-2 digits)
const isRegionalCode = (code: number): boolean => {
  return code < 100
}
```

## Error Handling Parameters

### API Error Patterns
```typescript
// Service layer errors
interface ApiError {
  status: 'error'
  message: string
  code?: number
}

// M49 processing errors
interface M49Error {
  invalid_codes: number[]
  missing_locations: number[]
  lookup_failures: string[]
}
```

### Component Error States
```typescript
// Loading states
loading: boolean              // General API loading
categoriesLoading: boolean    // Categories API loading
error: string | null          // General error message

// Error handling in components
if (error && articles.length === 0) {
  // Show error state
}
```

## Database Query Parameters

### M49 Junction Table Queries
```sql
-- Insert M49 codes directly
INSERT INTO article_locations (article_id, m49_code) VALUES (?, ?)

-- Query articles by M49 codes
SELECT a.*, GROUP_CONCAT(l.name) as location_names
FROM articles a
JOIN article_locations al ON a.id = al.article_id
JOIN locations l ON al.m49_code = l.m49_code
WHERE al.m49_code IN (840, 392)  -- USA, Japan
GROUP BY a.id

-- Hierarchical filtering (find all children of Asia)
WITH RECURSIVE asia_hierarchy AS (
  SELECT id, m49_code FROM locations WHERE m49_code = 142  -- Asia
  UNION ALL
  SELECT l.id, l.m49_code
  FROM locations l
  JOIN asia_hierarchy ah ON l.parent_id = ah.id
)
SELECT DISTINCT a.*
FROM articles a
JOIN article_locations al ON a.id = al.article_id
JOIN asia_hierarchy ah ON al.m49_code = ah.m49_code
```

### Category Junction Table Queries
```sql
-- Insert category relationships
INSERT INTO article_categories (article_id, category_id) VALUES (?, ?)

-- Query articles by categories
SELECT a.*, GROUP_CONCAT(c.name) as categories
FROM articles a
JOIN article_categories ac ON a.id = ac.article_id
JOIN categories c ON ac.category_id = c.id
WHERE c.name IN ('health', 'science tech')
GROUP BY a.id
```

## Validation Parameters

### TypeScript Type Guards
```typescript
// Article validation
const isValidArticle = (obj: any): obj is Article => {
  return obj && typeof obj.title === 'string' && typeof obj.url === 'string'
}

// Category validation
const isValidCategory = (obj: any): obj is Category => {
  return obj && typeof obj.name === 'string' && typeof obj.filter_name === 'string'
}

// M49 code validation
const isValidM49Code = (code: any): code is number => {
  return typeof code === 'number' && code > 0 && code < 1000
}
```

### Data Normalization Parameters
```typescript
// Article normalization with defaults
const normalizeArticle = (article: Partial<Article>): Article => ({
  title: article.title || 'Untitled Article',
  description: article.description || '',
  url: article.url || '#',
  source: article.source || { name: 'Unknown Source' },
  publishedAt: article.publishedAt || new Date().toISOString(),
  api_source: article.api_source || 'unknown',
  // ... other fields with defaults
})
```

## Development Parameters

### File Path Conventions
```typescript
// Frontend import paths (from frontend/src/app/explore/page.tsx)
import { useNews } from '../../../hooks/useNews'           // Up 3 levels to hooks
import { Article } from '../../../services/api'           // Up 3 levels to services
import VerticalNewsCard from '../../components/VerticalNewsCard' // Up 2 levels to components
```

### Environment Variables
```bash
# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_SHEETS_ID=your_spreadsheet_id
NEWS_API_KEY=your_newsapi_key
```

This reference ensures consistent parameter usage and prevents TypeScript 'any' errors throughout the HopeShot codebase, especially with the new M49 integration and frontend-backend connection architecture.