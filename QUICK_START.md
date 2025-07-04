# 🚀 ESG Platform CI/CD Quick Start Guide

## Immediate Next Steps

### 1. **Run the Setup Script**
```bash
./setup-cicd.sh
```

This script will:
- ✅ Check your Git status
- ✅ Guide you through GitHub repository creation
- ✅ Set up remote origin
- ✅ Push your code to GitHub
- ✅ Provide next steps for configuration

### 2. **Manual GitHub Setup (if needed)**

If the script doesn't work, follow these steps:

#### Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `gnanam-esg-modular`
3. Make it **Public**
4. **Don't** initialize with README, .gitignore, or license
5. Click "Create repository"

#### Connect Your Local Repository
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/gnanam-esg-modular.git
git push -u origin main
```

### 3. **Set Up GitHub Environments**

1. Go to your repository on GitHub
2. Go to **Settings** > **Environments**
3. Create environments:
   - **staging** (for testing)
   - **production** (for live deployment)

### 4. **Configure GitHub Secrets**

Go to **Settings** > **Secrets and variables** > **Actions**

Add these secrets:
```
DOCKER_REGISTRY_TOKEN=your_token_here
SLACK_WEBHOOK_URL=your_webhook_here
```

### 5. **Test the Pipeline**

Make a small change and push:
```bash
echo "# Test" >> README.md
git add README.md
git commit -m "test: Test CI/CD pipeline"
git push
```

Then check the **Actions** tab on GitHub to see your workflow run!

## 🎯 What You Get

### **Automated Workflows**
- ✅ **Testing**: Unit, integration, and performance tests
- ✅ **Security**: Daily vulnerability scanning
- ✅ **Building**: Docker images for all 12 modules
- ✅ **Deployment**: Staging (auto) and production (manual)
- ✅ **Monitoring**: Health checks and alerts

### **Environments**
- 🟢 **Staging**: Auto-deploy on push to `develop`
- 🔴 **Production**: Manual deployment with approval
- 🔵 **Development**: Local development setup

### **Security Features**
- 🔒 **Vulnerability scanning** (daily)
- 🔒 **Dependency auditing** (weekly)
- 🔒 **Container security** (on every build)
- 🔒 **Secrets management** (encrypted)

## 🛠️ Useful Commands

### **Deployment**
```bash
# Check status
./scripts/deployment/deploy.sh status -e staging

# Deploy to staging
./scripts/deployment/deploy.sh deploy -e staging

# Deploy to production
./scripts/deployment/deploy.sh deploy -e production

# Rollback
./scripts/deployment/deploy.sh rollback -e production -v 1.1.0
```

### **Health Checks**
```bash
# Run health checks
./scripts/deployment/health-check.sh -e staging

# Verbose health check
./scripts/deployment/health-check.sh -e production -v
```

### **Logs**
```bash
# View logs
./scripts/deployment/deploy.sh logs -e staging
```

## 📊 Monitoring

Once deployed, you can monitor:

- **GitHub Actions**: Workflow runs and status
- **Health Checks**: Service availability
- **Security**: Vulnerability reports
- **Performance**: Response times and throughput

## 🆘 Troubleshooting

### **Common Issues**

1. **Push fails**: Check GitHub credentials
2. **Workflow fails**: Check Actions tab for details
3. **Deployment fails**: Check environment configuration
4. **Health checks fail**: Check service logs

### **Get Help**

- 📚 **Documentation**: `docs/ci-cd-pipeline.md`
- 🐛 **Issues**: GitHub Issues tab
- 💬 **Support**: Check workflow logs

## 🎉 Success!

Once you see the green checkmarks in GitHub Actions, your CI/CD pipeline is working! 

Your ESG platform now has:
- 🔄 **Automated testing** and deployment
- 🛡️ **Security scanning** and monitoring
- 📈 **Performance tracking** and health checks
- 🚀 **Production-ready** deployment pipeline

---

*Need help? Run `./setup-cicd.sh` for guided setup!* 