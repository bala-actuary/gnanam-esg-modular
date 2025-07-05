# ESG Platform Frontend

This is the React frontend for the Project Gnanam ESG (Economic Scenario Generator) platform.

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation
```bash
npm install
```

### Development
```bash
npm start
```
The app will run on [http://localhost:3000](http://localhost:3000)

### Build for Production
```bash
npm run build
```

## 🏗️ Architecture

- **Framework**: React with TypeScript
- **UI Library**: Material-UI components
- **State Management**: React hooks and context
- **API Integration**: Axios for backend communication

## 📁 Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/         # Page components
├── services/      # API services
└── types/         # TypeScript type definitions
```

## 🔗 Backend Integration

The frontend connects to the FastAPI backend running on `http://localhost:8000` and provides:

- **Model Management**: View and configure risk models
- **Parameter Configuration**: Dynamic parameter forms for each model
- **Simulation Execution**: Run model simulations
- **Results Visualization**: View simulation results and plots

## 🎯 Key Features

- **Dynamic Parameter Forms**: Automatically generated based on backend model definitions
- **Real-time Validation**: Parameter validation with backend integration
- **Responsive Design**: Works on desktop and mobile devices
- **Authentication**: Login/logout functionality

## 🛠️ Development

### Available Scripts
- `npm start` - Start development server
- `npm test` - Run tests
- `npm run build` - Build for production
- `npm run eject` - Eject from Create React App (one-way operation)

## 📝 Notes

- The frontend uses symbolic links to external node_modules for workspace cleanliness
- All API calls are made to the FastAPI backend
- Parameter forms are dynamically generated based on backend model definitions

# Gnanam Frontend - External Dependencies Setup

## 🚨 **IMPORTANT: External Dependencies Strategy**

This frontend uses **external dependencies** to prevent workspace pollution and maintain Cursor performance. Dependencies are stored in `~/external-deps/gnanam-frontend/` and accessed via symbolic links.

### **Why External Dependencies?**
- **Cursor Performance**: Prevents 100,000+ files from slowing down IDE indexing
- **Workspace Cleanliness**: Maintains clean project structure
- **Governance Compliance**: Follows environment protection protocols
- **Team Collaboration**: Consistent setup across all developers

## 🛠️ **Setup Instructions**

### **First Time Setup**
```bash
# Navigate to frontend directory
cd esg-platform/frontend

# Run the setup script
./setup-external-deps.sh
```

### **Manual Setup (if script fails)**
```bash
# 1. Create external directories
mkdir -p ~/external-deps/gnanam-frontend
mkdir -p ~/external-deps/npm-cache

# 2. Configure npm
npm config set prefix ~/external-deps/gnanam-frontend
npm config set cache ~/external-deps/npm-cache

# 3. Install dependencies in external directory
cd ~/external-deps/gnanam-frontend
cp /mnt/c/Users/balaa/OneDrive/Documents/GitHub/Risk_Management/esg-platform/frontend/package.json .
npm install

# 4. Create symbolic link
cd /mnt/c/Users/balaa/OneDrive/Documents/GitHub/Risk_Management/esg-platform/frontend
ln -sf ~/external-deps/gnanam-frontend/node_modules node_modules
```

## 📋 **Usage Guidelines**

### **✅ DO:**
- Run npm commands from `esg-platform/frontend/`
- Use `npm start`, `npm build`, `npm test` normally
- Install new packages using `npm install package-name`
- The symbolic link will handle everything automatically

### **❌ DON'T:**
- Delete the symbolic link (`node_modules`)
- Install dependencies directly in workspace
- Run npm commands from external directory
- Modify files in `~/external-deps/gnanam-frontend/` directly

## 🔧 **Troubleshooting**

### **Symbolic Link Broken**
```bash
# Check if link exists
ls -la node_modules

# Recreate if broken
rm -f node_modules
ln -sf ~/external-deps/gnanam-frontend/node_modules node_modules
```

### **Dependencies Missing**
```bash
# Reinstall in external directory
cd ~/external-deps/gnanam-frontend
npm install

# Recreate symbolic link
cd /mnt/c/Users/balaa/OneDrive/Documents/GitHub/Risk_Management/esg-platform/frontend
ln -sf ~/external-deps/gnanam-frontend/node_modules node_modules
```

### **npm Commands Not Working**
```bash
# Verify npm configuration
npm config list

# Reset to external directories
npm config set prefix ~/external-deps/gnanam-frontend
npm config set cache ~/external-deps/npm-cache
```

## 🏗️ **Project Structure**

```
esg-platform/frontend/
├── src/                    # Source code
├── public/                 # Public assets
├── package.json           # Dependencies list
├── .npmrc                 # NPM configuration (external deps)
├── setup-external-deps.sh # Setup script
├── node_modules ->        # Symbolic link to external deps
└── README.md              # This file

~/external-deps/gnanam-frontend/
├── node_modules/          # Actual dependencies
├── package.json           # Copy of workspace package.json
└── package-lock.json      # Lock file
```

## 🚀 **Development Commands**

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Install new package
npm install package-name

# Update dependencies
npm update
```

## 🔒 **Configuration Files**

### **`.npmrc`**
- Configures npm to use external directories
- Prevents workspace pollution
- Sets cache location

### **`package.json`**
- Contains dependency list
- Includes setup scripts
- Defines build and test commands

## 📊 **Benefits Achieved**

- ✅ **Cursor Performance**: No 100,000+ files in workspace
- ✅ **Fast Indexing**: IDE responds quickly
- ✅ **Clean Workspace**: Organized project structure
- ✅ **Team Consistency**: Same setup for all developers
- ✅ **Governance Compliance**: Follows environment protection rules

## 🎯 **Success Metrics**

- **Workspace File Count**: <1,000 files (optimal)
- **IDE Indexing Time**: <30 seconds
- **npm Command Response**: <5 seconds
- **Development Server Startup**: <10 seconds

---

**Note**: This setup follows the governance framework's environment protection protocols and ensures optimal development experience while maintaining workspace cleanliness.
