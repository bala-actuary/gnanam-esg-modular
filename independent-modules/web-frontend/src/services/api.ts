const API_BASE_URL = 'http://localhost:8000';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface ModelParameter {
  name: string;
  type: string;
  default: any;
}

export interface Model {
  id: string;
  name: string;
  category: string;
  description: string;
  status: 'active' | 'inactive';
  parameters: ModelParameter[];
}

export interface ModelsResponse {
  models: Record<string, {
    name: string;
    category: string;
    description: string;
    parameters: ModelParameter[];
  }>;
  total_count: number;
  categories: string[];
}

export interface ModelRunRequest {
  model_type: string;
  parameters: Record<string, any>;
  scenario_name?: string;
  user_id?: string;
}

export interface ModelRunResponse {
  model_type: string;
  scenario_name: string;
  status: string;
  results: Record<string, any>;
  execution_time: number;
  timestamp: string;
}

export interface DashboardStats {
  total_models: number;
  active_models: number;
  total_scenarios: number;
  recent_runs: number;
}

class ApiService {
  private token: string | null = null;

  constructor() {
    // Clear token when page is unloaded (browser tab closed)
    window.addEventListener('beforeunload', () => {
      this.clearToken();
    });
    
    // Clear token when page becomes hidden (user switches tabs or minimizes)
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'hidden') {
        this.clearToken();
      }
    });
    
    // Clear token when user navigates away
    window.addEventListener('pagehide', () => {
      this.clearToken();
    });
  }

  setToken(token: string) {
    this.token = token;
    sessionStorage.setItem('auth_token', token);
  }

  getToken(): string | null {
    if (!this.token) {
      this.token = sessionStorage.getItem('auth_token');
    }
    return this.token;
  }

  clearToken() {
    this.token = null;
    sessionStorage.removeItem('auth_token');
    localStorage.removeItem('auth_token'); // Clear any old localStorage tokens too
  }

  forceLogout() {
    this.clearToken();
    // Redirect to login page
    window.location.href = '/';
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const token = this.getToken();

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        if (response.status === 401) {
          this.clearToken();
          throw new Error('Authentication required. Please log in again.');
        }
        
        let errorMessage = `HTTP Error: ${response.status}`;
        try {
          const errorData = await response.json();
          if (errorData.detail) {
            if (Array.isArray(errorData.detail)) {
              errorMessage = errorData.detail.map((e: any) => `${e.loc.join('.')} - ${e.msg}`).join('; ');
            } else {
              errorMessage = errorData.detail;
            }
          } else if (errorData.errors) {
            errorMessage = `Validation errors: ${JSON.stringify(errorData.errors)}`;
          }
        } catch (e) {
          errorMessage = `HTTP Error: ${response.status} - ${response.statusText}`;
        }
        
        throw new Error(errorMessage);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Authentication
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await this.request<LoginResponse>('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData.toString(),
    });
    this.setToken(response.access_token);
    return response;
  }

  async logout(): Promise<void> {
    await this.request('/api/v1/auth/logout', { method: 'POST' });
    this.clearToken();
  }

  // Models
  async getModels(): Promise<ModelsResponse> {
    return this.request<ModelsResponse>('/api/v1/models');
  }

  async runModel(request: ModelRunRequest): Promise<ModelRunResponse> {
    return this.request<ModelRunResponse>('/api/v1/models/run', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getModelStatus(jobId: string): Promise<ModelRunResponse> {
    return this.request<ModelRunResponse>(`/api/v1/models/status/${jobId}`);
  }

  // Dashboard
  async getDashboardStats(): Promise<DashboardStats> {
    return this.request<DashboardStats>('/api/v1/dashboard/stats');
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    return this.request<{ status: string }>('/health');
  }

  // Scenarios
  async getScenarios(): Promise<any[]> {
    return this.request<any[]>('/api/v1/scenarios');
  }

  async createScenario(scenario: any): Promise<any> {
    return this.request<any>('/api/v1/scenarios', {
      method: 'POST',
      body: JSON.stringify(scenario),
    });
  }

  async getScenario(scenarioId: string): Promise<any> {
    return this.request<any>(`/api/v1/scenarios/${scenarioId}`);
  }

  async updateScenario(scenarioId: string, scenario: any): Promise<any> {
    return this.request<any>(`/api/v1/scenarios/${scenarioId}`, {
      method: 'PUT',
      body: JSON.stringify(scenario),
    });
  }

  async deleteScenario(scenarioId: string): Promise<void> {
    return this.request<void>(`/api/v1/scenarios/${scenarioId}`, {
      method: 'DELETE',
    });
  }

  async downloadScenarioResults(scenarioId: string): Promise<any> {
    return this.request<any>(`/api/v1/scenarios/${scenarioId}/download`);
  }

  async getScenarioReport(scenarioId: string): Promise<any> {
    return this.request<any>(`/api/v1/scenarios/${scenarioId}/report`);
  }

  async configureScenario(scenarioId: string, configuration: any): Promise<any> {
    return this.request<any>(`/api/v1/scenarios/${scenarioId}/configure`, {
      method: 'POST',
      body: JSON.stringify(configuration),
    });
  }
}

export const apiService = new ApiService();
export default apiService; 