# 🔄 **GIT MIGRATION GUIDE**
## **Repository Restructuring for Modular Architecture**

---

## **🎯 EXECUTIVE SUMMARY**

This guide provides step-by-step instructions for migrating Git repositories during the transition from monolithic to modular architecture. The goal is to maintain proper version control while enabling independent module development.

### **Migration Strategy**
- **Option 1**: Multi-Repository (Recommended) - Each module gets its own Git repository
- **Option 2**: Monorepo with Workspaces - Single repository with workspace management
- **Option 3**: Hybrid Approach - Core modules in monorepo, risk modules independent

---

## **📋 PRE-MIGRATION CHECKLIST**

### **Before Starting Migration**
- [ ] **Backup Current State**: Create complete backup of current Git repositories
- [ ] **Document Current Structure**: Map all branches, tags, and commit history
- [ ] **Identify Dependencies**: List all internal and external Git dependencies
- [ ] **Plan Module Boundaries**: Define clear module responsibilities and ownership
- [ ] **Setup New Repositories**: Prepare new repository locations
- [ ] **Notify Team**: Inform all contributors about migration timeline

### **Current State Assessment**
```bash
# Check current repository structure
git remote -v
git branch -a
git tag -l
git log --oneline --graph --all
```

---

## **🚀 OPTION 1: MULTI-REPOSITORY MIGRATION (RECOMMENDED)**

### **Step 1: Create New Module Repositories**

#### **1.1 Create Remote Repositories**
```bash
# Create new repositories on GitHub/GitLab
# Example for risk-interest-rate module
gh repo create gnanam/risk-interest-rate --private --description "ESG Interest Rate Risk Module"
gh repo create gnanam/risk-credit --private --description "ESG Credit Risk Module"
gh repo create gnanam/risk-equity --private --description "ESG Equity Risk Module"
gh repo create gnanam/risk-fx --private --description "ESG Foreign Exchange Risk Module"
gh repo create gnanam/risk-inflation --private --description "ESG Inflation Risk Module"
gh repo create gnanam/risk-liquidity --private --description "ESG Liquidity Risk Module"
gh repo create gnanam/risk-counterparty --private --description "ESG Counterparty Risk Module"
gh repo create gnanam/radf-aggregation --private --description "ESG Risk Aggregation Framework"
gh repo create gnanam/ai-orchestra --private --description "ESG AI Model Orchestration"
gh repo create gnanam/backend-api --private --description "ESG Backend API Services"
gh repo create gnanam/frontend-dashboard --private --description "ESG Frontend Dashboard"
gh repo create gnanam/auth-rbac --private --description "ESG Authentication & RBAC"
gh repo create gnanam/deployment-infra --private --description "ESG Deployment Infrastructure"
gh repo create gnanam/shared-libraries --private --description "ESG Shared Libraries"
```

#### **1.2 Initialize Local Module Repositories**
```bash
# Navigate to modular directory
cd My_Projects/Modular_ESG/Gnanam_ESG/repositories

# Initialize each module repository
for module in risk-interest-rate risk-credit risk-equity risk-fx risk-inflation risk-liquidity risk-counterparty radf-aggregation ai-orchestra backend-api frontend-dashboard auth-rbac deployment-infra; do
    cd $module
    git init
    git remote add origin https://github.com/gnanam/$module.git
    git add .
    git commit -m "Initial commit: $module module structure"
    git branch -M main
    git push -u origin main
    cd ..
done
```

### **Step 2: Migrate Code from Monolithic**

#### **2.1 Create Migration Scripts**
```bash
# Create migration script for each module
cat > migrate-risk-interest-rate.sh << 'EOF'
#!/bin/bash
# Migrate interest rate models from monolithic

SOURCE_DIR="../../Monolithic_ESG/RiskModels/src/models/interest_rate"
TARGET_DIR="./repositories/risk-interest-rate/src"

# Create target directory
mkdir -p "$TARGET_DIR"

# Copy relevant files
cp -r "$SOURCE_DIR"/* "$TARGET_DIR/"

# Update import paths
find "$TARGET_DIR" -name "*.py" -exec sed -i 's/from RiskModels/from @gnanam\/types/g' {} \;

# Commit changes
cd repositories/risk-interest-rate
git add .
git commit -m "Migrate interest rate models from monolithic"
git push origin main
EOF

chmod +x migrate-risk-interest-rate.sh
```

#### **2.2 Execute Migration for Each Module**
```bash
# Execute migration scripts
./migrate-risk-interest-rate.sh
./migrate-risk-credit.sh
./migrate-risk-equity.sh
# ... repeat for all modules
```

### **Step 3: Setup Shared Libraries Repository**

#### **3.1 Create Shared Libraries Repository**
```bash
cd My_Projects/Modular_ESG/Gnanam_ESG/shared-libraries
git init
git remote add origin https://github.com/gnanam/shared-libraries.git

# Create initial structure
mkdir -p @gnanam/types @gnanam/utils @gnanam/contracts

# Create package.json for workspace
cat > package.json << 'EOF'
{
  "name": "@gnanam/shared-libraries",
  "version": "1.0.0",
  "description": "Shared libraries for ESG platform",
  "private": true,
  "workspaces": [
    "@gnanam/*"
  ],
  "scripts": {
    "build": "npm run build --workspaces",
    "test": "npm run test --workspaces",
    "publish": "npm publish --workspaces"
  }
}
EOF

git add .
git commit -m "Initial commit: shared libraries structure"
git branch -M main
git push -u origin main
```

---

## **🏗️ OPTION 2: MONOREPO WITH WORKSPACES**

### **Step 1: Create Monorepo Structure**
```bash
cd My_Projects/Modular_ESG/Gnanam_ESG
git init
git remote add origin https://github.com/gnanam/gnanam-esg-modular.git

# Create workspace configuration
cat > package.json << 'EOF'
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
    "dev": "concurrently \"npm run dev --workspaces\""
  }
}
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
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

git add .
git commit -m "Initial commit: monorepo structure"
git branch -M main
git push -u origin main
```

### **Step 2: Setup Module Workspaces**
```bash
# Each module becomes a workspace
cd repositories/risk-interest-rate
cat > package.json << 'EOF'
{
  "name": "@gnanam/risk-interest-rate",
  "version": "1.0.0",
  "description": "ESG Interest Rate Risk Module",
  "main": "src/index.ts",
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "dev": "ts-node src/index.ts"
  },
  "dependencies": {
    "@gnanam/types": "workspace:*",
    "@gnanam/utils": "workspace:*"
  }
}
EOF

# Repeat for all modules
```

---

## **🔧 GIT WORKFLOW STRATEGIES**

### **Branching Strategy for Multi-Repository**

#### **1. Module Development Workflow**
```bash
# Feature development
git checkout -b feature/new-interest-rate-model
# ... make changes ...
git commit -m "Add new interest rate model"
git push origin feature/new-interest-rate-model

# Create pull request
gh pr create --title "Add new interest rate model" --body "Implements Hull-White two-factor model"
```

#### **2. Integration Workflow**
```bash
# Integration testing
git checkout main
git pull origin main
npm run test:integration
npm run build
```

#### **3. Release Workflow**
```bash
# Create release
git checkout -b release/v1.2.0
git merge main
git tag v1.2.0
git push origin v1.2.0
```

### **Branching Strategy for Monorepo**

#### **1. Module-Specific Branches**
```bash
# Module-specific feature branches
git checkout -b feature/risk-interest-rate/new-model
git checkout -b feature/risk-credit/calibration-improvement
```

#### **2. Integration Branches**
```bash
# Integration branch for cross-module changes
git checkout -b integration/api-contracts
git merge feature/risk-interest-rate/new-model
git merge feature/risk-credit/calibration-improvement
```

---

## **📦 DEPENDENCY MANAGEMENT**

### **Module Dependencies**

#### **1. Internal Dependencies**
```json
// risk-interest-rate/package.json
{
  "dependencies": {
    "@gnanam/types": "^1.0.0",
    "@gnanam/utils": "^1.0.0",
    "@gnanam/contracts": "^1.0.0"
  }
}
```

#### **2. External Dependencies**
```json
// risk-interest-rate/package.json
{
  "dependencies": {
    "numpy": "^1.24.0",
    "scipy": "^1.10.0",
    "pandas": "^2.0.0"
  }
}
```

### **Version Management**

#### **1. Semantic Versioning**
```bash
# Major version for breaking changes
git tag v2.0.0

# Minor version for new features
git tag v1.3.0

# Patch version for bug fixes
git tag v1.2.1
```

#### **2. Dependency Updates**
```bash
# Update shared library
cd shared-libraries/@gnanam/types
npm version patch
npm publish

# Update dependent modules
cd ../../repositories/risk-interest-rate
npm update @gnanam/types
```

---

## **🔗 CI/CD INTEGRATION**

### **Multi-Repository CI/CD**

#### **1. Module-Specific Pipelines**
```yaml
# .github/workflows/risk-module.yml
name: Risk Module CI/CD
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm install
      - name: Run tests
        run: npm run test
      - name: Build
        run: npm run build
```

#### **2. Integration Pipeline**
```yaml
# .github/workflows/integration.yml
name: Integration Testing
on: [workflow_run]
jobs:
  integration:
    runs-on: ubuntu-latest
    steps:
      - name: Clone all modules
        run: |
          git clone https://github.com/gnanam/risk-interest-rate
          git clone https://github.com/gnanam/risk-credit
          # ... clone all modules
      - name: Run integration tests
        run: npm run test:integration
```

### **Monorepo CI/CD**

#### **1. Workspace-Aware Pipeline**
```yaml
# .github/workflows/monorepo.yml
name: Monorepo CI/CD
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm install
      - name: Build all workspaces
        run: npm run build
      - name: Test all workspaces
        run: npm run test
```

---

## **🚨 MIGRATION RISKS AND MITIGATION**

### **1. Data Loss Prevention**
- **Multiple Backups**: Create backups before migration
- **Incremental Migration**: Migrate one module at a time
- **Rollback Plan**: Maintain ability to rollback
- **Version Control**: Use Git for all changes

### **2. Dependency Management**
- **Dependency Mapping**: Map all dependencies before migration
- **Version Compatibility**: Ensure module version compatibility
- **Breaking Changes**: Plan for breaking changes carefully
- **Shared Library Strategy**: Create comprehensive shared libraries

### **3. Team Coordination**
- **Communication**: Clear communication about migration timeline
- **Training**: Train team on new Git workflows
- **Documentation**: Comprehensive documentation for new processes
- **Support**: Provide support during transition period

---

## **📊 MIGRATION TIMELINE**

### **Week 1: Preparation**
- [ ] Create backup of current repositories
- [ ] Document current Git structure
- [ ] Plan module boundaries
- [ ] Setup new repository locations

### **Week 2: Repository Creation**
- [ ] Create new module repositories
- [ ] Setup shared libraries repository
- [ ] Initialize basic structure
- [ ] Setup CI/CD pipelines

### **Week 3: Code Migration**
- [ ] Migrate risk models (7 modules)
- [ ] Migrate core services (3 modules)
- [ ] Migrate infrastructure (2 modules)
- [ ] Update all references

### **Week 4: Validation**
- [ ] Integration testing
- [ ] Performance testing
- [ ] Documentation update
- [ ] Team training

---

## **🎯 SUCCESS METRICS**

### **Technical Metrics**
- ✅ **Zero Data Loss**: All code and history preserved
- ✅ **Build Success**: All modules build successfully
- ✅ **Test Coverage**: 90%+ test coverage maintained
- ✅ **Integration Success**: Cross-module integration works

### **Process Metrics**
- ✅ **Development Velocity**: Improved development speed
- ✅ **Deployment Frequency**: Increased deployment frequency
- ✅ **Bug Reduction**: Reduced bugs through modularity
- ✅ **Team Productivity**: Improved team collaboration

---

## **🚀 NEXT STEPS**

### **Immediate Actions (This Week)**
1. **Choose Migration Strategy**: Decide between multi-repo vs monorepo
2. **Create Backup**: Create comprehensive backup of current state
3. **Setup New Repositories**: Create new repository structure
4. **Begin Documentation**: Start creating migration documentation

### **Short-term Actions (Next 2 Weeks)**
1. **Migrate First Module**: Start with risk-interest-rate module
2. **Setup CI/CD**: Configure pipelines for each module
3. **Create Integration Framework**: Cross-module testing
4. **Update Documentation**: Module-specific documentation

### **Medium-term Actions (Next Month)**
1. **Complete Migration**: Finish all module migration
2. **Integration Testing**: Comprehensive testing
3. **Performance Optimization**: Optimize modular performance
4. **Team Training**: Complete team training

---

**🎯 This Git migration guide provides a comprehensive approach to restructuring your repositories for modular architecture while maintaining proper version control and enabling independent module development.**

**Ready to begin the Git migration? Let's start with the repository creation phase!** 🚀 