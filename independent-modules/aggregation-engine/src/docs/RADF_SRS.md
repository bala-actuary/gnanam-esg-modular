# Risk Aggregation & Dependency Framework (RADF) - System Requirements Specification (SRS)

## 1. Overview
The RADF is a core component of the RiskModels platform, responsible for orchestrating, aggregating, and managing dependencies across all risk models. It enables holistic risk assessment, scenario aggregation, and supports regulatory, audit, and business needs.

## 2. Objectives
- Enable seamless aggregation of results from multiple risk models
- Allow flexible, transparent dependency mapping between models
- Support a wide range of aggregation methods (sum, VaR, ES, custom)
- Provide robust audit, governance, and reporting features
- Be accessible and usable by both technical and non-technical users

## 3. Functional Requirements
- Standardized data contracts for all model inputs/outputs
- Configurable dependency mapping (via config file and/or UI)
- Orchestration engine to resolve dependencies and run models in correct order
- Aggregation engine supporting pluggable methods
- Scenario "recipes" for reusable configurations
- Audit logging of all runs, configs, and results
- Versioning of configs and outputs
- API endpoints for running, monitoring, and retrieving results
- (Future) Web UI for scenario setup, dependency mapping, and results visualization

## 4. Non-Functional Requirements
- Performance: Must handle large portfolios and complex dependency graphs efficiently
- Security: RBAC, authentication, audit trails, and data encryption
- Usability: Clear documentation, user-friendly config, and (future) UI
- Extensibility: Easy to add new models, aggregation methods, and dependency types
- Compliance: Support for regulatory and audit requirements

## 5. User Roles & Workflows
- **Actuary/Risk Manager:** Define scenarios, configure dependencies, run aggregations, review results
- **Developer:** Integrate new models, extend aggregation/orchestration logic, maintain system
- **Auditor/Regulator:** Review logs, configs, and results for compliance

### Example Workflow
1. User defines scenario and dependencies in config file (or UI)
2. User triggers aggregation via API (or UI)
3. RADF orchestrates model runs, resolves dependencies, aggregates results
4. User reviews results and audit logs

## 6. Acceptance Criteria
- All models can be orchestrated and aggregated via RADF
- Users can define and edit dependencies/configs without code changes
- Aggregated results and audit logs are accessible and exportable
- System meets performance, security, and compliance requirements

---
