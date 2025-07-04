# Web Frontend Module

This module provides the main web frontend application for the Gnanam ESG platform, built with React, TypeScript, and modern web technologies.

## 🏗️ Architecture

### Core Components
- **React 18**: Modern React with hooks and concurrent features
- **TypeScript**: Type-safe development
- **React Router**: Client-side routing
- **Ant Design**: UI component library
- **Chart.js/Recharts**: Data visualization
- **Axios**: HTTP client for API communication
- **Styled Components**: CSS-in-JS styling

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

### Development

```bash
# Start development server
npm run dev

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format

# Type checking
npm run type-check
```

### Production

```bash
# Build and serve production build
npm run prod

# Or build only
npm run build
```

## 🧪 Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage

# Run specific test file
npm test -- --testPathPattern=Dashboard
```

## 📱 Application Features

### Core Pages
- **Dashboard**: Main overview with key metrics
- **Models**: Risk model management and configuration
- **Scenarios**: Scenario analysis and stress testing
- **Settings**: Application configuration
- **Login**: Authentication interface

### Components
- **Layout**: Main application layout with navigation
- **Charts**: Reusable chart components
- **Forms**: Form components with validation
- **Tables**: Data table components
- **Modals**: Modal and dialog components

### Services
- **API Client**: Centralized API communication
- **Auth Service**: Authentication and authorization
- **Data Service**: Data fetching and caching
- **Notification Service**: User notifications

## 📁 Structure

```
web-frontend/
├── src/
│   ├── components/           # Reusable UI components
│   │   ├── Layout.tsx
│   │   ├── Charts/
│   │   ├── Forms/
│   │   └── Tables/
│   ├── pages/               # Page components
│   │   ├── Dashboard.tsx
│   │   ├── Login.tsx
│   │   ├── Models.tsx
│   │   ├── Scenarios.tsx
│   │   └── Settings.tsx
│   ├── services/            # API and business logic
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── data.ts
│   ├── hooks/               # Custom React hooks
│   ├── utils/               # Utility functions
│   ├── types/               # TypeScript type definitions
│   ├── styles/              # Global styles
│   ├── App.tsx              # Main app component
│   ├── index.tsx            # Entry point
│   └── index.css            # Global CSS
├── public/                  # Static assets
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
├── package.json
├── tsconfig.json
└── README.md
```

## 🔧 Development

### Adding New Pages

1. Create page component in `src/pages/`
2. Add route in `App.tsx`
3. Update navigation in `Layout.tsx`
4. Add page-specific types in `types/`

### Adding New Components

1. Create component in `src/components/`
2. Add TypeScript interfaces
3. Include unit tests
4. Update component documentation

### API Integration

```typescript
// Example API service usage
import { apiClient } from '../services/api';

const getRiskMetrics = async () => {
  const response = await apiClient.get('/api/risk/metrics');
  return response.data;
};
```

### State Management

The application uses React hooks for state management:
- `useState` for local component state
- `useContext` for global state
- `useReducer` for complex state logic
- Custom hooks for reusable state logic

## 🎨 Styling

### CSS-in-JS with Styled Components

```typescript
import styled from 'styled-components';

const StyledButton = styled.button`
  background: ${props => props.primary ? '#007bff' : '#6c757d'};
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
`;
```

### Ant Design Components

```typescript
import { Button, Card, Table } from 'antd';

const MyComponent = () => (
  <Card title="Risk Metrics">
    <Table dataSource={data} columns={columns} />
    <Button type="primary">Calculate Risk</Button>
  </Card>
);
```

## 📊 Data Visualization

### Chart.js Integration

```typescript
import { Line } from 'react-chartjs-2';

const RiskChart = ({ data }) => (
  <Line
    data={data}
    options={{
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Risk Metrics Over Time'
        }
      }
    }}
  />
);
```

### Recharts Integration

```typescript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const RiskLineChart = ({ data }) => (
  <LineChart width={600} height={300} data={data}>
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="date" />
    <YAxis />
    <Tooltip />
    <Line type="monotone" dataKey="value" stroke="#8884d8" />
  </LineChart>
);
```

## 🔐 Authentication

### Login Flow

```typescript
import { useAuth } from '../hooks/useAuth';

const LoginPage = () => {
  const { login } = useAuth();
  
  const handleLogin = async (credentials) => {
    try {
      await login(credentials);
      // Redirect to dashboard
    } catch (error) {
      // Handle error
    }
  };
};
```

### Protected Routes

```typescript
import { ProtectedRoute } from '../components/ProtectedRoute';

const App = () => (
  <Router>
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <DashboardPage />
        </ProtectedRoute>
      } />
    </Routes>
  </Router>
);
```

## 🚀 Deployment

### Build Process

```bash
# Create production build
npm run build

# The build folder contains:
# - index.html
# - static/js/ (bundled JavaScript)
# - static/css/ (bundled CSS)
# - static/media/ (images and assets)
```

### Docker Deployment

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Environment Variables

```bash
# API Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_TIMEOUT=30000

# Authentication
REACT_APP_AUTH_DOMAIN=your-domain.auth0.com
REACT_APP_AUTH_CLIENT_ID=your-client-id

# Feature Flags
REACT_APP_ENABLE_ANALYTICS=true
REACT_APP_ENABLE_DEBUG=false
```

## 🔄 Integration

### API Communication

The frontend communicates with backend services through:
- **REST APIs**: Standard REST endpoints
- **WebSocket**: Real-time updates
- **GraphQL**: Complex data queries (optional)

### Module Integration

```typescript
// Integration with other modules
import { RiskMetrics } from '@gnanam/types';
import { calculateVaR } from '@gnanam/utils';

const Dashboard = () => {
  const [metrics, setMetrics] = useState<RiskMetrics[]>([]);
  
  useEffect(() => {
    // Fetch data from risk models
    fetchRiskMetrics().then(setMetrics);
  }, []);
};
```

## 📚 References

- React Documentation: https://react.dev/
- TypeScript Documentation: https://www.typescriptlang.org/
- Ant Design: https://ant.design/
- Chart.js: https://www.chartjs.org/
- Recharts: https://recharts.org/
- Styled Components: https://styled-components.com/

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Submit a pull request

## 📄 License

This module is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 