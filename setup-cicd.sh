#!/bin/bash

# ESG Platform CI/CD Setup Script
# This script helps you set up the CI/CD pipeline step by step

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 ESG Platform CI/CD Setup${NC}"
echo "=================================="
echo

# Check if we're in the right directory
if [[ ! -f "package.json" ]] || [[ ! -d ".github/workflows" ]]; then
    echo -e "${RED}❌ Error: Please run this script from the Gnanam_ESG directory${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Found ESG platform files${NC}"
echo

# Step 1: Check Git status
echo -e "${BLUE}Step 1: Checking Git status...${NC}"
if [[ -n $(git status --porcelain) ]]; then
    echo -e "${YELLOW}⚠️  You have uncommitted changes. Committing them...${NC}"
    git add .
    git commit -m "feat: Add CI/CD pipeline setup"
    echo -e "${GREEN}✅ Changes committed${NC}"
else
    echo -e "${GREEN}✅ No uncommitted changes${NC}"
fi
echo

# Step 2: Check remote
echo -e "${BLUE}Step 2: Checking Git remote...${NC}"
if git remote get-url origin > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Remote origin already configured${NC}"
    echo "Remote URL: $(git remote get-url origin)"
else
    echo -e "${YELLOW}⚠️  No remote origin configured${NC}"
    echo
    echo -e "${BLUE}📋 Manual Setup Required:${NC}"
    echo "1. Go to https://github.com/new"
    echo "2. Create repository: gnanam-esg-modular"
    echo "3. Make it Public"
    echo "4. Don't initialize with README, .gitignore, or license"
    echo
    read -p "Enter your GitHub username: " github_username
    if [[ -n "$github_username" ]]; then
        echo -e "${BLUE}Adding remote origin...${NC}"
        git remote add origin "https://github.com/$github_username/gnanam-esg-modular.git"
        echo -e "${GREEN}✅ Remote origin added${NC}"
    else
        echo -e "${RED}❌ No username provided. Please run the script again.${NC}"
        exit 1
    fi
fi
echo

# Step 3: Push to GitHub
echo -e "${BLUE}Step 3: Pushing to GitHub...${NC}"
if git push -u origin main; then
    echo -e "${GREEN}✅ Successfully pushed to GitHub${NC}"
else
    echo -e "${RED}❌ Failed to push to GitHub${NC}"
    echo "Please check your GitHub credentials and try again."
    exit 1
fi
echo

# Step 4: Set up GitHub Environments
echo -e "${BLUE}Step 4: Setting up GitHub Environments...${NC}"
echo -e "${YELLOW}📋 Manual Setup Required:${NC}"
echo "1. Go to your repository on GitHub"
echo "2. Go to Settings > Environments"
echo "3. Create environments: staging, production"
echo "4. Add protection rules if needed"
echo

# Step 5: Set up GitHub Secrets
echo -e "${BLUE}Step 5: Setting up GitHub Secrets...${NC}"
echo -e "${YELLOW}📋 Manual Setup Required:${NC}"
echo "Go to Settings > Secrets and variables > Actions"
echo "Add the following secrets:"
echo
echo "Required for basic functionality:"
echo "- DOCKER_REGISTRY_TOKEN (if using private registry)"
echo "- SLACK_WEBHOOK_URL (for notifications)"
echo
echo "Required for production deployment:"
echo "- KUBECONFIG_PROD (if using Kubernetes)"
echo "- AWS_ACCESS_KEY_ID (if using AWS)"
echo "- AWS_SECRET_ACCESS_KEY (if using AWS)"
echo

# Step 6: Test the pipeline
echo -e "${BLUE}Step 6: Testing the pipeline...${NC}"
echo -e "${GREEN}✅ Your CI/CD pipeline is now set up!${NC}"
echo
echo "To test the pipeline:"
echo "1. Make a small change to any file"
echo "2. Commit and push:"
echo "   git add . && git commit -m 'test: Test CI/CD pipeline' && git push"
echo "3. Go to Actions tab on GitHub to see the workflow run"
echo

# Step 7: Next steps
echo -e "${BLUE}Step 7: Next Steps${NC}"
echo "1. Set up your deployment infrastructure (Docker, Kubernetes, etc.)"
echo "2. Configure environment-specific settings"
echo "3. Set up monitoring and alerting"
echo "4. Test deployments in staging environment"
echo "5. Configure production deployment"
echo

echo -e "${GREEN}🎉 Setup complete! Your ESG platform CI/CD pipeline is ready.${NC}"
echo
echo -e "${BLUE}📚 Documentation:${NC}"
echo "- CI/CD Pipeline: docs/ci-cd-pipeline.md"
echo "- Deployment: scripts/deployment/"
echo "- Health Checks: scripts/deployment/health-check.sh"
echo
echo -e "${BLUE}🛠️  Useful Commands:${NC}"
echo "- Check deployment status: ./scripts/deployment/deploy.sh status -e staging"
echo "- Run health checks: ./scripts/deployment/health-check.sh -e staging"
echo "- View logs: ./scripts/deployment/deploy.sh logs -e staging" 