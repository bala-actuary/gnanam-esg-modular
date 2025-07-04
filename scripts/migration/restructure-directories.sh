#!/bin/bash

# 🏗️ DIRECTORY RESTRUCTURING SCRIPT
# This script automates the migration from monolithic to modular architecture
# Usage: ./restructure-directories.sh

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CURRENT_ROOT="$(pwd)"
MONOLITHIC_SOURCE="../../Risk_Management"
MONOLITHIC_TARGET="../Monolithic_ESG"
MODULAR_TARGET="."

echo -e "${BLUE}🏗️  ESG PROJECT DIRECTORY RESTRUCTURING${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

# Function to print status messages
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Function to create backup
create_backup() {
    print_info "Creating backup of current state..."
    
    BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    if [ -d "$MONOLITHIC_SOURCE" ]; then
        print_info "Backing up monolithic source..."
        cp -r "$MONOLITHIC_SOURCE" "$BACKUP_DIR/"
    fi
    
    if [ -d "$MODULAR_TARGET" ]; then
        print_info "Backing up modular target..."
        cp -r "$MODULAR_TARGET" "$BACKUP_DIR/"
    fi
    
    print_status "Backup created in: $BACKUP_DIR"
}

# Function to create directory structure
create_directory_structure() {
    print_info "Creating new directory structure..."
    
    # Create Monolithic_ESG directory
    mkdir -p "$MONOLITHIC_TARGET"
    print_status "Created Monolithic_ESG directory"
    
    # Create Modular_ESG structure
    mkdir -p "$MODULAR_TARGET/docs/strategic"
    mkdir -p "$MODULAR_TARGET/docs/architecture"
    mkdir -p "$MODULAR_TARGET/docs/implementation"
    mkdir -p "$MODULAR_TARGET/docs/migration"
    print_status "Created documentation directories"
    
    # Create module repositories
    mkdir -p "$MODULAR_TARGET/repositories/risk-interest-rate"
    mkdir -p "$MODULAR_TARGET/repositories/risk-credit"
    mkdir -p "$MODULAR_TARGET/repositories/risk-equity"
    mkdir -p "$MODULAR_TARGET/repositories/risk-fx"
    mkdir -p "$MODULAR_TARGET/repositories/risk-inflation"
    mkdir -p "$MODULAR_TARGET/repositories/risk-liquidity"
    mkdir -p "$MODULAR_TARGET/repositories/risk-counterparty"
    mkdir -p "$MODULAR_TARGET/repositories/radf-aggregation"
    mkdir -p "$MODULAR_TARGET/repositories/ai-orchestra"
    mkdir -p "$MODULAR_TARGET/repositories/backend-api"
    mkdir -p "$MODULAR_TARGET/repositories/frontend-dashboard"
    mkdir -p "$MODULAR_TARGET/repositories/auth-rbac"
    mkdir -p "$MODULAR_TARGET/repositories/deployment-infra"
    print_status "Created 12 module repositories"
    
    # Create shared libraries
    mkdir -p "$MODULAR_TARGET/shared-libraries/@gnanam/types"
    mkdir -p "$MODULAR_TARGET/shared-libraries/@gnanam/utils"
    mkdir -p "$MODULAR_TARGET/shared-libraries/@gnanam/contracts"
    print_status "Created shared libraries structure"
    
    # Create integration testing
    mkdir -p "$MODULAR_TARGET/integration/e2e-tests"
    mkdir -p "$MODULAR_TARGET/integration/api-tests"
    mkdir -p "$MODULAR_TARGET/integration/performance-tests"
    print_status "Created integration testing structure"
    
    # Create scripts
    mkdir -p "$MODULAR_TARGET/scripts/migration"
    mkdir -p "$MODULAR_TARGET/scripts/setup"
    mkdir -p "$MODULAR_TARGET/scripts/deployment"
    print_status "Created scripts structure"
}

# Function to move monolithic code
move_monolithic_code() {
    print_info "Moving monolithic code..."
    
    if [ -d "$MONOLITHIC_SOURCE" ]; then
        print_info "Moving from $MONOLITHIC_SOURCE to $MONOLITHIC_TARGET"
        cp -r "$MONOLITHIC_SOURCE"/* "$MONOLITHIC_TARGET/"
        print_status "Monolithic code moved successfully"
    else
        print_warning "Monolithic source directory not found: $MONOLITHIC_SOURCE"
        print_info "Please ensure the monolithic code is in the correct location"
    fi
}

# Function to create module templates
create_module_templates() {
    print_info "Creating module templates..."
    
    MODULES=(
        "risk-interest-rate"
        "risk-credit"
        "risk-equity"
        "risk-fx"
        "risk-inflation"
        "risk-liquidity"
        "risk-counterparty"
        "radf-aggregation"
        "ai-orchestra"
        "backend-api"
        "frontend-dashboard"
        "auth-rbac"
        "deployment-infra"
    )
    
    for module in "${MODULES[@]}"; do
        MODULE_DIR="$MODULAR_TARGET/repositories/$module"
        
        # Create package.json
        cat > "$MODULE_DIR/package.json" << EOF
{
  "name": "@gnanam/$module",
  "version": "1.0.0",
  "description": "ESG $module module",
  "main": "src/index.ts",
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "test:unit": "jest --testPathPattern=unit",
    "test:integration": "jest --testPathPattern=integration",
    "lint": "eslint src/**/*.ts",
    "format": "prettier --write src/**/*.ts"
  },
  "dependencies": {
    "@gnanam/types": "workspace:*",
    "@gnanam/utils": "workspace:*",
    "@gnanam/contracts": "workspace:*"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "jest": "^29.0.0",
    "@types/jest": "^29.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0"
  }
}
EOF
        
        # Create README.md
        cat > "$MODULE_DIR/README.md" << EOF
# $module

ESG $module module for the Gnanam ESG platform.

## Overview

This module handles $module functionality within the ESG platform.

## Installation

\`\`\`bash
npm install
\`\`\`

## Development

\`\`\`bash
npm run build
npm run test
npm run lint
\`\`\`

## API

[Document API endpoints and interfaces here]

## Testing

\`\`\`bash
npm run test:unit
npm run test:integration
\`\`\`
EOF
        
        # Create .gitignore
        cat > "$MODULE_DIR/.gitignore" << EOF
node_modules/
dist/
build/
*.log
.env
.env.local
.env.production
coverage/
.DS_Store
*.tsbuildinfo
EOF
        
        # Create src directory structure
        mkdir -p "$MODULE_DIR/src"
        mkdir -p "$MODULE_DIR/tests/unit"
        mkdir -p "$MODULE_DIR/tests/integration"
        
        # Create index.ts
        cat > "$MODULE_DIR/src/index.ts" << EOF
// $module module entry point
export * from './types';
export * from './services';
export * from './utils';
EOF
        
        # Create types.ts
        cat > "$MODULE_DIR/src/types.ts" << EOF
// $module module types
export interface ${module//-/_}_config {
  // Configuration interface
}

export interface ${module//-/_}_result {
  // Result interface
}
EOF
        
        print_status "Created template for $module"
    done
}

# Function to create shared library templates
create_shared_library_templates() {
    print_info "Creating shared library templates..."
    
    # Create types package.json
    cat > "$MODULAR_TARGET/shared-libraries/@gnanam/types/package.json" << EOF
{
  "name": "@gnanam/types",
  "version": "1.0.0",
  "description": "Shared TypeScript types for ESG platform",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "test": "jest"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "jest": "^29.0.0",
    "@types/jest": "^29.0.0"
  }
}
EOF
    
    # Create utils package.json
    cat > "$MODULAR_TARGET/shared-libraries/@gnanam/utils/package.json" << EOF
{
  "name": "@gnanam/utils",
  "version": "1.0.0",
  "description": "Shared utilities for ESG platform",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "test": "jest"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "jest": "^29.0.0",
    "@types/jest": "^29.0.0"
  }
}
EOF
    
    # Create contracts package.json
    cat > "$MODULAR_TARGET/shared-libraries/@gnanam/contracts/package.json" << EOF
{
  "name": "@gnanam/contracts",
  "version": "1.0.0",
  "description": "API contracts for ESG platform",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "test": "jest"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "jest": "^29.0.0",
    "@types/jest": "^29.0.0"
  }
}
EOF
    
    print_status "Created shared library templates"
}

# Function to create root package.json
create_root_package_json() {
    print_info "Creating root package.json for workspace..."
    
    cat > "$MODULAR_TARGET/package.json" << EOF
{
  "name": "gnanam-esg-modular",
  "version": "1.0.0",
  "description": "Gnanam ESG Modular Platform",
  "private": true,
  "workspaces": [
    "repositories/*",
    "shared-libraries/@gnanam/*"
  ],
  "scripts": {
    "build": "npm run build --workspaces",
    "test": "npm run test --workspaces",
    "lint": "npm run lint --workspaces",
    "format": "npm run format --workspaces",
    "clean": "npm run clean --workspaces",
    "dev": "concurrently \"npm run dev --workspaces\"",
    "setup": "npm install && npm run build"
  },
  "devDependencies": {
    "concurrently": "^8.0.0",
    "typescript": "^5.0.0"
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  }
}
EOF
    
    print_status "Created root package.json"
}

# Function to create documentation
create_documentation() {
    print_info "Creating documentation structure..."
    
    # Create main README
    cat > "$MODULAR_TARGET/README.md" << EOF
# Gnanam ESG Modular Platform

This is the modular implementation of the Gnanam ESG platform, designed for scalability and maintainability.

## Architecture

The platform is divided into 12 independent modules:

### Risk Modules (7)
- \`risk-interest-rate\` - Interest rate risk models
- \`risk-credit\` - Credit risk models
- \`risk-equity\` - Equity risk models
- \`risk-fx\` - Foreign exchange risk models
- \`risk-inflation\` - Inflation risk models
- \`risk-liquidity\` - Liquidity risk models
- \`risk-counterparty\` - Counterparty risk models

### Core Modules (3)
- \`radf-aggregation\` - Risk aggregation framework
- \`ai-orchestra\` - AI model orchestration
- \`backend-api\` - Core API services

### Infrastructure Modules (2)
- \`frontend-dashboard\` - User interface
- \`auth-rbac\` - Authentication & authorization
- \`deployment-infra\` - Production deployment

## Quick Start

\`\`\`bash
npm install
npm run setup
npm run dev
\`\`\`

## Development

Each module can be developed independently:

\`\`\`bash
cd repositories/risk-interest-rate
npm run dev
\`\`\`

## Testing

\`\`\`bash
npm run test
\`\`\`

## Documentation

- [Strategic Planning](docs/strategic/)
- [Architecture Decisions](docs/architecture/)
- [Implementation Guides](docs/implementation/)
- [Migration Guide](docs/migration/)
EOF
    
    print_status "Created documentation structure"
}

# Main execution
main() {
    echo -e "${BLUE}Starting directory restructuring...${NC}"
    echo ""
    
    # Check if we're in the right directory
    if [ ! -f "package.json" ] || [ ! -d "repositories" ]; then
        print_error "Please run this script from the Modular_ESG/Gnanam_ESG directory"
        exit 1
    fi
    
    # Create backup
    create_backup
    
    # Create directory structure
    create_directory_structure
    
    # Move monolithic code
    move_monolithic_code
    
    # Create module templates
    create_module_templates
    
    # Create shared library templates
    create_shared_library_templates
    
    # Create root package.json
    create_root_package_json
    
    # Create documentation
    create_documentation
    
    echo ""
    print_status "Directory restructuring completed successfully!"
    echo ""
    print_info "Next steps:"
    echo "1. Review the new structure"
    echo "2. Update Git repositories"
    echo "3. Begin module migration"
    echo "4. Update import paths"
    echo ""
    print_info "Backup created in: backup_$(date +%Y%m%d_%H%M%S)"
}

# Run main function
main "$@" 