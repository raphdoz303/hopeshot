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

  // Test function for root endpoint (/)
  // This checks if our FastAPI backend is running and responding
  const testRootEndpoint = async () => {
    resetStates()
    
    try {
      const response = await fetch('http://localhost:8000/')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      setApiResponse(JSON.stringify(data, null, 2))  // Pretty format JSON with 2-space indentation
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred')
    } finally {
      setIsLoading(false)  // Always reset loading state
    }
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

  // Test function for /api/news endpoint
  // This fetches real news articles from NewsAPI and formats them for display
  const testNewsAPI = async () => {
    resetStates()
    
    try {
      // Request 5 articles for faster testing
      const response = await fetch('http://localhost:8000/api/news?pageSize=5')
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      


      // Create a formatted summary instead of showing all article data
      // This makes the response easier to read and faster to load
const formattedResponse = {
  status: data.status,
  requested: 5,
  uniqueArticles: data.uniqueArticles,
  duplicatesRemoved: data.duplicatesRemoved,
  sampleTitles: data.articles?.map((article: any) => ({
    title: article.title,
    source: article.source?.name || 'Unknown'
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
          message="Use this page to test backend API connections" 
          emoji="🔧"
        />

        {/* Main testing section */}
        <div className="mt-8 space-y-6">
          <h2 className="text-2xl font-semibold text-gray-700">API Test Buttons</h2>
          
          {/* Button container with consistent spacing */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            {/* Root endpoint test button */}
            <button
              onClick={testRootEndpoint}
              disabled={isLoading}
              className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              {isLoading ? 'Testing...' : 'Test Root (/)'}
            </button>

            {/* API test endpoint button */}
            <button
              onClick={testApiEndpoint}
              disabled={isLoading}
              className="bg-green-500 hover:bg-green-600 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              {isLoading ? 'Testing...' : 'Test API (/api/test)'}
            </button>

            {/* News API test button */}
            <button
              onClick={testNewsAPI}
              disabled={isLoading}
              className="bg-purple-500 hover:bg-purple-600 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              {isLoading ? 'Testing...' : 'Test News API'}
            </button>
            
          </div>

          {/* Error display section - only shows if there's an error */}
          {error && (
            <div className="mt-6 p-4 border border-red-300 rounded-lg bg-red-50">
              <p className="text-red-700 font-medium">❌ Error:</p>
              <p className="text-red-600 mt-1">{error}</p>
            </div>
          )}

          {/* API response display section */}
          <div className="mt-6">
            <h3 className="text-lg font-medium text-gray-700 mb-2">API Response:</h3>
            <pre className="bg-gray-100 border rounded-lg p-4 overflow-x-auto text-sm min-h-[200px]">
              {apiResponse || 'No response yet - click a button above to test an endpoint!'}
            </pre>
          </div>
          
        </div>
      </div>
    </div>
  )
}