#!/bin/bash

# Multi-Repository Migration Script
# Converts monorepo modules to independent Git repositories

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Multi-Repository Migration Script${NC}"
echo "=========================================="
echo

# Define all modules
MODULES=(
    "risk-interest-rate"
    "risk-credit"
    "risk-equity"
    "risk-foreign-exchange"
    "risk-inflation"
    "risk-liquidity"
    "risk-counterparty"
    "radf-aggregation"
    "ai-gateway"
    "backend-api"
    "frontend-dashboard"
    "auth-rbac"
    "deployment-infra"
    "monitoring-dashboard"
    "aggregation-engine"
    "web-frontend"
)

# Create parent directory for independent repositories
PARENT_DIR="../independent-modules"
mkdir -p "$PARENT_DIR"

echo -e "${BLUE}Step 1: Creating independent module repositories...${NC}"
echo

for module in "${MODULES[@]}"; do
    echo -e "${YELLOW}Processing: $module${NC}"
    
    # Create module directory
    MODULE_DIR="$PARENT_DIR/$module"
    mkdir -p "$MODULE_DIR"
    
    # Copy module files (excluding .git)
    if [ -d "$module" ]; then
        echo "  📁 Copying files..."
        cp -r "$module"/* "$MODULE_DIR/" 2>/dev/null || true
        
        # Create .gitignore for the module
        cat > "$MODULE_DIR/.gitignore" << 'EOF'
# Dependencies
node_modules/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env

# Build outputs
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Coverage
coverage/
.coverage
htmlcov/

# Temporary files
*.tmp
*.temp
EOF
        
        # Create README for the module
        cat > "$MODULE_DIR/README.md" << EOF
# $module

## Overview
Independent module for the Gnanam ESG platform.

## Installation
\`\`\`bash
npm install
# or
pip install -r requirements.txt
\`\`\`

## Development
\`\`\`bash
npm run dev
# or
python src/main.py
\`\`\`

## Testing
\`\`\`bash
npm test
# or
python -m pytest
\`\`\`

## Contributing
1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License
Proprietary - Gnanam ESG Platform
EOF
        
        echo -e "  ✅ $module prepared"
    else
        echo -e "  ⚠️  Module $module not found"
    fi
done

echo
echo -e "${BLUE}Step 2: Creating shared libraries repository...${NC}"
echo

# Create shared libraries repository
SHARED_DIR="$PARENT_DIR/shared-libraries"
mkdir -p "$SHARED_DIR"

# Copy shared libraries
if [ -d "../shared-libraries" ]; then
    cp -r "../shared-libraries"/* "$SHARED_DIR/" 2>/dev/null || true
fi

# Create shared libraries README
cat > "$SHARED_DIR/README.md" << 'EOF'
# Shared Libraries

## Overview
Common libraries and utilities shared across all ESG platform modules.

## Structure
- `@gnanam/types` - Common TypeScript types
- `@gnanam/utils` - Shared utilities
- `@gnanam/contracts` - API contracts

## Installation
```bash
npm install
```

## Usage
```typescript
import { RiskModel } from '@gnanam/types';
import { calculateRisk } from '@gnanam/utils';
```

## Publishing
```bash
npm run publish
```

## License
Proprietary - Gnanam ESG Platform
EOF

echo -e "${GREEN}✅ Shared libraries prepared${NC}"

echo
echo -e "${BLUE}Step 3: Creating integration repository...${NC}"
echo

# Create integration repository
INTEGRATION_DIR="$PARENT_DIR/esg-integration"
mkdir -p "$INTEGRATION_DIR"

# Copy integration tests
if [ -d "../integration-tests" ]; then
    cp -r "../integration-tests"/* "$INTEGRATION_DIR/" 2>/dev/null || true
fi

# Create integration README
cat > "$INTEGRATION_DIR/README.md" << 'EOF'
# ESG Platform Integration

## Overview
Integration testing and deployment configuration for the modular ESG platform.

## Structure
- `integration-tests/` - Cross-module integration tests
- `deployment/` - Deployment configurations
- `ci-cd/` - CI/CD pipeline configurations

## Running Integration Tests
```bash
python run_tests.py
```

## Deployment
```bash
./deploy.sh staging
./deploy.sh production
```

## License
Proprietary - Gnanam ESG Platform
EOF

echo -e "${GREEN}✅ Integration repository prepared${NC}"

echo
echo -e "${BLUE}Step 4: Creating migration guide...${NC}"
echo

# Create migration guide
cat > "$PARENT_DIR/MIGRATION_GUIDE.md" << 'EOF'
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
EOF

echo -e "${GREEN}✅ Migration guide created${NC}"

echo
echo -e "${GREEN}🎉 Multi-repository structure created successfully!${NC}"
echo
echo -e "${BLUE}📁 Independent modules created in: $PARENT_DIR${NC}"
echo
echo -e "${YELLOW}📋 Next Steps:${NC}"
echo "1. Review the created structure"
echo "2. Create GitHub repositories for each module"
echo "3. Initialize Git repositories"
echo "4. Set up CI/CD pipelines"
echo "5. Update import statements"
echo
echo -e "${BLUE}📚 See $PARENT_DIR/MIGRATION_GUIDE.md for detailed instructions${NC}" 