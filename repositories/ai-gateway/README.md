# AI Gateway Module

This module provides the AI/ML orchestration gateway service for the Gnanam ESG platform, offering comprehensive AI model management, workflow automation, and intelligent risk analysis capabilities.

## 🏗️ Architecture

### Core Components
- **AI Model Management**: Centralized model registry and configuration
- **Workflow Orchestration**: Automated multi-step AI/ML pipelines
- **Task Queue Management**: Celery-based task execution and monitoring
- **LLM Integration**: OpenAI, Anthropic, and custom LLM support
- **ML Model Orchestration**: Classification, regression, and anomaly detection
- **Cost Tracking**: Real-time model usage and cost monitoring
- **Performance Monitoring**: Task execution metrics and optimization

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

### Development

```bash
# Start AI Gateway service
npm run dev

# Or directly with Python
python src/ai_gateway.py --dev

# Start workflow orchestrator
npm run orchestrate
```

### Production

```bash
# Start production server
npm start

# Build and deploy with Docker
npm run build
npm run deploy
```

## 🧪 Testing

```bash
# Run all tests
npm run test

# Run unit tests only
npm run test:unit

# Run integration tests
npm run test:integration

# Run with coverage
npm run test:coverage
```

## 🤖 AI Capabilities

### LLM Integration
- **OpenAI Models**: GPT-4, GPT-3.5 Turbo integration
- **Anthropic Models**: Claude 3 Sonnet, Claude 3 Haiku
- **Custom Models**: Local and custom LLM support
- **Cost Optimization**: Token usage tracking and cost management
- **Prompt Engineering**: Structured prompt templates and validation

### Machine Learning Models
- **Classification**: Risk level classification models
- **Regression**: Price prediction and forecasting models
- **Anomaly Detection**: Market anomaly and fraud detection
- **Time Series**: Temporal pattern analysis and prediction
- **Clustering**: Portfolio segmentation and grouping

### Workflow Automation
- **Multi-step Pipelines**: Complex AI/ML workflow orchestration
- **Dependency Management**: Step dependencies and execution order
- **Error Handling**: Robust error handling and retry mechanisms
- **Progress Tracking**: Real-time workflow progress monitoring
- **Result Aggregation**: Automated result collection and formatting

## 📁 Structure

```
ai-gateway/
├── src/
│   ├── ai_gateway.py         # Main AI Gateway service
│   ├── orchestrator.py       # Workflow orchestration
│   ├── index.py              # Module entry point
│   ├── models/               # AI model implementations
│   │   ├── llm_models.py
│   │   ├── ml_models.py
│   │   └── custom_models.py
│   ├── workflows/            # Workflow definitions
│   │   ├── risk_analysis.py
│   │   ├── scenario_gen.py
│   │   └── model_training.py
│   ├── tasks/                # Celery task definitions
│   │   ├── llm_tasks.py
│   │   ├── ml_tasks.py
│   │   └── workflow_tasks.py
│   └── utils/                # Utility functions
│       ├── cost_tracker.py
│       ├── model_registry.py
│       └── validators.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── config/
│   ├── models.yaml
│   ├── workflows.yaml
│   └── providers.yaml
├── package.json
├── requirements.txt
└── README.md
```

## 🔧 Development

### Adding New Models

1. Create model implementation in `src/models/`
2. Add model configuration in `config/models.yaml`
3. Register model in model registry
4. Add tests and documentation

### Creating Workflows

1. Define workflow in `src/workflows/`
2. Add workflow configuration
3. Create Celery tasks
4. Test workflow execution

### Configuration

Environment variables:
```bash
# AI Service Configuration
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
AI_GATEWAY_PORT=8001

# Task Queue
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Monitoring
PROMETHEUS_URL=http://localhost:9090
METRICS_INTERVAL=30

# Cost Tracking
COST_ALERT_THRESHOLD=100
COST_TRACKING_ENABLED=true
```

### Code Quality

```bash
# Format code
npm run format

# Lint code
npm run lint

# Type checking
mypy src/
```

## 🔄 API Integration

### REST API Endpoints

```python
# Create AI task
POST /tasks
{
    "task_type": "llm_analysis",
    "model_config": {
        "name": "gpt-4",
        "provider": "openai",
        "parameters": {"temperature": 0.7}
    },
    "input_data": {
        "prompt": "Analyze the risk profile of this portfolio"
    }
}

# Get task status
GET /tasks/{task_id}

# Execute LLM task directly
POST /execute/llm
{
    "model_config": {...},
    "input_data": {...}
}

# Execute ML task directly
POST /execute/ml
{
    "model_config": {...},
    "input_data": {...}
}
```

### WebSocket Events

```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8001/ws');

// Listen for events
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    switch(data.type) {
        case 'task_started':
            console.log('Task started:', data.task_id);
            break;
        case 'task_completed':
            console.log('Task completed:', data.result);
            break;
        case 'workflow_progress':
            console.log('Workflow progress:', data.progress);
            break;
    }
};
```

### Webhook Integration

```python
# Configure webhook endpoint
WEBHOOK_URL = "https://your-service.com/webhooks"

# Webhook events
{
    "event": "task_completion",
    "task_id": "task_123",
    "result": {...},
    "timestamp": "2024-01-01T12:00:00Z"
}
```

## 📊 Workflow Examples

### Risk Analysis Workflow

```python
# Risk analysis workflow definition
workflow = {
    "workflow_id": "risk_analysis",
    "name": "Risk Analysis Workflow",
    "steps": [
        {
            "step_id": "data_prep",
            "task_type": "data_preprocessing",
            "input_mapping": {"data": "input.market_data"},
            "output_mapping": {"processed_data": "processed_data"}
        },
        {
            "step_id": "anomaly_check",
            "task_type": "anomaly_detection",
            "input_mapping": {"data": "step.data_prep.processed_data"},
            "dependencies": ["data_prep"]
        },
        {
            "step_id": "risk_classify",
            "task_type": "risk_classification",
            "input_mapping": {"features": "step.data_prep.processed_data"},
            "dependencies": ["data_prep"]
        },
        {
            "step_id": "llm_analysis",
            "task_type": "llm_analysis",
            "input_mapping": {"prompt": "input.analysis_prompt"},
            "dependencies": ["anomaly_check", "risk_classify"]
        }
    ]
}
```

### Scenario Generation Workflow

```python
# Scenario generation workflow
scenario_workflow = {
    "workflow_id": "scenario_generation",
    "name": "Scenario Generation Workflow",
    "steps": [
        {
            "step_id": "market_analysis",
            "task_type": "data_analysis",
            "input_mapping": {"market_data": "input.market_data"}
        },
        {
            "step_id": "scenario_gen",
            "task_type": "scenario_generation",
            "input_mapping": {"analysis": "step.market_analysis.result"},
            "dependencies": ["market_analysis"]
        },
        {
            "step_id": "risk_assessment",
            "task_type": "risk_assessment",
            "input_mapping": {"scenarios": "step.scenario_gen.scenarios"},
            "dependencies": ["scenario_gen"]
        }
    ]
}
```

## 💰 Cost Management

### Cost Tracking

```python
# Track model usage costs
cost_tracker = CostTracker()

# Record LLM usage
cost_tracker.record_llm_usage(
    model="gpt-4",
    tokens_used=1000,
    cost=0.03
)

# Record ML model usage
cost_tracker.record_ml_usage(
    model="risk-classifier",
    inference_time=0.5,
    cost=0.001
)

# Get cost summary
summary = cost_tracker.get_cost_summary()
print(f"Total cost: ${summary['total_cost']}")
```

### Cost Optimization

- **Model Selection**: Automatic model selection based on cost/performance
- **Token Optimization**: Prompt optimization to reduce token usage
- **Batch Processing**: Batch requests to reduce API calls
- **Caching**: Result caching to avoid redundant computations
- **Budget Limits**: Configurable budget limits and alerts

## 🔐 Security

### API Security

- **Authentication**: JWT-based authentication
- **Authorization**: Role-based access control
- **Rate Limiting**: API rate limiting and throttling
- **Input Validation**: Comprehensive input validation and sanitization
- **Audit Logging**: Complete audit trail of all operations

### Model Security

- **Model Validation**: Input/output validation for all models
- **Bias Detection**: Automated bias detection and mitigation
- **Explainability**: Model explainability and interpretability
- **Version Control**: Model versioning and rollback capabilities
- **Access Control**: Fine-grained model access permissions

## 🚀 Deployment

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

EXPOSE 8001
CMD ["python", "src/ai_gateway.py"]
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-gateway
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-gateway
  template:
    metadata:
      labels:
        app: ai-gateway
    spec:
      containers:
      - name: ai-gateway
        image: gnanam/ai-gateway:latest
        ports:
        - containerPort: 8001
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-secrets
              key: openai-key
```

## 🔄 Integration

### External Services
- **Risk Models**: Integration with all risk model modules
- **Monitoring**: Integration with monitoring dashboard
- **API Gateway**: Integration with main API gateway
- **Data Sources**: Market data and external data feeds
- **Notification Service**: Alert and notification integration

### Model Providers
- **OpenAI**: GPT-4, GPT-3.5 Turbo
- **Anthropic**: Claude 3 Sonnet, Claude 3 Haiku
- **Local Models**: Custom trained models
- **Cloud Providers**: AWS SageMaker, Azure ML, GCP AI Platform

## 📚 References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Celery Documentation: https://docs.celeryproject.org/
- OpenAI API: https://platform.openai.com/docs/
- Anthropic API: https://docs.anthropic.com/
- Redis Documentation: https://redis.io/documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## 📄 License

This module is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 