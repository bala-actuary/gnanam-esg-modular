import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  IconButton,
  Tooltip,
  LinearProgress,
} from '@mui/material';
import {
  Add,
  Edit,
  Delete,
  PlayArrow,
  Timeline,
  Settings,
  Visibility,
  Download,
} from '@mui/icons-material';

const Scenarios: React.FC = () => {
  const [scenarios, setScenarios] = useState([
    {
      id: 1,
      name: 'Stress Test 2025',
      description: 'Comprehensive stress testing scenario for 2025',
      status: 'Completed',
      progress: 100,
      models: ['Hull-White One Factor', 'GBM Model', 'Merton Model'],
      startDate: '2025-07-01',
      endDate: '2025-07-01',
      results: 'Available',
    },
    {
      id: 2,
      name: 'Baseline Scenario',
      description: 'Standard baseline economic scenario',
      status: 'Running',
      progress: 65,
      models: ['Hull-White One Factor', 'GBM Model'],
      startDate: '2025-07-02',
      endDate: null,
      results: 'In Progress',
    },
    {
      id: 3,
      name: 'Adverse Economic',
      description: 'Adverse economic conditions scenario',
      status: 'Pending',
      progress: 0,
      models: ['All Models'],
      startDate: null,
      endDate: null,
      results: 'Not Started',
    },
    {
      id: 4,
      name: 'Interest Rate Shock',
      description: 'Interest rate stress testing scenario',
      status: 'Completed',
      progress: 100,
      models: ['Hull-White One Factor'],
      startDate: '2025-06-30',
      endDate: '2025-06-30',
      results: 'Available',
    },
    {
      id: 5,
      name: 'Market Volatility',
      description: 'High market volatility scenario',
      status: 'Completed',
      progress: 100,
      models: ['GBM Model', 'FX GBM Model'],
      startDate: '2025-06-29',
      endDate: '2025-06-29',
      results: 'Available',
    },
    {
      id: 6,
      name: 'Credit Risk Assessment',
      description: 'Comprehensive credit risk evaluation',
      status: 'Completed',
      progress: 100,
      models: ['Merton Model'],
      startDate: '2025-06-28',
      endDate: '2025-06-28',
      results: 'Available',
    },
  ]);

  const [selectedScenario, setSelectedScenario] = useState<any>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogType, setDialogType] = useState<'view' | 'edit' | 'new'>('view');

  const handleViewScenario = (scenario: any) => {
    setSelectedScenario(scenario);
    setDialogType('view');
    setDialogOpen(true);
  };

  const handleEditScenario = (scenario: any) => {
    setSelectedScenario(scenario);
    setDialogType('edit');
    setDialogOpen(true);
  };

  const handleNewScenario = () => {
    setSelectedScenario({
      name: '',
      description: '',
      models: [],
    });
    setDialogType('new');
    setDialogOpen(true);
  };

  const handleRunScenario = (scenarioId: number) => {
    console.log('Running scenario:', scenarioId);
  };

  const handleDeleteScenario = (scenarioId: number) => {
    setScenarios(scenarios.filter(scenario => scenario.id !== scenarioId));
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Completed': return 'success';
      case 'Running': return 'warning';
      case 'Pending': return 'default';
      case 'Failed': return 'error';
      default: return 'default';
    }
  };

  const getProgressColor = (progress: number) => {
    if (progress === 100) return 'success';
    if (progress > 50) return 'warning';
    return 'primary';
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
          Scenarios
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={handleNewScenario}
        >
          New Scenario
        </Button>
      </Box>

      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3 }}>
        {scenarios.map((scenario) => (
          <Box key={scenario.id} sx={{ flex: '1 1 500px', minWidth: 500 }}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Box>
                    <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
                      {scenario.name}
                    </Typography>
                    <Chip
                      label={scenario.status}
                      size="small"
                      color={getStatusColor(scenario.status) as any}
                    />
                  </Box>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Tooltip title="View Details">
                      <IconButton
                        size="small"
                        onClick={() => handleViewScenario(scenario)}
                      >
                        <Visibility />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Edit Scenario">
                      <IconButton
                        size="small"
                        onClick={() => handleEditScenario(scenario)}
                      >
                        <Edit />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Delete Scenario">
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => handleDeleteScenario(scenario.id)}
                      >
                        <Delete />
                      </IconButton>
                    </Tooltip>
                  </Box>
                </Box>

                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {scenario.description}
                </Typography>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    Progress: {scenario.progress}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={scenario.progress}
                    color={getProgressColor(scenario.progress) as any}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>

                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                  {scenario.models.map((model) => (
                    <Chip
                      key={model}
                      label={model}
                      size="small"
                      variant="outlined"
                    />
                  ))}
                </Box>

                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    {scenario.startDate ? `Started: ${scenario.startDate}` : 'Not started'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Results: {scenario.results}
                  </Typography>
                </Box>

                <Box sx={{ display: 'flex', gap: 1 }}>
                  {scenario.status === 'Completed' ? (
                    <>
                      <Button
                        variant="contained"
                        size="small"
                        startIcon={<Download />}
                        sx={{ flex: 1 }}
                      >
                        Download Results
                      </Button>
                      <Button
                        variant="outlined"
                        size="small"
                        startIcon={<Timeline />}
                      >
                        View Report
                      </Button>
                    </>
                  ) : scenario.status === 'Running' ? (
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<Timeline />}
                      sx={{ flex: 1 }}
                    >
                      Monitor Progress
                    </Button>
                  ) : (
                    <Button
                      variant="contained"
                      size="small"
                      startIcon={<PlayArrow />}
                      onClick={() => handleRunScenario(scenario.id)}
                      sx={{ flex: 1 }}
                    >
                      Start Scenario
                    </Button>
                  )}
                  <Button
                    variant="outlined"
                    size="small"
                    startIcon={<Settings />}
                  >
                    Configure
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Box>
        ))}
      </Box>

      {/* Scenario Details Dialog */}
      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {dialogType === 'new' ? 'Create New Scenario' :
           dialogType === 'edit' ? 'Edit Scenario' : 'Scenario Details'}
        </DialogTitle>
        <DialogContent>
          {selectedScenario && (
            <Box sx={{ mt: 2 }}>
              {dialogType === 'view' ? (
                <Box>
                  <Typography variant="h6" sx={{ mb: 2 }}>{selectedScenario.name}</Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {selectedScenario.description}
                  </Typography>
                  
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, mb: 2 }}>
                    <Box>
                      <Typography variant="body2" color="text.secondary">Status</Typography>
                      <Typography variant="body1">{selectedScenario.status}</Typography>
                    </Box>
                    <Box>
                      <Typography variant="body2" color="text.secondary">Progress</Typography>
                      <Typography variant="body1">{selectedScenario.progress}%</Typography>
                    </Box>
                    <Box>
                      <Typography variant="body2" color="text.secondary">Start Date</Typography>
                      <Typography variant="body1">{selectedScenario.startDate || 'Not started'}</Typography>
                    </Box>
                    <Box>
                      <Typography variant="body2" color="text.secondary">End Date</Typography>
                      <Typography variant="body1">{selectedScenario.endDate || 'Not completed'}</Typography>
                    </Box>
                    <Box>
                      <Typography variant="body2" color="text.secondary">Results</Typography>
                      <Typography variant="body1">{selectedScenario.results}</Typography>
                    </Box>
                  </Box>

                  <Typography variant="subtitle1" sx={{ mb: 1 }}>Models:</Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {selectedScenario.models.map((model: string) => (
                      <Chip
                        key={model}
                        label={model}
                        size="small"
                        variant="outlined"
                      />
                    ))}
                  </Box>
                </Box>
              ) : (
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  <TextField
                    fullWidth
                    label="Scenario Name"
                    value={selectedScenario.name}
                    onChange={(e) => setSelectedScenario({ ...selectedScenario, name: e.target.value })}
                  />
                  <TextField
                    fullWidth
                    multiline
                    rows={3}
                    label="Description"
                    value={selectedScenario.description}
                    onChange={(e) => setSelectedScenario({ ...selectedScenario, description: e.target.value })}
                  />
                  <FormControl fullWidth>
                    <InputLabel>Models</InputLabel>
                    <Select
                      multiple
                      value={selectedScenario.models}
                      label="Models"
                      onChange={(e) => setSelectedScenario({ ...selectedScenario, models: e.target.value })}
                    >
                      <MenuItem value="Hull-White One Factor">Hull-White One Factor</MenuItem>
                      <MenuItem value="GBM Model">GBM Model</MenuItem>
                      <MenuItem value="Merton Model">Merton Model</MenuItem>
                      <MenuItem value="FX GBM Model">FX GBM Model</MenuItem>
                      <MenuItem value="Inflation Model">Inflation Model</MenuItem>
                      <MenuItem value="Liquidity Model">Liquidity Model</MenuItem>
                      <MenuItem value="All Models">All Models</MenuItem>
                    </Select>
                  </FormControl>
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>
            {dialogType === 'view' ? 'Close' : 'Cancel'}
          </Button>
          {(dialogType === 'edit' || dialogType === 'new') && (
            <Button variant="contained" onClick={() => setDialogOpen(false)}>
              {dialogType === 'new' ? 'Create' : 'Save'}
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Scenarios; 