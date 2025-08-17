// Test page to verify frontend-backend communication

'use client'  // This makes it a client component (can use hooks and events)

import { useState } from 'react'
import StatusBanner from '../../components/StatusBanner'

export default function TestPage() {
  // State to store API responses
  const [apiResponse, setApiResponse] = useState<string>('')
  const [isLoading, setIsLoading] = useState(false)

  // Function to test the root endpoint
  const testRootEndpoint = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('http://localhost:8000/')
      const data = await response.json()
      setApiResponse(JSON.stringify(data, null, 2))  // Pretty format JSON
    } catch (error) {
      setApiResponse(`Error: ${error}`)
    }
    setIsLoading(false)
  }

  // Function to test the /api/test endpoint
  const testApiEndpoint = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/test')
      const data = await response.json()
      setApiResponse(JSON.stringify(data, null, 2))
    } catch (error) {
      setApiResponse(`Error: ${error}`)
    }
    setIsLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-800 mb-6">
          🧪 HopeShot API Test Page
        </h1>

        <StatusBanner 
          status="development" 
          message="Use this page to test backend API connections" 
          emoji="🔧"
        />

        <div className="mt-8 space-y-4">
          <h2 className="text-2xl font-semibold text-gray-700">API Test Buttons</h2>
          
          {/* Test buttons */}
          <div className="flex space-x-4">
            <button
              onClick={testRootEndpoint}
              disabled={isLoading}
              className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-medium"
            >
              {isLoading ? 'Testing...' : 'Test Root Endpoint (/)'}
            </button>

            <button
              onClick={testApiEndpoint}
              disabled={isLoading}
              className="bg-green-500 hover:bg-green-600 disabled:bg-gray-400 text-white px-6 py-3 rounded-lg font-medium"
            >
              {isLoading ? 'Testing...' : 'Test API Endpoint (/api/test)'}
            </button>
          </div>

          {/* Response display */}
          <div className="mt-6">
            <h3 className="text-lg font-medium text-gray-700 mb-2">API Response:</h3>
            <pre className="bg-gray-100 border rounded-lg p-4 overflow-x-auto text-sm">
              {apiResponse || 'No response yet - click a button above to test!'}
            </pre>
          </div>
        </div>
      </div>
    </div>
  )
}