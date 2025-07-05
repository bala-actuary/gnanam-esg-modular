
import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  LinearProgress,
  IconButton,
  Tooltip,
  Divider
} from '@mui/material';
import {
  PlayArrow,
  Settings,
  Info,
  CheckCircle,
  Error,
  Refresh,
  Tune
} from '@mui/icons-material';
import apiService, { Model, ModelRunRequest, ModelsResponse, ModelRunResponse } from '../services/api';

interface ModelExecution {
  modelId: string;
  status: 'idle' | 'running' | 'completed' | 'failed';
  result?: any;
  error?: string;
}

interface ModelSettings {
  modelId: string;
  parameters: Record<string, any>;
  description: string;
}

const Models: React.FC = () => {
  const [models, setModels] = useState<Model[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedModel, setSelectedModel] = useState<Model | null>(null);
  const [executionDialog, setExecutionDialog] = useState(false);
  const [settingsDialog, setSettingsDialog] = useState(false);
  const [executionParams, setExecutionParams] = useState<Record<string, any>>({});
  const [modelSettings, setModelSettings] = useState<ModelSettings[]>([]);
  const [executions, setExecutions] = useState<ModelExecution[]>([]);

  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    try {
      setLoading(true);
      setError(null);
      const modelResponse: ModelsResponse = await apiService.getModels();
      const modelList = Object.entries(modelResponse.models || {}).map(([id, modelData]) => ({
        id,
        name: modelData.name,
        category: modelData.category,
        description: modelData.description,
        parameters: modelData.parameters || [],
        status: 'active' as const
      }));
      setModels(modelList);
    } catch (err: any) {
      const errorMessage = err?.message || 'Failed to load models';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleRunModel = (model: Model) => {
    setSelectedModel(model);
    const defaultParams = model.parameters.reduce((acc, param) => {
      acc[param.name] = param.default;
      return acc;
    }, {} as Record<string, any>);
    setExecutionParams(defaultParams);
    setExecutionDialog(true);
  };

  const handleSettingsClick = (model: Model) => {
    setSelectedModel(model);
    const existingSettings = modelSettings.find(s => s.modelId === model.id);
    if (existingSettings) {
      setExecutionParams(existingSettings.parameters);
    } else {
      const defaultParams = model.parameters.reduce((acc, param) => {
        acc[param.name] = param.default;
        return acc;
      }, {} as Record<string, any>);
      setExecutionParams(defaultParams);
    }
    setSettingsDialog(true);
  };

  const handleSaveSettings = () => {
    if (!selectedModel) return;
    const newSettings: ModelSettings = {
      modelId: selectedModel.id,
      parameters: { ...executionParams },
      description: `Settings for ${selectedModel.name}`
    };
    setModelSettings(prev => {
      const filtered = prev.filter(s => s.modelId !== selectedModel.id);
      return [...filtered, newSettings];
    });
    setSettingsDialog(false);
  };

  const handleExecuteModel = async () => {
    if (!selectedModel) return;

    const execution: ModelExecution = {
      modelId: selectedModel.id,
      status: 'running'
    };

    setExecutions(prev => [...prev, execution]);
    setExecutionDialog(false);

    try {
      const request: ModelRunRequest = {
        model_type: selectedModel.id,
        parameters: { ...executionParams }
      };

      const response = await apiService.runModel(request);
      
      setExecutions(prev => prev.map(exec => 
        exec.modelId === selectedModel.id 
          ? { ...exec, status: 'completed', result: response.results }
          : exec
      ));
    } catch (err: any) {
      const errorMessage = err?.message || 'Execution failed';
      setExecutions(prev => prev.map(exec => 
        exec.modelId === selectedModel.id 
          ? { ...exec, status: 'failed', error: errorMessage }
          : exec
      ));
    }
  };

  const renderParameterFields = (model: Model) => {
    return model.parameters.map(param => (
      <TextField
        key={param.name}
        label={param.name}
        type={param.type === 'float' ? 'number' : 'text'}
        value={executionParams[param.name] || ''}
        onChange={(e) => setExecutionParams(prev => ({
          ...prev,
          [param.name]: param.type === 'float' ? parseFloat(e.target.value) : e.target.value
        }))}
        helperText={`Default: ${param.default}`}
        fullWidth
      />
    ));
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle sx={{ color: 'success.main' }} />;
      case 'inactive':
        return <Error sx={{ color: 'error.main' }} />;
      default:
        return <Info sx={{ color: 'info.main' }} />;
    }
  };

  const getExecutionStatus = (modelId: string) => {
    return executions.find(exec => exec.modelId === modelId);
  };

  const getModelSettings = (modelId: string) => {
    return modelSettings.find(s => s.modelId === modelId);
  };

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Risk Models
        </Typography>
        <LinearProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Risk Models
        </Typography>
        <Button
          variant="outlined"
          startIcon={<Refresh />}
          onClick={fetchModels}
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

      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
        {models.map((model) => {
          const execution = getExecutionStatus(model.id);
          const settings = getModelSettings(model.id);
          
          return (
            <Card key={model.id} sx={{ flex: '1 1 350px', minWidth: '350px' }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Box>
                    <Typography variant="h6" gutterBottom>
                      {model.name}
                    </Typography>
                    <Chip
                      label={model.category}
                      size="small"
                      sx={{ mb: 1 }}
                    />
                  </Box>
                  {getStatusIcon(model.status)}
                </Box>
                
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {model.description}
                </Typography>

                {settings && (
                  <Alert severity="info" sx={{ mb: 2 }}>
                    <Typography variant="body2">
                      <strong>Saved Settings:</strong> {Object.keys(settings.parameters).length} parameters configured
                    </Typography>
                  </Alert>
                )}

                {execution && (
                  <Alert 
                    severity={execution.status === 'completed' ? 'success' : execution.status === 'failed' ? 'error' : 'info'}
                    sx={{ mb: 2 }}
                  >
                    {execution.status === 'running' && 'Model is running...'}
                    {execution.status === 'completed' && 'Execution completed successfully'}
                    {execution.status === 'failed' && execution.error}
                  </Alert>
                )}

                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button
                    variant="contained"
                    startIcon={<PlayArrow />}
                    onClick={() => handleRunModel(model)}
                    disabled={model.status !== 'active' || execution?.status === 'running'}
                    sx={{ flex: 1 }}
                  >
                    Run Model
                  </Button>
                  <Tooltip title="Model Settings & Configuration">
                    <IconButton 
                      size="small"
                      onClick={() => handleSettingsClick(model)}
                      color={settings ? "primary" : "default"}
                    >
                      <Settings />
                    </IconButton>
                  </Tooltip>
                </Box>
              </CardContent>
            </Card>
          );
        })}
      </Box>

      {/* Model Execution Dialog */}
      <Dialog 
        open={executionDialog} 
        onClose={() => setExecutionDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <PlayArrow color="primary" />
            Run Model: {selectedModel?.name}
          </Box>
        </DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Configure parameters for {selectedModel?.name} model execution.
          </Typography>
          
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {selectedModel && renderParameterFields(selectedModel)}
            <Divider sx={{ my: 2 }} />
            <TextField
              label="Time Horizon (years)"
              type="number"
              value={executionParams.time_horizon || 1.0}
              onChange={(e) => setExecutionParams(prev => ({
                ...prev,
                time_horizon: parseFloat(e.target.value)
              }))}
              helperText="Simulation time period in years"
              fullWidth
            />
            <TextField
              label="Number of Simulations"
              type="number"
              value={executionParams.num_simulations || 100}
              onChange={(e) => setExecutionParams(prev => ({
                ...prev,
                num_simulations: parseInt(e.target.value)
              }))}
              helperText="Number of Monte Carlo simulation paths"
              fullWidth
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setExecutionDialog(false)}>
            Cancel
          </Button>
          <Button 
            onClick={handleExecuteModel}
            variant="contained"
            disabled={!selectedModel}
          >
            Execute
          </Button>
        </DialogActions>
      </Dialog>

      {/* Model Settings Dialog */}
      <Dialog 
        open={settingsDialog} 
        onClose={() => setSettingsDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Tune color="primary" />
            Model Settings: {selectedModel?.name}
          </Box>
        </DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Configure default parameters for {selectedModel?.name}.
          </Typography>
          
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {selectedModel && renderParameterFields(selectedModel)}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSettingsDialog(false)}>
            Cancel
          </Button>
          <Button 
            onClick={handleSaveSettings}
            variant="contained"
            startIcon={<Tune />}
            disabled={!selectedModel}
          >
            Save Settings
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Models;
 