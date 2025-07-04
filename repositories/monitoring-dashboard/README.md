# Monitoring Dashboard Module

This module provides the monitoring dashboard service for the Gnanam ESG platform, offering real-time monitoring, visualization, and alerting capabilities for all risk models and system components.

## 🏗️ Architecture

### Core Components
- **Real-time Monitoring**: Live system and risk model monitoring
- **Interactive Dashboards**: Streamlit and Plotly-based visualizations
- **Alerting System**: Configurable alerts and notifications
- **Performance Metrics**: System performance and health monitoring
- **Data Visualization**: Advanced charts and graphs for risk analysis

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
# Start monitoring dashboard
npm run dev

# Or directly with Python
python src/monitoring.py --dev

# Start Streamlit dashboard
npm run dashboard
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

## 📊 Dashboard Features

### Real-time Monitoring
- **System Health**: Service status and performance metrics
- **Risk Model Status**: Individual risk model health and performance
- **Aggregation Engine**: RADF workflow monitoring
- **API Gateway**: Request/response monitoring

### Risk Analytics
- **Portfolio Risk**: Real-time portfolio risk metrics
- **Scenario Analysis**: Multi-risk scenario visualization
- **Stress Testing**: Stress test results and analysis
- **Correlation Analysis**: Risk factor correlation matrices

### Performance Metrics
- **Response Times**: API response time monitoring
- **Throughput**: Request processing rates
- **Error Rates**: Error tracking and analysis
- **Resource Usage**: CPU, memory, and disk usage

### Alerting System
- **Threshold Alerts**: Configurable alert thresholds
- **Anomaly Detection**: Automated anomaly detection
- **Notification Channels**: Email, Slack, webhook notifications
- **Escalation Rules**: Automated escalation procedures

## 📁 Structure

```
monitoring-dashboard/
├── src/
│   ├── monitoring.py         # Core monitoring service
│   ├── dashboard.py          # Streamlit dashboard
│   ├── metrics.py            # Metrics collection
│   ├── alerts.py             # Alerting system
│   ├── visualizations.py     # Chart and graph components
│   └── utils/                # Utility functions
│       ├── data_processor.py
│       └── formatters.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── dashboards/
│   ├── system_health.py
│   ├── risk_analytics.py
│   └── performance.py
├── config/
│   ├── alerts.yaml
│   └── thresholds.yaml
├── package.json
├── requirements.txt
└── README.md
```

## 🔧 Development

### Adding New Dashboards

1. Create dashboard file in `dashboards/`
2. Implement visualization components
3. Add data connectors
4. Update navigation

### Configuration

Environment variables:
```bash
# Dashboard Settings
DASHBOARD_PORT=8501
DASHBOARD_HOST=0.0.0.0

# Monitoring
PROMETHEUS_URL=http://localhost:9090
METRICS_INTERVAL=30

# Alerting
ALERT_WEBHOOK_URL=https://hooks.slack.com/...
ALERT_EMAIL_SMTP=smtp.gmail.com:587

# Database
METRICS_DB_URL=postgresql://user:pass@localhost/metrics
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

## 📈 Visualization Components

### Charts and Graphs
- **Time Series**: Historical trend analysis
- **Heatmaps**: Correlation and risk matrices
- **Scatter Plots**: Risk factor relationships
- **Bar Charts**: Performance comparisons
- **Gauge Charts**: Real-time metrics
- **Network Graphs**: System dependencies

### Interactive Features
- **Filters**: Dynamic data filtering
- **Drill-down**: Hierarchical data exploration
- **Real-time Updates**: Live data refresh
- **Export**: Data export capabilities
- **Sharing**: Dashboard sharing and embedding

## 🔔 Alerting System

### Alert Types
- **Performance Alerts**: Response time thresholds
- **Error Alerts**: Error rate monitoring
- **Resource Alerts**: System resource usage
- **Business Alerts**: Risk metric thresholds
- **Security Alerts**: Security event monitoring

### Notification Channels
- **Email**: SMTP-based email notifications
- **Slack**: Slack webhook integration
- **Webhooks**: Custom webhook endpoints
- **SMS**: Text message notifications
- **PagerDuty**: Incident management integration

## 🚀 Deployment

### Docker
```bash
# Build image
docker build -t gnanam/monitoring-dashboard .

# Run container
docker run -p 8501:8501 gnanam/monitoring-dashboard
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: monitoring-dashboard
spec:
  replicas: 2
  selector:
    matchLabels:
      app: monitoring-dashboard
  template:
    metadata:
      labels:
        app: monitoring-dashboard
    spec:
      containers:
      - name: monitoring-dashboard
        image: gnanam/monitoring-dashboard:latest
        ports:
        - containerPort: 8501
```

## 🔄 Integration

### Data Sources
- **Prometheus**: Metrics collection
- **Risk Models**: Real-time risk data
- **API Gateway**: Request/response data
- **Aggregation Engine**: Workflow data
- **External APIs**: Market data and feeds

### External Services
- **Alerting Services**: PagerDuty, Slack, email
- **Data Lakes**: BigQuery, Snowflake, S3
- **Analytics Platforms**: Grafana, Kibana
- **ML Platforms**: Model monitoring integration

## 📚 References

- Streamlit Documentation: https://docs.streamlit.io/
- Plotly Documentation: https://plotly.com/python/
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