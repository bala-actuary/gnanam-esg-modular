# Orchestrator logic for RADF will be implemented here.

import logging
import json
import csv
from datetime import datetime
from typing import Dict, Any, Optional
from io import StringIO
from .config import load_config, validate_config


class RADFError(Exception):
    """Base exception for RADF-specific errors."""

    pass


class ConfigError(RADFError):
    """Raised when config validation fails."""

    pass


class ModelExecutionError(RADFError):
    """Raised when model execution fails."""

    pass


class AggregationError(RADFError):
    """Raised when aggregation fails."""

    pass


class RADFOrchestrator:
    def __init__(self, config_path: str, user: Optional[str] = None):
        self.config_path = config_path
        self.config = None
        self.user = user or "unknown"
        self.audit_log = []
        self._setup_logging()

    def _setup_logging(self):
        """Set up structured logging for audit trail."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    def _log_audit_event(
        self, event_type: str, details: Dict[str, Any], status: str = "success"
    ):
        """Log an audit event with structured data."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "user": self.user,
            "event_type": event_type,
            "details": details,
            "status": status,
        }
        self.audit_log.append(event)
        logging.info(f"AUDIT: {event_type} - {status} - {details}")

    def load_config(self):
        """Load and validate configuration with detailed error handling."""
        try:
            self._log_audit_event("config_load", {"config_path": self.config_path})
            self.config = load_config(self.config_path)
            if self.config is None:
                raise ConfigError("Failed to load configuration file")
            self._log_audit_event(
                "config_load", {"config_path": self.config_path}, "success"
            )
        except Exception as e:
            self._log_audit_event(
                "config_load",
                {"config_path": self.config_path, "error": str(e)},
                "error",
            )
            raise ConfigError(f"Configuration loading failed: {e}")

    def validate_config(self):
        """Validate configuration with detailed error reporting."""
        try:
            scenario_name = (
                self.config.get("scenario_name", "unknown")
                if self.config
                else "unknown"
            )
            self._log_audit_event("config_validation", {"scenario_name": scenario_name})
            if not validate_config(self.config):
                raise ConfigError("Configuration validation failed")
            self._log_audit_event(
                "config_validation", {"scenario_name": scenario_name}, "success"
            )
            return True
        except Exception as e:
            scenario_name = (
                self.config.get("scenario_name", "unknown")
                if self.config
                else "unknown"
            )
            self._log_audit_event(
                "config_validation",
                {"scenario_name": scenario_name, "error": str(e)},
                "error",
            )
            raise ConfigError(f"Configuration validation failed: {e}")

    def _execute_models(self):
        """Execute models with dependency resolution and error handling."""
        try:
            models_config = self.config.get("models", []) if self.config else []
            num_models = len(models_config)
            self._log_audit_event("model_execution", {"num_models": num_models})
            
            # Execute models with dependency resolution
            executed_models = {}
            execution_order = self._resolve_dependencies(models_config)
            
            for model_name in execution_order:
                model_config = next((m for m in models_config if m.get("name") == model_name), None)
                if model_config:
                    try:
                        result = self._execute_single_model(model_config, executed_models)
                        executed_models[model_name] = result
                        self._log_audit_event(
                            "model_execution_success", 
                            {"model_name": model_name, "result_keys": list(result.keys())}
                        )
                    except Exception as e:
                        self._log_audit_event(
                            "model_execution_error", 
                            {"model_name": model_name, "error": str(e)}, 
                            "error"
                        )
                        raise ModelExecutionError(f"Model {model_name} execution failed: {e}")
            
            self._log_audit_event(
                "model_execution", 
                {"num_models": num_models, "executed_models": list(executed_models.keys())}, 
                "success"
            )
            return executed_models
            
        except Exception as e:
            self._log_audit_event("model_execution", {"error": str(e)}, "error")
            raise ModelExecutionError(f"Model execution failed: {e}")

    def _resolve_dependencies(self, models_config):
        """Resolve model dependencies and return execution order."""
        # Simple dependency resolution - models without dependencies first
        dependency_graph = {}
        for model in models_config:
            model_name = model.get("name", "unknown")
            dependencies = model.get("dependencies", [])
            dependency_graph[model_name] = dependencies
        
        # Topological sort (simplified)
        execution_order = []
        visited = set()
        
        def visit(model_name):
            if model_name in visited:
                return
            visited.add(model_name)
            
            # Visit dependencies first
            for dep in dependency_graph.get(model_name, []):
                if dep in dependency_graph:
                    visit(dep)
            
            execution_order.append(model_name)
        
        # Visit all models
        for model_name in dependency_graph:
            visit(model_name)
        
        return execution_order

    def _execute_single_model(self, model_config, executed_models):
        """Execute a single model with its configuration."""
        model_name = model_config.get("name", "unknown")
        model_type = model_config.get("type", "unknown")
        parameters = model_config.get("parameters", {})
        
        # Simulate model execution based on type
        if model_type == "interest_rate":
            return self._execute_interest_rate_model(parameters)
        elif model_type == "equity":
            return self._execute_equity_model(parameters)
        elif model_type == "credit":
            return self._execute_credit_model(parameters)
        elif model_type == "fx":
            return self._execute_fx_model(parameters)
        elif model_type == "inflation":
            return self._execute_inflation_model(parameters)
        elif model_type == "liquidity":
            return self._execute_liquidity_model(parameters)
        elif model_type == "counterparty":
            return self._execute_counterparty_model(parameters)
        else:
            # Generic model execution
            return {
                "model_name": model_name,
                "model_type": model_type,
                "risk_measure": [0.0],
                "parameters": parameters,
                "execution_time": 0.1,
                "status": "completed"
            }

    def _execute_interest_rate_model(self, parameters):
        """Execute interest rate model simulation."""
        return {
            "model_type": "interest_rate",
            "risk_measure": [0.05, 0.03, 0.07],
            "parameters": parameters,
            "execution_time": 0.2,
            "status": "completed"
        }

    def _execute_equity_model(self, parameters):
        """Execute equity model simulation."""
        return {
            "model_type": "equity",
            "risk_measure": [0.12, 0.08, 0.15],
            "parameters": parameters,
            "execution_time": 0.15,
            "status": "completed"
        }

    def _execute_credit_model(self, parameters):
        """Execute credit model simulation."""
        return {
            "model_type": "credit",
            "risk_measure": [0.02, 0.01, 0.04],
            "parameters": parameters,
            "execution_time": 0.25,
            "status": "completed"
        }

    def _execute_fx_model(self, parameters):
        """Execute FX model simulation."""
        return {
            "model_type": "fx",
            "risk_measure": [0.08, 0.05, 0.11],
            "parameters": parameters,
            "execution_time": 0.18,
            "status": "completed"
        }

    def _execute_inflation_model(self, parameters):
        """Execute inflation model simulation."""
        return {
            "model_type": "inflation",
            "risk_measure": [0.03, 0.02, 0.05],
            "parameters": parameters,
            "execution_time": 0.12,
            "status": "completed"
        }

    def _execute_liquidity_model(self, parameters):
        """Execute liquidity model simulation."""
        return {
            "model_type": "liquidity",
            "risk_measure": [0.06, 0.04, 0.09],
            "parameters": parameters,
            "execution_time": 0.22,
            "status": "completed"
        }

    def _execute_counterparty_model(self, parameters):
        """Execute counterparty model simulation."""
        return {
            "model_type": "counterparty",
            "risk_measure": [0.04, 0.02, 0.07],
            "parameters": parameters,
            "execution_time": 0.20,
            "status": "completed"
        }

    def _perform_aggregation(self):
        """Perform aggregation with error handling."""
        try:
            agg_config = self.config.get("aggregation", {}) if self.config else {}
            method = agg_config.get("method", "sum")
            self._log_audit_event("aggregation", {"method": method})
            
            # Get model outputs from execution
            model_outputs = getattr(self, '_executed_models', {})
            if not model_outputs:
                # If no models were executed, create sample data
                model_outputs = {
                    "interest_rate": {"risk_measure": [0.05, 0.03, 0.07]},
                    "equity": {"risk_measure": [0.12, 0.08, 0.15]},
                    "credit": {"risk_measure": [0.02, 0.01, 0.04]}
                }
            
            # Import and use aggregation engine
            from .aggregation import aggregate
            
            # Perform aggregation
            aggregation_result = aggregate(model_outputs, agg_config)
            
            self._log_audit_event(
                "aggregation", 
                {"method": method, "result_keys": list(aggregation_result.keys())}, 
                "success"
            )
            
            # Store aggregation result
            self.aggregation_result = aggregation_result
            
            return aggregation_result
            
        except Exception as e:
            self._log_audit_event("aggregation", {"error": str(e)}, "error")
            raise AggregationError(f"Aggregation failed: {e}")

    def export_audit_log(
        self, format: str = "json", filepath: Optional[str] = None
    ) -> str:
        """Export audit log in specified format (json or csv)."""
        if format.lower() == "json":
            output = json.dumps(self.audit_log, indent=2)
        elif format.lower() == "csv":
            if not self.audit_log:
                output = ""
            else:
                fieldnames = self.audit_log[0].keys()
                output_buffer = StringIO()
                writer = csv.DictWriter(output_buffer, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.audit_log)
                output = output_buffer.getvalue()
                output_buffer.close()
        else:
            raise ValueError(f"Unsupported format: {format}")

        if filepath:
            with open(filepath, "w") as f:
                f.write(output)
            logging.info(f"Audit log exported to {filepath}")

        return output

    def run(self):
        """Main execution flow with comprehensive error handling and audit logging."""
        self._log_audit_event("radf_run_start", {"config_path": self.config_path})
        print("RADF run started.")

        try:
            # Load and validate configuration
            self.load_config()
            self.validate_config()

            # Execute models
            executed_models = self._execute_models()
            self._executed_models = executed_models  # Store for aggregation

            # Perform aggregation
            self._perform_aggregation()

            msg = "RADF execution completed successfully."
            self._log_audit_event("radf_run_complete", {"status": "success"})
            logging.info(msg)
            print(msg)

        except (ConfigError, ModelExecutionError, AggregationError) as e:
            msg = f"RADF execution failed: {e}"
            self._log_audit_event(
                "radf_run_complete", {"status": "error", "error": str(e)}
            )
            logging.error(msg)
            print(msg)
            raise
        except Exception as e:
            msg = f"Unexpected error during RADF execution: {e}"
            self._log_audit_event(
                "radf_run_complete", {"status": "error", "error": str(e)}
            )
            logging.error(msg, exc_info=True)
            print(msg)
            raise
        finally:
            self._log_audit_event("radf_run_end", {"total_events": len(self.audit_log)})
            logging.info("RADF run finished.")
            print("RADF run finished.")
