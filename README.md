# Gnanam ESG Modular Platform

This is the modular implementation of the Gnanam ESG platform, designed for scalability and maintainability. The platform is divided into independent modules that can be developed, tested, and deployed separately.

## 🏗️ Architecture

The platform is divided into 12 independent modules:

### Risk Modules (7)
- `risk-interest-rate` - Interest rate risk models
- `risk-credit` - Credit risk models
- `risk-equity` - Equity risk models
- `risk-foreign-exchange` - Foreign exchange risk models
- `risk-inflation` - Inflation risk models
- `risk-liquidity` - Liquidity risk models
- `risk-counterparty` - Counterparty risk models

### Core Modules (3)
- `radf-aggregation` - Risk aggregation framework
- `ai-gateway` - AI model orchestration
- `backend-api` - Core API services

### Infrastructure Modules (2)
- `frontend-dashboard` - User interface
- `auth-rbac` - Authentication & authorization
- `deployment-infra` - Production deployment

## 🚀 Quick Start

### Prerequisites
- Node.js >= 18.0.0
- npm >= 9.0.0
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/gnanam/gnanam-esg-modular.git
cd gnanam-esg-modular

# Install dependencies
npm install

# Setup the platform
npm run setup

# Start development
npm run dev
```

## 📁 Project Structure

```
Gnanam_ESG/
├── docs/                   # Documentation
│   ├── architecture/       # Architecture decisions
│   ├── implementation/     # Implementation guides
│   ├── migration/          # Migration documentation
│   └── strategic/          # Strategic planning
├── repositories/           # Module repositories
│   ├── risk-*/             # Risk model modules
│   ├── radf-aggregation/   # Risk aggregation
│   ├── ai-gateway/         # AI orchestration
│   ├── backend-api/        # Core API services
│   ├── frontend-dashboard/ # User interface
│   ├── auth-rbac/          # Authentication
│   └── deployment-infra/   # Infrastructure
├── shared-libraries/       # Shared dependencies
│   └── @gnanam/
│       ├── types/          # Common TypeScript types
│       ├── utils/          # Shared utilities
│       └── contracts/      # API contracts
├── integration/            # Integration testing
│   ├── e2e-tests/          # End-to-end tests
│   ├── api-tests/          # API integration tests
│   └── performance-tests/  # Performance validation
└── scripts/                # Build and deployment scripts
    ├── migration/          # Migration scripts
    ├── setup/              # Setup scripts
    └── deployment/         # Deployment scripts
```

## 🛠️ Development

### Working with Modules

Each module can be developed independently:

```bash
# Navigate to a specific module
cd repositories/risk-interest-rate

# Install module dependencies
npm install

# Run module tests
npm run test

# Build module
npm run build

# Start module development server
npm run dev
```

### Adding a New Module

1. Create a new directory in `repositories/`
2. Initialize with `package.json`, `README.md`, and basic structure
3. Add the module to the workspace in root `package.json`
4. Implement the module following the established patterns
5. Add tests and documentation

### Shared Libraries

Common code is shared through the `@gnanam` packages:

- `@gnanam/types` - Common TypeScript types
- `@gnanam/utils` - Shared utilities
- `@gnanam/contracts` - API contracts

## 🧪 Testing

### Running Tests

```bash
# Run all tests
npm run test

# Run tests for a specific module
cd repositories/risk-interest-rate && npm run test

# Run integration tests
npm run test:integration

# Run performance tests
npm run test:performance
```

### Test Coverage

All modules should maintain >90% test coverage. Coverage reports are generated automatically.

## 📚 Documentation

- [Architecture Design](docs/architecture/MODULAR_ARCHITECTURE_DESIGN.md)
- [Implementation Guide](docs/implementation/MODULAR_IMPLEMENTATION_GUIDE.md)
- [Migration Guide](docs/migration/MODULAR_MIGRATION_GUIDE.md)
- [Git Migration Guide](docs/migration/GIT_MIGRATION_GUIDE.md)

## 🔧 Scripts

- `npm run build` - Build all modules
- `npm run test` - Run all tests
- `npm run lint` - Lint all code
- `npm run format` - Format all code
- `npm run dev` - Start development servers
- `npm run setup` - Initial setup
- `npm run migrate` - Run migration scripts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Check the [documentation](docs/)
- Open an [issue](https://github.com/gnanam/gnanam-esg-modular/issues)
- Contact the development team

---

**Ready to build the future of ESG risk management? Start with your first module!** 🚀 