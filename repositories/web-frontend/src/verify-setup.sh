#!/bin/bash

# Frontend Setup Verification Script
# This script verifies that external dependencies are working correctly

echo "🔍 Verifying Gnanam Frontend External Dependencies Setup..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Must run from esg-platform/frontend directory"
    exit 1
fi

# Check symbolic link
echo "📁 Checking symbolic link..."
if [ -L "node_modules" ]; then
    echo "✅ Symbolic link exists"
    echo "   node_modules -> $(readlink node_modules)"
else
    echo "❌ Symbolic link missing"
    echo "   Run: ln -sf ~/external-deps/gnanam-frontend/node_modules node_modules"
    exit 1
fi

# Check external directory
echo "📂 Checking external directory..."
if [ -d "$(readlink node_modules)" ]; then
    echo "✅ External dependencies directory exists"
else
    echo "❌ External dependencies directory missing"
    echo "   Run: cd ~/external-deps/gnanam-frontend && npm install"
    exit 1
fi

# Check npm configuration
echo "⚙️  Checking npm configuration..."
npm config get prefix | grep -q "external-deps" && echo "✅ npm prefix configured correctly" || echo "⚠️  npm prefix not set to external directory"

# Test npm commands
echo "🧪 Testing npm commands..."
if npm list --depth=0 > /dev/null 2>&1; then
    echo "✅ npm list working"
else
    echo "❌ npm list failed"
    exit 1
fi

# Check workspace file count
echo "📊 Checking workspace file count..."
workspace_files=$(find . -type f -name "*.js" -o -name "*.ts" -o -name "*.tsx" -o -name "*.json" -o -name "*.md" | wc -l)
echo "   Workspace files: $workspace_files (should be <1000)"

# Check if node_modules is actually a link (not a directory)
if [ -d "node_modules" ] && [ ! -L "node_modules" ]; then
    echo "❌ WARNING: node_modules is a directory, not a symbolic link!"
    echo "   This means dependencies are installed in workspace (BAD)"
    echo "   Run: rm -rf node_modules && ln -sf ~/external-deps/gnanam-frontend/node_modules node_modules"
    exit 1
fi

echo ""
echo "🎉 Setup verification complete!"
echo ""
echo "📋 Summary:"
echo "  ✅ Symbolic link working"
echo "  ✅ External dependencies accessible"
echo "  ✅ npm commands functional"
echo "  ✅ Workspace remains clean"
echo ""
echo "🚀 Ready for development!" 