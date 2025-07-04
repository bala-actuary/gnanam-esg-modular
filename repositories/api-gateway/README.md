# API Gateway Module

This module provides the main API Gateway service for the Gnanam ESG platform, serving as the entry point for all client requests and orchestrating communication between microservices.

## 🏗️ Architecture

### Core Components
- **FastAPI Application**: High-performance async web framework
- **Request Routing**: Intelligent routing to appropriate microservices
- **Authentication & Authorization**: JWT-based security
- **Rate Limiting**: Request throttling and protection
- **Load Balancing**: Distribution of requests across services
- **Monitoring & Logging**: Prometheus metrics and structured logging

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
# Start development server
npm run dev

# Or directly with uvicorn
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
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

## 📊 API Endpoints

### Health & Status
- `GET /health` - Service health check
- `GET /status` - Detailed service status
- `GET /metrics` - Prometheus metrics

### Risk Model APIs
- `POST /api/v1/risk/interest-rate/simulate` - Interest rate simulation
- `POST /api/v1/risk/credit/calculate` - Credit risk calculation
- `POST /api/v1/risk/equity/simulate` - Equity risk simulation
- `POST /api/v1/risk/fx/simulate` - Foreign exchange simulation
- `POST /api/v1/risk/inflation/simulate` - Inflation risk simulation
- `POST /api/v1/risk/liquidity/analyze` - Liquidity risk analysis
- `POST /api/v1/risk/counterparty/exposure` - Counterparty exposure

### Aggregation APIs
- `POST /api/v1/aggregate/scenario` - Multi-risk scenario aggregation
- `GET /api/v1/aggregate/results/{scenario_id}` - Get aggregation results

### AI Integration
- `POST /api/v1/ai/analyze` - AI-powered risk analysis
- `POST /api/v1/ai/optimize` - Portfolio optimization
- `POST /api/v1/ai/forecast` - Risk forecasting

## 📁 Structure

```
api-gateway/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection and models
│   ├── middleware/          # Custom middleware
│   │   ├── auth.py
│   │   ├── logging.py
│   │   └── rate_limit.py
│   ├── routes/              # API route handlers
│   │   ├── health.py
│   │   ├── risk_models.py
│   │   ├── aggregation.py
│   │   └── ai_integration.py
│   ├── services/            # Business logic services
│   │   ├── risk_service.py
│   │   ├── aggregation_service.py
│   │   └── ai_service.py
│   └── utils/               # Utility functions
│       ├── validators.py
│       └── helpers.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── package.json
├── requirements.txt
└── README.md
```

## 🔧 Development

### Adding New Endpoints

1. Create route handler in `src/routes/`
2. Add business logic in `src/services/`
3. Update API documentation
4. Add tests in `tests/`

### Configuration

Environment variables:
```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/gnanam

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256

# Services
RISK_SERVICE_URL=http://localhost:8001
AGGREGATION_SERVICE_URL=http://localhost:8002
AI_SERVICE_URL=http://localhost:8003

# Monitoring
PROMETHEUS_PORT=9090
LOG_LEVEL=INFO
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

## 🔒 Security

### Authentication
- JWT-based token authentication
- Role-based access control (RBAC)
- API key management for external clients

### Rate Limiting
- Per-client rate limiting
- Burst protection
- DDoS mitigation

### Data Validation
- Request/response validation with Pydantic
- Input sanitization
- SQL injection prevention

## 📈 Monitoring & Observability

### Metrics
- Request/response times
- Error rates
- Throughput
- Service health

### Logging
- Structured logging with structlog
- Request tracing
- Error tracking

### Health Checks
- Service health endpoints
- Dependency health monitoring
- Circuit breaker patterns

## 🚀 Deployment

### Docker
```bash
# Build image
docker build -t gnanam/api-gateway .

# Run container
docker run -p 8000:8000 gnanam/api-gateway
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
    spec:
      containers:
      - name: api-gateway
        image: gnanam/api-gateway:latest
        ports:
        - containerPort: 8000
```

## 🔄 Integration

### Microservices Communication
- HTTP/REST APIs
- gRPC for high-performance calls
- Message queues for async operations

### External Services
- Risk model microservices
- Aggregation engine
- AI/ML services
- Monitoring dashboard

## 📚 References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Uvicorn Documentation: https://www.uvicorn.org/
- Prometheus Client: https://prometheus.io/docs/guides/python/
- Structlog: https://www.structlog.org/

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## 📄 License

This module is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 