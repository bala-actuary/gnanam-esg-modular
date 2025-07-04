import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Alert,
  Button,
  Chip
} from '@mui/material';
import {
  Assessment,
  Timeline,
  Refresh,
  CheckCircle,
  Warning,
  Error,
  Analytics
} from '@mui/icons-material';
import apiService, { DashboardStats, Model as ApiModel, ModelsResponse } from '../services/api';

interface SystemStatus {
  status: 'healthy' | 'warning' | 'error';
  message: string;
  uptime: string;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [models, setModels] = useState<ApiModel[]>([]);
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    status: 'healthy',
    message: 'All systems operational',
    uptime: 'Loading...'
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch dashboard stats
      const dashboardStats = await apiService.getDashboardStats();
      setStats(dashboardStats);

      // Fetch models
      const modelResponse: ModelsResponse = await apiService.getModels();
      // The API returns { models: {...}, total_count: 7, categories: [...] }
      // We need to convert the models object to an array
      const modelList = Object.entries(modelResponse.models || {}).map(([id, model]) => ({
        id,
        name: model.name,
        category: model.category,
        description: model.description,
        parameters: model.parameters || [],
        status: 'active' as const
      }));
      setModels(modelList);

      // Check system health
      try {
        await apiService.healthCheck();
        setSystemStatus({
          status: 'healthy',
          message: 'All systems operational',
          uptime: '2 days, 14 hours'
        });
      } catch (healthError) {
        setSystemStatus({
          status: 'warning',
          message: 'Some services may be experiencing issues',
          uptime: 'Unknown'
        });
      }
    } catch (err: any) {
      const errorMessage = err?.message || 'Failed to load dashboard data';
      setError(errorMessage);
      setSystemStatus({
        status: 'error',
        message: 'System connectivity issues detected',
        uptime: 'Unknown'
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const getStatusIcon = (status: 'healthy' | 'warning' | 'error') => {
    switch (status) {
      case 'healthy':
        return <CheckCircle sx={{ color: 'success.main' }} />;
      case 'warning':
        return <Warning sx={{ color: 'warning.main' }} />;
      case 'error':
        return <Error sx={{ color: 'error.main' }} />;
    }
  };

  const getStatusColor = (status: 'healthy' | 'warning' | 'error') => {
    switch (status) {
      case 'healthy':
        return 'success';
      case 'warning':
        return 'warning';
      case 'error':
        return 'error';
    }
  };

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <LinearProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Button
          variant="outlined"
          startIcon={<Refresh />}
          onClick={fetchDashboardData}
          disabled={loading}
        >
          Refresh
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* System Status */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            {getStatusIcon(systemStatus.status)}
            <Typography variant="h6" sx={{ ml: 1 }}>
              System Status
            </Typography>
            <Chip
              label={systemStatus.status.toUpperCase()}
              color={getStatusColor(systemStatus.status)}
              size="small"
              sx={{ ml: 'auto' }}
            />
          </Box>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            {systemStatus.message}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Uptime: {systemStatus.uptime}
          </Typography>
        </CardContent>
      </Card>

      {/* Key Metrics */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 3 }}>
        <Card sx={{ flex: '1 1 200px', minWidth: '200px' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Analytics sx={{ mr: 1, color: 'primary.main' }} />
              <Box>
                <Typography variant="h4">
                  {stats?.total_models || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Total Models
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ flex: '1 1 200px', minWidth: '200px' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <CheckCircle sx={{ mr: 1, color: 'success.main' }} />
              <Box>
                <Typography variant="h4">
                  {stats?.active_models || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Active Models
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ flex: '1 1 200px', minWidth: '200px' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Assessment sx={{ mr: 1, color: 'info.main' }} />
              <Box>
                <Typography variant="h4">
                  {stats?.total_scenarios || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Total Scenarios
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ flex: '1 1 200px', minWidth: '200px' }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Timeline sx={{ mr: 1, color: 'secondary.main' }} />
              <Box>
                <Typography variant="h4">
                  {stats?.recent_runs || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Recent Runs
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </Box>

      {/* Model Status */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Model Status
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
            {models.map((model) => (
              <Card key={model.id} variant="outlined" sx={{ flex: '1 1 300px', minWidth: '300px' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box>
                      <Typography variant="subtitle1" gutterBottom>
                        {model.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {model.category}
                      </Typography>
                    </Box>
                    <Chip
                      label={model.status}
                      color={model.status === 'active' ? 'success' : 'default'}
                      size="small"
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {model.description}
                  </Typography>
                </CardContent>
              </Card>
            ))}
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Dashboard; 