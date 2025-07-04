# Risk Aggregation & Dependency Framework (RADF) - Test Plan

## 1. Test Objectives
- Ensure RADF meets all functional and non-functional requirements
- Validate correct orchestration, dependency resolution, and aggregation
- Confirm usability, security, and compliance

## 2. Test Types
- Unit tests (orchestrator, aggregation, plugins)
- Integration tests (multi-model, end-to-end scenarios)
- Performance tests (large portfolios, complex dependencies)
- Security tests (auth, RBAC, audit logging)
- User acceptance tests (UAT) for actuaries/risk managers

## 3. Test Scenarios
- Orchestrate and aggregate two or more models with dependencies
- Handle missing data, errors, and retries
- Run all supported aggregation methods (sum, VaR, ES, custom)
- Validate audit logs and versioning
- Test API endpoints and (future) UI workflows
- Simulate regulatory/audit review (log and config export)

## 4. Acceptance Criteria
- All requirements in RADF_SRS are covered by tests
- All tests pass for each release
- No critical bugs or regressions
- Users can run, monitor, and review aggregations as specified

## 5. Traceability Matrix
- Map each test scenario to SRS requirements for auditability

---
