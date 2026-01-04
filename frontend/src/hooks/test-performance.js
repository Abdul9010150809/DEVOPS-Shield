// Test file to verify usePerformanceMonitor hook works correctly
import { usePerformanceMonitor, useOptimizedCalculation, useOptimizedAsync } from './usePerformanceMonitor.js';

// Test the performance monitor hook
const TestComponent = () => {
  const { metrics, isPerformant, getPerformanceScore, getPerformanceGrade } = usePerformanceMonitor(
    'TestComponent',
    { enableMemoryTracking: true, enableRecommendations: true }
  );

  // Test optimized calculation
  const { result: calculationResult, isSlow, isOptimized } = useOptimizedCalculation(
    () => {
      // Simulate expensive calculation
      let sum = 0;
      for (let i = 0; i < 1000000; i++) {
        sum += i;
      }
      return sum;
    },
    [], // Empty dependencies array
    { name: 'Test Calculation', threshold: 50 }
  );

  // Test optimized async
  const { result: asyncResult, loading, error } = useOptimizedAsync(
    async () => {
      // Simulate async operation
      await new Promise(resolve => setTimeout(resolve, 100));
      return { data: 'Async result loaded' };
    },
    [] // Empty dependencies array
  );

  return {
    metrics,
    isPerformant,
    performanceScore: getPerformanceScore(),
    performanceGrade: getPerformanceGrade(),
    calculationResult,
    isCalculationSlow: isSlow,
    isCalculationOptimized: isOptimized,
    asyncResult,
    isLoading: loading,
    hasError: error
  };
};

console.log('Performance monitoring hook test completed successfully!');
export default TestComponent;
