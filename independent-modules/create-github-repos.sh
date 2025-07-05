#!/bin/bash

# GitHub Repository Creation Script
# Creates GitHub repositories for all independent modules

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 GitHub Repository Creation Script${NC}"
echo "=========================================="
echo

# Get GitHub username from command line argument
GITHUB_USERNAME="$1"

if [[ -z "$GITHUB_USERNAME" ]]; then
    echo -e "${RED}❌ Usage: $0 <github_username>${NC}"
    echo -e "${YELLOW}Example: $0 your-username${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Using GitHub username: $GITHUB_USERNAME${NC}"
echo

# Define all modules with descriptions
declare -A MODULES=(
    ["risk-interest-rate"]="ESG Interest Rate Risk Models"
    ["risk-credit"]="ESG Credit Risk Models"
    ["risk-equity"]="ESG Equity Risk Models"
    ["risk-foreign-exchange"]="ESG Foreign Exchange Risk Models"
    ["risk-inflation"]="ESG Inflation Risk Models"
    ["risk-liquidity"]="ESG Liquidity Risk Models"
    ["risk-counterparty"]="ESG Counterparty Risk Models"
    ["radf-aggregation"]="ESG Risk Aggregation Framework"
    ["ai-gateway"]="ESG AI Model Orchestration"
    ["backend-api"]="ESG Backend API Services"
    ["frontend-dashboard"]="ESG Frontend Dashboard"
    ["auth-rbac"]="ESG Authentication & RBAC"
    ["deployment-infra"]="ESG Deployment Infrastructure"
    ["monitoring-dashboard"]="ESG Monitoring Dashboard"
    ["aggregation-engine"]="ESG Data Aggregation Engine"
    ["web-frontend"]="ESG Web Frontend"
    ["shared-libraries"]="ESG Shared Libraries"
    ["esg-integration"]="ESG Platform Integration"
)

echo -e "${BLUE}Step 1: Creating GitHub repositories...${NC}"
echo

# Create repositories
for module in "${!MODULES[@]}"; do
    description="${MODULES[$module]}"
    
    echo -e "${YELLOW}Creating: $module${NC}"
    echo "  Description: $description"
    
    # Check if repository already exists
    if gh repo view "$GITHUB_USERNAME/$module" >/dev/null 2>&1; then
        echo -e "  ⚠️  Repository already exists, skipping..."
    else
        # Create repository
        if gh repo create "$GITHUB_USERNAME/$module" \
            --private \
            --description "$description" \
            --source . \
            --remote origin \
            --push; then
            echo -e "  ✅ Repository created successfully"
        else
            echo -e "  ❌ Failed to create repository"
        fi
    fi
    echo
done

echo -e "${BLUE}Step 2: Setting up individual module repositories...${NC}"
echo

# Setup each module repository
for module in "${!MODULES[@]}"; do
    if [[ -d "$module" ]]; then
        echo -e "${YELLOW}Setting up: $module${NC}"
        
        cd "$module"
        
        # Initialize git if not already done
        if [[ ! -d ".git" ]]; then
            git init
        fi
        
        # Add remote origin
        git remote add origin "https://github.com/$GITHUB_USERNAME/$module.git" 2>/dev/null || true
        
        # Add all files
        git add .
        
        # Commit if there are changes
        if [[ -n $(git status --porcelain) ]]; then
            git commit -m "Initial commit: $module module"
            
            # Push to GitHub
            if git push -u origin main; then
                echo -e "  ✅ Pushed to GitHub successfully"
            else
                echo -e "  ⚠️  Push failed (repository might not exist yet)"
            fi
        else
            echo -e "  ℹ️  No changes to commit"
        fi
        
        cd ..
        echo
    fi
done

echo -e "${BLUE}Step 3: Creating organization structure...${NC}"
echo

# Create organization structure file
cat > "ORGANIZATION_STRUCTURE.md" << EOF
# ESG Platform Organization Structure

## GitHub Organization: $GITHUB_USERNAME

### Risk Model Repositories
- \`$GITHUB_USERNAME/risk-interest-rate\` - Interest rate risk models
- \`$GITHUB_USERNAME/risk-credit\` - Credit risk models
- \`$GITHUB_USERNAME/risk-equity\` - Equity risk models
- \`$GITHUB_USERNAME/risk-foreign-exchange\` - Foreign exchange risk models
- \`$GITHUB_USERNAME/risk-inflation\` - Inflation risk models
- \`$GITHUB_USERNAME/risk-liquidity\` - Liquidity risk models
- \`$GITHUB_USERNAME/risk-counterparty\` - Counterparty risk models

### Core Service Repositories
- \`$GITHUB_USERNAME/radf-aggregation\` - Risk aggregation framework
- \`$GITHUB_USERNAME/ai-gateway\` - AI model orchestration
- \`$GITHUB_USERNAME/backend-api\` - Core API services
- \`$GITHUB_USERNAME/frontend-dashboard\` - User interface
- \`$GITHUB_USERNAME/auth-rbac\` - Authentication & authorization
- \`$GITHUB_USERNAME/deployment-infra\` - Production deployment
- \`$GITHUB_USERNAME/monitoring-dashboard\` - Monitoring and observability
- \`$GITHUB_USERNAME/aggregation-engine\` - Data aggregation engine
- \`$GITHUB_USERNAME/web-frontend\` - Web frontend

### Shared Resource Repositories
- \`$GITHUB_USERNAME/shared-libraries\` - Common libraries and utilities
- \`$GITHUB_USERNAME/esg-integration\` - Integration testing and deployment

## Development Workflow

### For Each Module:
1. Clone the specific module repository
2. Create a feature branch
3. Make changes
4. Run tests
5. Create pull request
6. Merge to main

### LLM Memory Management:
- Work on one module at a time
- Each repository has focused context
- AI assistance is specialized per domain

## Benefits Achieved:
- ✅ **LLM Memory Management**: Each repository has focused context
- ✅ **Independent Development**: Teams can work on modules in parallel
- ✅ **Scalability**: Easy to add new risk models
- ✅ **Professional SDLC**: Industry-standard microservices approach

EOF

echo -e "${GREEN}✅ Organization structure documented${NC}"

echo
echo -e "${GREEN}🎉 Multi-repository setup completed!${NC}"
echo
echo -e "${BLUE}📁 Independent modules ready in: $(pwd)${NC}"
echo
echo -e "${YELLOW}📋 Next Steps:${NC}"
echo "1. Review the created repositories on GitHub"
echo "2. Set up CI/CD pipelines for each module"
echo "3. Configure branch protection rules"
echo "4. Set up integration testing"
echo "5. Begin development with focused LLM context"
echo
echo -e "${BLUE}📚 See ORGANIZATION_STRUCTURE.md for repository overview${NC}"
echo -e "${BLUE}📚 See MIGRATION_GUIDE.md for detailed instructions${NC}" 