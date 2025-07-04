import argparse
import logging
from .orchestrator import RADFOrchestrator


def main():
    parser = argparse.ArgumentParser(description="Run RADF scenario.")
    parser.add_argument(
        "--config", required=True, help="Path to scenario config file (YAML/JSON)"
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    try:
        orchestrator = RADFOrchestrator(config_path=args.config)
        orchestrator.run()
    except Exception as e:
        logging.error(f"RADF execution failed: {e}")


if __name__ == "__main__":
    main()
