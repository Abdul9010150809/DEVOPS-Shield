/**
 * Zero Trust API Service
 * Handles all Zero Trust pipeline API calls
 */

import api from './apiConfig';

const nowIso = () => new Date().toISOString();

const createStubDependencyResponse = (manifest) => {
  const blocked = Object.keys(manifest || {}).filter((pkg) => /rogue|shadow|unknown/i.test(pkg));
  return {
    approved: blocked.length === 0,
    blocked_packages: blocked,
    reasons: blocked.map((pkg) => `Policy violation detected for ${pkg}`),
  };
};

export const zeroTrustService = {
  /**
   * Health check
   */
  healthCheck: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      return {
        status: 'degraded',
        environment: 'demo-fallback',
        timestamp: nowIso(),
        error: error.message || 'unreachable',
      };
    }
  },

  /**
   * Verify source integrity
   */
  verifySourceIntegrity: async (data) => {
    try {
      const response = await api.post('/api/zero-trust/source/verify', data);
      return response.data;
    } catch (error) {
      console.error('Source integrity verification failed:', error);
      const hasSecrets = Boolean(data?.has_secrets);
      return {
        identity_score: hasSecrets ? 0.58 : 0.83,
        secrets_found: hasSecrets,
        approved: !hasSecrets,
        reasons: hasSecrets ? ['simulated_secret_pattern'] : [],
        fallback: true,
      };
    }
  },

  /**
   * Check dependencies
   */
  checkDependencies: async (manifest) => {
    try {
      const response = await api.post('/api/zero-trust/deps/check', { manifest });
      return response.data;
    } catch (error) {
      console.error('Dependency check failed:', error);
      return {
        ...createStubDependencyResponse(manifest),
        fallback: true,
      };
    }
  },

  /**
   * Record to blockchain ledger
   */
  recordToBlockchain: async (data) => {
    try {
      const response = await api.post('/api/zero-trust/ledger/record', data);
      return response.data;
    } catch (error) {
      console.error('Blockchain recording failed:', error);
      return {
        recorded: true,
        chain_valid: true,
        fallback: true,
        storage: 'local-ledger',
        timestamp: nowIso(),
      };
    }
  },

  /**
   * Verify artifact
   */
  verifyArtifact: async (data) => {
    try {
      const response = await api.post('/api/zero-trust/artifact/verify', data);
      return response.data;
    } catch (error) {
      console.error('Artifact verification failed:', error);
      return {
        signed: Boolean(data?.signature),
        sandbox_verified: true,
        approved: Boolean(data?.signature),
        fallback: true,
      };
    }
  },

  /**
   * Get security data
   */
  getSecurityScenarios: async () => {
    try {
      const response = await api.get('/api/data/real_world_security_scenarios');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch security scenarios:', error);
      throw error;
    }
  },

  /**
   * Get blockchain architecture data
   */
  getBlockchainArchitecture: async () => {
    try {
      const response = await api.get('/api/data/blockchain_trust_architecture');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch blockchain architecture:', error);
      throw error;
    }
  },
};

export default zeroTrustService;
