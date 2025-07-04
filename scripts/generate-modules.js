#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🚀 Generating Gnanam ESG Platform Modules...\n');

// Create repositories directory
const reposDir = path.join(__dirname, '..', 'repositories');
if (!fs.existsSync(reposDir)) {
  fs.mkdirSync(reposDir, { recursive: true });
  console.log(`Created directory: ${reposDir}`);
}

// Simple module generation
const modules = ['risk-interest-rate', 'risk-credit', 'risk-equity', 'risk-foreign-exchange', 'risk-inflation', 'risk-liquidity', 'risk-counterparty', 'aggregation-engine', 'ai-gateway', 'api-gateway', 'web-frontend', 'monitoring-dashboard'];

modules.forEach(moduleName => {
  const modulePath = path.join(reposDir, moduleName);
  
  // Create module directory
  if (!fs.existsSync(modulePath)) {
    fs.mkdirSync(modulePath, { recursive: true });
    console.log(`Created module directory: ${moduleName}`);
  }
  
  // Create src directory
  const srcPath = path.join(modulePath, 'src');
  if (!fs.existsSync(srcPath)) {
    fs.mkdirSync(srcPath, { recursive: true });
  }
  
  // Create basic package.json
  const packageJson = {
    name: `@gnanam/${moduleName}`,
    version: '1.0.0',
    description: `${moduleName} module`,
    main: 'dist/index.js',
    types: 'dist/index.d.ts',
    scripts: {
      build: 'tsc',
      test: 'jest',
      lint: 'eslint src --ext .ts'
    },
    dependencies: {
      '@gnanam/types': 'workspace:*',
      '@gnanam/utils': 'workspace:*'
    },
    devDependencies: {
      '@types/node': '^18.0.0',
      'typescript': '^5.2.0',
      'jest': '^29.0.0',
      '@types/jest': '^29.0.0'
    },
    keywords: ['esg', 'risk-models'],
    author: 'Gnanam Team',
    license: 'MIT'
  };
  
  fs.writeFileSync(path.join(modulePath, 'package.json'), JSON.stringify(packageJson, null, 2));
  console.log(`Created package.json for: ${moduleName}`);
  
  // Create basic index.ts
  const indexContent = `// ${moduleName} module
export const MODULE_INFO = {
  name: '${moduleName}',
  version: '1.0.0'
};
`;
  
  fs.writeFileSync(path.join(modulePath, 'src', 'index.ts'), indexContent);
  console.log(`Created index.ts for: ${moduleName}`);
});

console.log('\n🎉 All modules generated successfully!');
