// Test page to verify frontend-backend communication
// This component provides a visual interface to test all our API endpoints

'use client'  // This makes it a client component (can use hooks and events)

import { useState } from 'react'
import StatusBanner from '../../components/StatusBanner'

export default function TestPage() {
  // State variables to manage component data
  const [apiResponse, setApiResponse] = useState<string>('')  // Stores API response JSON
  const [isLoading, setIsLoading] = useState(false)           // Loading state for buttons
  const [error, setError] = useState('')                     // Error messages

  // Helper function to reset states before making API calls
  const resetStates = () => {
    setIsLoading(true)
    setApiResponse('')
    setError('')
  }

  // Test function for /api/test endpoint
  // This verifies our test endpoint with sample data
  const testApiEndpoint = async () => {
    resetStates()
    
    try {
      const response = await fetch('http://localhost:8000/api/test')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setApiResponse(JSON.stringify(data, null, 2))
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  // Test function for /api/sources/test endpoint
  // This checks if all news sources are properly configured and connected
  const testAllSources = async () => {
    resetStates()
    
    try {
      const response = await fetch('http://localhost:8000/api/sources/test')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setApiResponse(JSON.stringify(data, null, 2))
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  // Test function for unified news from all sources
  // Shows source breakdown and api_source field for each article
  const testUnifiedNews = async () => {
    resetStates()
    
    try {
      const response = await fetch('http://localhost:8000/api/news?pageSize=5')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      // Show source breakdown in response + sentiment scores
      const formattedResponse = {
      status: data.status,
      totalSources: data.totalSources,
      sourcesUsed: data.sourcesUsed,
      sourcesFailed: data.sourcesFailed,
      totalArticles: data.totalArticles,
      crossSourceDuplicatesRemoved: data.crossSourceDuplicatesRemoved,
      sentiment_analyzed: data.sentiment_analyzed,        // NEW
      analyzed_sources: data.analyzed_sources,            // NEW
      sampleArticles: data.articles?.slice(0, 5).map((article: any) => ({
        title: article.title,
        source: article.source?.name,
        api_source: article.api_source,
        publishedAt: article.publishedAt,
        uplift_score: article.uplift_score,               // NEW
        sentiment_analysis: article.sentiment_analysis   // NEW - Full sentiment data
      })) || []
    }
    
    setApiResponse(JSON.stringify(formattedResponse, null, 2))
    
  } catch (err) {
    setError(err instanceof Error ? err.message : 'Unknown error occurred')
  } finally {
    setIsLoading(false)
  }
}

  // Test function for NewsAPI source only
  // Note: Currently uses unified endpoint - will be enhanced when backend adds source-specific endpoints
  const testNewsAPIOnly = async () => {
    resetStates()
    
    try {
      // For now, we'll call unified endpoint and filter results by api_source
      const response = await fetch('http://localhost:8000/api/news?pageSize=10')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      // Filter to show only NewsAPI articles
      const newsApiArticles = data.articles?.filter((article: any) => 
        article.api_source === 'newsapi'
      ) || []
      
      const formattedResponse = {
        status: data.status,
        source_filter: 'newsapi',
        total_newsapi_articles: newsApiArticles.length,
        total_all_sources: data.totalArticles,
        newsapi_articles: newsApiArticles.slice(0, 3).map((article: any) => ({
          title: article.title,
          source: article.source?.name,
          api_source: article.api_source,
          publishedAt: article.publishedAt
        }))
      }
      
      setApiResponse(JSON.stringify(formattedResponse, null, 2))
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  // Test function for NewsData source only
  const testNewsDataOnly = async () => {
    resetStates()
    
    try {
      const response = await fetch('http://localhost:8000/api/news?pageSize=10')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      // Filter to show only NewsData articles
      const newsDataArticles = data.articles?.filter((article: any) => 
        article.api_source === 'newsdata'
      ) || []
      
      const formattedResponse = {
        status: data.status,
        source_filter: 'newsdata',
        total_newsdata_articles: newsDataArticles.length,
        total_all_sources: data.totalArticles,
        newsdata_articles: newsDataArticles.slice(0, 3).map((article: any) => ({
          title: article.title,
          source: article.source?.name,
          api_source: article.api_source,
          publishedAt: article.publishedAt
        }))
      }
      
      setApiResponse(JSON.stringify(formattedResponse, null, 2))
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  // Test function for AFP source only
  const testAFPOnly = async () => {
    resetStates()
    
    try {
      // Use the specific AFP endpoint for testing
      const response = await fetch('http://localhost:8000/api/news/afp?pageSize=5')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      const formattedResponse = {
        status: data.status,
        source: 'AFP (direct endpoint)',
        total_articles: data.totalArticles || 0,
        note: 'AFP requires content subscription activation',
        afp_articles: data.articles?.slice(0, 3).map((article: any) => ({
          title: article.title,
          source: article.source?.name,
          api_source: article.api_source,
          publishedAt: article.publishedAt
        })) || []
      }
      
      setApiResponse(JSON.stringify(formattedResponse, null, 2))
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Page header */}
        <h1 className="text-4xl font-bold text-gray-800 mb-6">
          🧪 HopeShot API Test Page
        </h1>

        {/* Status banner to show current page purpose */}
        <StatusBanner 
          status="development" 
          message="Use this page to test backend API connections and individual sources" 
          emoji="🔧"
        />

        {/* Main testing section */}
        <div className="mt-8 space-y-6">
          <h2 className="text-2xl font-semibold text-gray-700">API Test Buttons</h2>
          
          {/* Button container with source-specific layout */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            
            {/* API Health check button */}
            <button
              onClick={testApiEndpoint}
              disabled={isLoading}
              className="bg-green-500 hover:bg-green-600 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              {isLoading ? 'Testing...' : 'Test API Health'}
            </button>

            {/* Test all sources connectivity */}
            <button
              onClick={testAllSources}
              disabled={isLoading}
              className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              {isLoading ? 'Testing...' : 'Test All Sources'}
            </button>

            {/* Get unified news from all sources */}
            <button
              onClick={testUnifiedNews}
              disabled={isLoading}
              className="bg-purple-500 hover:bg-purple-600 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              {isLoading ? 'Testing...' : 'Get Unified News'}
            </button>

            {/* Test NewsAPI only */}
            <button
              onClick={testNewsAPIOnly}
              disabled={isLoading}
              className="bg-orange-500 hover:bg-orange-600 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              {isLoading ? 'Testing...' : 'Test NewsAPI Only'}
            </button>

            {/* Test NewsData only */}
            <button
              onClick={testNewsDataOnly}
              disabled={isLoading}
              className="bg-red-500 hover:bg-red-600 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              {isLoading ? 'Testing...' : 'Test NewsData Only'}
            </button>

            {/* Test AFP only */}
            <button
              onClick={testAFPOnly}
              disabled={isLoading}
              className="bg-yellow-500 hover:bg-yellow-600 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              {isLoading ? 'Testing...' : 'Test AFP Only'}
            </button>
            
          </div>

          {/* Error display section - only shows if there's an error */}
          {error && (
            <div className="mt-6 p-4 border border-red-300 rounded-lg bg-red-50">
              <p className="text-red-700 font-medium">❌ Error:</p>
              <p className="text-red-600 mt-1">{error}</p>
            </div>
          )}

          {/* Enhanced API response display section */}
          <div className="mt-6">
            <h3 className="text-lg font-medium text-gray-700 mb-2">API Response:</h3>
            
            {/* Add response metadata if available */}
            {apiResponse && (
              <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm text-blue-700">
                  📊 <strong>Response received</strong> - Check the data below for source details and article info
                </p>
              </div>
            )}
            
            {/* Improved response container with better styling */}
            <div className="bg-white border rounded-lg shadow-sm">
              <div className="bg-gray-50 px-4 py-2 border-b rounded-t-lg">
                <span className="text-sm font-medium text-gray-600">JSON Response Data</span>
              </div>
              <pre className="p-4 overflow-x-auto text-sm font-mono leading-relaxed min-h-[300px] max-h-[600px] overflow-y-auto">
                {apiResponse || '💡 No response yet - click a button above to test an endpoint!\n\n🔍 Look for these key fields:\n• sourcesUsed: Which APIs provided data\n• api_source: Shows source for each article\n• totalArticles: Number of articles found\n• crossSourceDuplicatesRemoved: Duplicate detection results'}
              </pre>
            </div>
            
            {/* Add helper text */}
            <div className="mt-2 text-xs text-gray-500">
              💡 <strong>Pro tip:</strong> Look for the <code>api_source</code> field in articles to see which news provider supplied each story
            </div>
          </div>
          
        </div>
      </div>
    </div>
  )
}