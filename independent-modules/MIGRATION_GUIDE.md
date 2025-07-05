# Multi-Repository Migration Guide

## Overview
This directory contains independent module repositories for the Gnanam ESG platform.

## Module Repositories

### Risk Models
- `risk-interest-rate/` - Interest rate risk models
- `risk-credit/` - Credit risk models
- `risk-equity/` - Equity risk models
- `risk-foreign-exchange/` - Foreign exchange risk models
- `risk-inflation/` - Inflation risk models
- `risk-liquidity/` - Liquidity risk models
- `risk-counterparty/` - Counterparty risk models

### Core Services
- `radf-aggregation/` - Risk aggregation framework
- `ai-gateway/` - AI model orchestration
- `backend-api/` - Core API services
- `frontend-dashboard/` - User interface
- `auth-rbac/` - Authentication & authorization
- `deployment-infra/` - Production deployment
- `monitoring-dashboard/` - Monitoring and observability
- `aggregation-engine/` - Data aggregation engine
- `web-frontend/` - Web frontend

### Shared Resources
- `shared-libraries/` - Common libraries and utilities
- `esg-integration/` - Integration testing and deployment

## Next Steps

### 1. Create GitHub Repositories
```bash
# For each module, create a GitHub repository
gh repo create gnanam/risk-interest-rate --private
gh repo create gnanam/risk-credit --private
# ... repeat for all modules
```

### 2. Initialize Git Repositories
```bash
cd risk-interest-rate
git init
git remote add origin https://github.com/gnanam/risk-interest-rate.git
git add .
git commit -m "Initial commit: risk-interest-rate module"
git push -u origin main
```

### 3. Set Up CI/CD
Each module should have its own CI/CD pipeline configured.

### 4. Update Dependencies
Update import statements to use shared libraries.

## Benefits
- **LLM Memory Management**: Each repository has focused context
- **Independent Development**: Teams can work on modules in parallel
- **Scalability**: Easy to add new risk models
- **Professional SDLC**: Industry-standard microservices approach

## License
Proprietary - Gnanam ESG Platform
