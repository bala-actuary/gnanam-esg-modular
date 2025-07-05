#!/bin/bash

# Setup First Repository Script
# Uses existing Git setup without GitHub CLI

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 First Repository Setup Script${NC}"
echo "====================================="
echo

echo -e "${YELLOW}Step 1: Create GitHub Repository${NC}"
echo "Please go to https://github.com/new and create:"
echo "  Repository Name: risk-interest-rate"
echo "  Description: ESG Interest Rate Risk Models"
echo "  Visibility: Private"
echo "  Don't initialize with README, .gitignore, or license"
echo

read -p "Press Enter after you've created the repository..."

echo -e "${YELLOW}Step 2: Setting up local repository...${NC}"

# Navigate to the first module
cd risk-interest-rate

# Initialize git if not already done
if [[ ! -d ".git" ]]; then
    echo "  📁 Initializing Git repository..."
    git init
fi

# Add remote origin
echo "  🔗 Adding remote origin..."
git remote add origin https://github.com/bala-actuary/risk-interest-rate.git 2>/dev/null || echo "  ℹ️  Remote already exists"

# Add all files
echo "  📝 Adding files..."
git add .

# Commit if there are changes
if [[ -n $(git status --porcelain) ]]; then
    echo "  💾 Committing changes..."
    git commit -m "Initial commit: risk-interest-rate module"
    
    # Push to GitHub
    echo "  🚀 Pushing to GitHub..."
    if git push -u origin main; then
        echo -e "  ${GREEN}✅ Successfully pushed to GitHub!${NC}"
    else
        echo -e "  ${RED}❌ Push failed. Please check your GitHub credentials.${NC}"
        echo "  You may need to authenticate with GitHub in your terminal."
    fi
else
    echo -e "  ℹ️  No changes to commit"
fi

cd ..

echo
echo -e "${GREEN}🎉 First repository setup complete!${NC}"
echo
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Verify the repository at: https://github.com/bala-actuary/risk-interest-rate"
echo "2. Repeat this process for the remaining 17 modules"
echo "3. Or run the automated script once GitHub CLI is working"
echo
echo -e "${YELLOW}💡 Tip: You can use Cursor's Source Control to push changes!${NC}" 