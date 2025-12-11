import apiClient from '../services/apiClient';

class PipelineController {
  async getPipelines(limit = 10) {
    try {
      const response = await apiClient.get(`/api/pipelines/?limit=${limit}`);
      console.log('[PipelineController] Pipelines response:', response);
      return response?.data || response;
    } catch (error) {
      console.error('[PipelineController] Error fetching pipelines:', error);
      throw error;
    }
  }

  async getPipelineHistory(days = 7) {
    try {
      const response = await apiClient.get(`/api/pipelines/history?days=${days}`);
      console.log('[PipelineController] History response:', response);
      return response?.data || response;
    } catch (error) {
      console.error('[PipelineController] Error fetching history:', error);
      throw error;
    }
  }

  async getPipelineDetails(pipelineId) {
    try {
      const response = await apiClient.get(`/api/pipelines/${pipelineId}/`);
      console.log('[PipelineController] Details response:', response);
      return response?.data || response;
    } catch (error) {
      console.error('[PipelineController] Error fetching details:', error);
      throw error;
    }
  }
}

export default new PipelineController();
