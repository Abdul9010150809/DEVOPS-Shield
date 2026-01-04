/**
 * Performance Monitoring Hook - React Performance Optimization
 * ==============================================================
 * 
 * This hook provides comprehensive performance monitoring for React components
 * including render time tracking, memory usage monitoring, and optimization suggestions.
 */

import { useEffect, useRef, useState, useCallback, useMemo } from 'react';

// Performance metrics object structure
const createPerformanceMetrics = (componentName) => ({
  renderCount: 0,
  totalRenderTime: 0,
  averageRenderTime: 0,
  lastRenderTime: 0,
  memoryUsage: 0,
  componentId: componentName,
  isOptimized: true,
  recommendations: []
});

// Performance threshold constants
const PERFORMANCE_THRESHOLDS = {
  MAX_RENDER_TIME_MS: 16, // 60fps target
  MAX_AVERAGE_RENDER_TIME_MS: 10,
  MAX_MEMORY_USAGE_MB: 50,
  MAX_RENDER_COUNT: 100,
  WARNING_RENDER_COUNT: 50
};

// Performance recommendation rules
const RECOMMENDATION_RULES = [
  {
    condition: (metrics) => metrics.averageRenderTime > PERFORMANCE_THRESHOLDS.MAX_AVERAGE_RENDER_TIME_MS,
    message: 'Component renders slowly. Consider using React.memo() or useMemo().'
  },
  {
    condition: (metrics) => metrics.renderCount > PERFORMANCE_THRESHOLDS.WARNING_RENDER_COUNT,
    message: 'Component renders frequently. Check for unnecessary re-renders.'
  },
  {
    condition: (metrics) => metrics.memoryUsage > PERFORMANCE_THRESHOLDS.MAX_MEMORY_USAGE_MB,
    message: 'High memory usage. Consider optimizing data structures or using lazy loading.'
  },
  {
    condition: (metrics) => metrics.lastRenderTime > PERFORMANCE_THRESHOLDS.MAX_RENDER_TIME_MS * 2,
    message: 'Last render was very slow. Consider breaking component into smaller pieces.'
  }
];

/**
 * Hook for monitoring component performance
 * @param {string} componentName - Name of the component for identification
 * @param {Object} options - Configuration options
 * @returns {Object} Performance metrics and utilities
 */
export const usePerformanceMonitor = (
  componentName,
  options = {}
) => {
  const {
    enableMemoryTracking = true,
    enableRenderTracking = true,
    enableRecommendations = true,
    logThreshold = PERFORMANCE_THRESHOLDS.MAX_RENDER_TIME_MS
  } = options;

  // Component state
  const [metrics, setMetrics] = useState(() => createPerformanceMetrics(componentName));

  // Refs for tracking
  const renderCountRef = useRef(0);
  const totalRenderTimeRef = useRef(0);
  const lastRenderTimeRef = useRef(0);
  const renderStartTimeRef = useRef(0);
  const componentIdRef = useRef(componentName);

  // Memory tracking
  const getMemoryUsage = useCallback(() => {
    if (!enableMemoryTracking || typeof window === 'undefined') return 0;
    
    try {
      const perf = window.performance;
      if (perf && perf.memory) {
        return Math.round(perf.memory.usedJSHeapSize / 1024 / 1024);
      }
    } catch (error) {
      console.warn('Memory tracking not available:', error);
    }
    return 0;
  }, [enableMemoryTracking]);

  // Generate performance recommendations
  const generateRecommendations = useCallback((currentMetrics) => {
    if (!enableRecommendations) return [];
    
    return RECOMMENDATION_RULES
      .filter(rule => rule.condition(currentMetrics))
      .map(rule => rule.message);
  }, [enableRecommendations]);

  // Update metrics
  const updateMetrics = useCallback(() => {
    const currentRenderCount = renderCountRef.current;
    const currentTotalRenderTime = totalRenderTimeRef.current;
    const currentLastRenderTime = lastRenderTimeRef.current;
    const currentMemoryUsage = getMemoryUsage();
    
    const averageRenderTime = currentRenderCount > 0 
      ? currentTotalRenderTime / currentRenderCount 
      : 0;
    
    const isOptimized = 
      averageRenderTime <= PERFORMANCE_THRESHOLDS.MAX_AVERAGE_RENDER_TIME_MS &&
      currentRenderCount <= PERFORMANCE_THRESHOLDS.WARNING_RENDER_COUNT &&
      currentMemoryUsage <= PERFORMANCE_THRESHOLDS.MAX_MEMORY_USAGE_MB;
    
    const newMetrics = {
      renderCount: currentRenderCount,
      totalRenderTime: currentTotalRenderTime,
      averageRenderTime,
      lastRenderTime: currentLastRenderTime,
      memoryUsage: currentMemoryUsage,
      componentId: componentIdRef.current,
      isOptimized,
      recommendations: generateRecommendations({
        renderCount: currentRenderCount,
        totalRenderTime: currentTotalRenderTime,
        averageRenderTime,
        lastRenderTime: currentLastRenderTime,
        memoryUsage: currentMemoryUsage,
        componentId: componentIdRef.current,
        isOptimized,
        recommendations: []
      })
    };
    
    setMetrics(newMetrics);
    
    // Log performance warnings
    if (currentLastRenderTime > logThreshold) {
      console.warn(
        `🐌 Slow render detected in ${componentName}: ${currentLastRenderTime.toFixed(2)}ms`,
        newMetrics
      );
    }
  }, [getMemoryUsage, generateRecommendations, logThreshold, componentName]);

  // Start render timing
  const startRenderTiming = useCallback(() => {
    if (!enableRenderTracking) return;
    
    renderStartTimeRef.current = performance.now();
  }, [enableRenderTracking]);

  // End render timing
  const endRenderTiming = useCallback(() => {
    if (!enableRenderTracking || renderStartTimeRef.current === 0) return;
    
    const renderTime = performance.now() - renderStartTimeRef.current;
    renderCountRef.current += 1;
    totalRenderTimeRef.current += renderTime;
    lastRenderTimeRef.current = renderTime;
    
    updateMetrics();
    renderStartTimeRef.current = 0;
  }, [enableRenderTracking, updateMetrics]);

  // Performance monitoring effect
  useEffect(() => {
    startRenderTiming();
    
    return () => {
      endRenderTiming();
    };
  });

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      // Log final metrics
      if (process.env.NODE_ENV === 'development') {
        console.log(`📊 Performance metrics for ${componentName}:`, metrics);
      }
    };
  }, [componentName, metrics]);

  // Memoized performance utilities
  const performanceUtils = useMemo(() => ({
    /**
     * Check if component is performing well
     */
    isPerformant: metrics.isOptimized,
    
    /**
     * Get performance score (0-100)
     */
    getPerformanceScore: () => {
      let score = 100;
      
      // Deduct points for slow renders
      if (metrics.averageRenderTime > PERFORMANCE_THRESHOLDS.MAX_AVERAGE_RENDER_TIME_MS) {
        score -= Math.min(30, (metrics.averageRenderTime - PERFORMANCE_THRESHOLDS.MAX_AVERAGE_RENDER_TIME_MS) / 2);
      }
      
      // Deduct points for high render count
      if (metrics.renderCount > PERFORMANCE_THRESHOLDS.WARNING_RENDER_COUNT) {
        score -= Math.min(20, (metrics.renderCount - PERFORMANCE_THRESHOLDS.WARNING_RENDER_COUNT) / 5);
      }
      
      // Deduct points for high memory usage
      if (metrics.memoryUsage > PERFORMANCE_THRESHOLDS.MAX_MEMORY_USAGE_MB) {
        score -= Math.min(25, (metrics.memoryUsage - PERFORMANCE_THRESHOLDS.MAX_MEMORY_USAGE_MB) / 2);
      }
      
      return Math.max(0, Math.round(score));
    },
    
    /**
     * Get performance grade
     */
    getPerformanceGrade: () => {
      const score = performanceUtils.getPerformanceScore();
      if (score >= 90) return 'A';
      if (score >= 80) return 'B';
      if (score >= 70) return 'C';
      if (score >= 60) return 'D';
      return 'F';
    },
    
    /**
     * Reset metrics
     */
    resetMetrics: () => {
      renderCountRef.current = 0;
      totalRenderTimeRef.current = 0;
      lastRenderTimeRef.current = 0;
      updateMetrics();
    }
  }), [metrics, updateMetrics]);

  return {
    metrics,
    ...performanceUtils
  };
};

/**
 * Hook for optimizing expensive calculations
 * @param {Function} calculation - Expensive calculation function
 * @param {Array} dependencies - Dependencies for memoization
 * @param {Object} options - Configuration options
 * @returns {Object} Memoized result and performance info
 */
export const useOptimizedCalculation = (
  calculation,
  dependencies,
  options = {}
) => {
  const { name = 'Calculation', threshold = 10 } = options;
  const [calculationTime, setCalculationTime] = useState(0);
  const [isSlow, setIsSlow] = useState(false);
  
  const result = useMemo(() => {
    const startTime = performance.now();
    const result = calculation();
    const endTime = performance.now();
    const duration = endTime - startTime;
    
    setCalculationTime(duration);
    setIsSlow(duration > threshold);
    
    if (duration > threshold) {
      console.warn(`🐌 Slow ${name}: ${duration.toFixed(2)}ms`);
    }
    
    return result;
  }, dependencies);
  
  return {
    result,
    calculationTime,
    isSlow,
    isOptimized: !isSlow
  };
};

/**
 * Hook for optimizing async operations
 * @param {Function} asyncOperation - Async operation function
 * @param {Array} dependencies - Dependencies for memoization
 * @returns {Object} Memoized async result and loading state
 */
export const useOptimizedAsync = (
  asyncOperation,
  dependencies
) => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastExecution, setLastExecution] = useState(null);
  
  useEffect(() => {
    let cancelled = false;
    
    const executeOperation = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const startTime = performance.now();
        const result = await asyncOperation();
        const endTime = performance.now();
        const duration = endTime - startTime;
        
        if (!cancelled) {
          setResult(result);
          setLastExecution(new Date());
          
          if (duration > 1000) {
            console.warn(`🐌 Slow async operation: ${duration.toFixed(2)}ms`);
          }
        }
      } catch (err) {
        if (!cancelled) {
          setError(err);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };
    
    executeOperation();
    
    return () => {
      cancelled = true;
    };
  }, dependencies);
  
  return {
    result,
    loading,
    error,
    lastExecution,
    execute: asyncOperation
  };
};

/**
 * Hook for virtual scrolling performance
 * @param {Array} items - Array of items to virtualize
 * @param {number} itemHeight - Height of each item
 * @param {number} containerHeight - Height of container
 * @returns {Object} Virtualized items and scroll utilities
 */
export const useVirtualScroll = (
  items,
  itemHeight,
  containerHeight
) => {
  const [scrollTop, setScrollTop] = useState(0);
  const [containerRef, setContainerRef] = useState(null);
  
  const visibleItems = useMemo(() => {
    const startIndex = Math.floor(scrollTop / itemHeight);
    const endIndex = Math.min(
      startIndex + Math.ceil(containerHeight / itemHeight) + 1,
      items.length
    );
    
    return {
      startIndex,
      endIndex,
      items: items.slice(startIndex, endIndex),
      offsetY: startIndex * itemHeight
    };
  }, [items, scrollTop, itemHeight, containerHeight]);
  
  const handleScroll = useCallback((e) => {
    setScrollTop(e.currentTarget.scrollTop);
  }, []);
  
  return {
    ...visibleItems,
    containerRef,
    onScroll: handleScroll,
    totalHeight: items.length * itemHeight
  };
};

/**
 * Hook for debounced values with performance tracking
 * @param {*} value - Value to debounce
 * @param {number} delay - Delay in milliseconds
 * @returns {*} Debounced value
 */
export const useDebouncedValue = (value, delay) => {
  const [debouncedValue, setDebouncedValue] = useState(value);
  const [isDebouncing, setIsDebouncing] = useState(false);
  
  useEffect(() => {
    setIsDebouncing(true);
    
    const handler = setTimeout(() => {
      setDebouncedValue(value);
      setIsDebouncing(false);
    }, delay);
    
    return () => {
      clearTimeout(handler);
      setIsDebouncing(false);
    };
  }, [value, delay]);
  
  return debouncedValue;
};

export default usePerformanceMonitor;
