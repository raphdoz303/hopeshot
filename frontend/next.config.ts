import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Memory optimization for development
  experimental: {
    // Reduce memory usage during compilation
    turbo: {
      memoryLimit: 512, // Limit Turbo to 512MB
    },
    // Disable some memory-intensive features in development
    optimizeCss: false,
    scrollRestoration: false,
  },

  // Webpack optimization for lower memory usage
  webpack: (config, { dev, isServer }) => {
    if (dev && !isServer) {
      // Reduce bundle splitting to save memory
      config.optimization.splitChunks = {
        chunks: 'all',
        minSize: 20000,
        maxSize: 250000,
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            chunks: 'all',
          },
        },
      };

      // Reduce webpack worker memory usage
      config.optimization.minimize = false;
      config.optimization.moduleIds = 'deterministic';
      
      // Limit parallel processing to reduce memory spikes
      config.parallelism = 1;
    }
    
    return config;
  },

  // Compiler options
  compiler: {
    // Remove console logs in production but keep them in development
    removeConsole: false,
  },

  // Disable some features that consume memory during development
  poweredByHeader: false,
  compress: false, // Disable compression in dev for faster builds
  
  // Optimize image handling
  images: {
    domains: [], // Add domains as needed
    unoptimized: true, // Skip image optimization in development
  },
};

export default nextConfig;
