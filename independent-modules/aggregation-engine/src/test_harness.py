"""
RADF Test Harness

Provides utilities for running sample scenarios, validating results, and generating test reports.
Supports automated testing and validation of the RADF system.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from .orchestrator import RADFOrchestrator, RADFError


class RADFTestHarness:
    def __init__(self, test_data_dir: str = "test_data"):
        self.test_data_dir = test_data_dir
        self.results = []
        self._setup_logging()

    def _setup_logging(self):
        """Set up logging for test harness."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    def run_scenario(self, config_path: str, user: str = "test_user") -> Dict[str, Any]:
        """Run a single scenario and return results."""
        try:
            logging.info(f"Running scenario: {config_path}")
            orchestrator = RADFOrchestrator(config_path, user)
            orchestrator.run()

            result = {
                "config_path": config_path,
                "user": user,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "success",
                "audit_log": orchestrator.audit_log,
                "error": None,
            }

            logging.info(f"Scenario completed successfully: {config_path}")
            return result

        except RADFError as e:
            logging.error(f"RADF error in scenario {config_path}: {e}")
            result = {
                "config_path": config_path,
                "user": user,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "radf_error",
                "audit_log": [],
                "error": str(e),
            }
            return result
        except Exception as e:
            logging.error(f"Unexpected error in scenario {config_path}: {e}")
            result = {
                "config_path": config_path,
                "user": user,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "unexpected_error",
                "audit_log": [],
                "error": str(e),
            }
            return result

    def run_scenarios(
        self, config_paths: List[str], user: str = "test_user"
    ) -> List[Dict[str, Any]]:
        """Run multiple scenarios and return results."""
        results = []
        for config_path in config_paths:
            result = self.run_scenario(config_path, user)
            results.append(result)
        return results

    def run_all_scenarios_in_directory(
        self, directory: str, user: str = "test_user"
    ) -> List[Dict[str, Any]]:
        """Run all scenario config files in a directory."""
        config_paths = []
        for filename in os.listdir(directory):
            if filename.endswith((".yaml", ".yml", ".json")):
                config_paths.append(os.path.join(directory, filename))

        logging.info(f"Found {len(config_paths)} scenario configs in {directory}")
        return self.run_scenarios(config_paths, user)

    def validate_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate test results and generate summary."""
        total_scenarios = len(results)
        successful_scenarios = sum(1 for r in results if r["status"] == "success")
        failed_scenarios = total_scenarios - successful_scenarios

        validation_summary = {
            "total_scenarios": total_scenarios,
            "successful_scenarios": successful_scenarios,
            "failed_scenarios": failed_scenarios,
            "success_rate": (
                successful_scenarios / total_scenarios if total_scenarios > 0 else 0
            ),
            "timestamp": datetime.utcnow().isoformat(),
            "details": results,
        }

        logging.info(
            f"Validation complete: {successful_scenarios}/{total_scenarios} scenarios passed"
        )
        return validation_summary

    def generate_test_report(
        self, results: List[Dict[str, Any]], output_path: Optional[str] = None
    ) -> str:
        """Generate a comprehensive test report."""
        validation_summary = self.validate_results(results)

        report = {
            "test_report": {
                "title": "RADF Test Report",
                "generated_at": datetime.utcnow().isoformat(),
                "summary": validation_summary,
                "scenarios": results,
            }
        }

        report_json = json.dumps(report, indent=2)

        if output_path:
            with open(output_path, "w") as f:
                f.write(report_json)
            logging.info(f"Test report saved to: {output_path}")

        return report_json

    def export_audit_logs(
        self, results: List[Dict[str, Any]], output_dir: str = "audit_logs"
    ):
        """Export audit logs from all scenarios."""
        os.makedirs(output_dir, exist_ok=True)

        for i, result in enumerate(results):
            if result["audit_log"]:
                timestamp = result["timestamp"].replace(":", "-")
                filename = f"audit_log_{i}_{timestamp}.json"
                filepath = os.path.join(output_dir, filename)

                with open(filepath, "w") as f:
                    json.dump(result["audit_log"], f, indent=2)

                logging.info(f"Audit log exported: {filepath}")


def run_sample_scenarios():
    """Run sample scenarios for testing and demonstration."""
    harness = RADFTestHarness()

    # Run sample scenarios
    sample_configs = [
        "RiskModels/src/RADF/sample_scenario_valid.yaml",
        "RiskModels/src/RADF/sample_scenario_invalid.yaml",
    ]

    results = harness.run_scenarios(sample_configs, "demo_user")

    # Generate report
    harness.generate_test_report(results, "test_report.json")

    # Export audit logs
    harness.export_audit_logs(results)

    print(
        "Sample scenarios completed. Check test_report.json and audit_logs/ directory."
    )
    return results


if __name__ == "__main__":
    run_sample_scenarios()
