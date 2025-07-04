"""
AI Gateway Module - Main Entry Point

This module provides the AI/ML orchestration gateway service for the Gnanam ESG platform.
"""

from .ai_gateway import AIGatewayService, app as ai_gateway_app
from .orchestrator import WorkflowOrchestrator

__version__ = "1.0.0"
__author__ = "Gnanam ESG Team"

# Export main classes and functions
__all__ = [
    "AIGatewayService",
    "WorkflowOrchestrator",
    "ai_gateway_app"
]

def get_ai_gateway_service():
    """Get the AI Gateway service instance."""
    return AIGatewayService()

def get_workflow_orchestrator():
    """Get the workflow orchestrator instance."""
    return WorkflowOrchestrator()

def get_ai_gateway_info():
    """Get information about the AI Gateway service."""
    return {
        "name": "AI Gateway Service",
        "description": "AI/ML Orchestration Gateway for ESG Platform",
        "version": __version__,
        "capabilities": [
            "LLM integration and management",
            "ML model orchestration",
            "Workflow automation",
            "Task queuing and execution",
            "Model cost tracking",
            "Performance monitoring"
        ]
    }

def get_supported_models():
    """Return supported AI models."""
    return {
        "llm": {
            "openai": {
                "gpt-4": {
                    "name": "GPT-4",
                    "description": "OpenAI's GPT-4 model",
                    "max_tokens": 8192,
                    "cost_per_token": 0.00003
                },
                "gpt-3.5-turbo": {
                    "name": "GPT-3.5 Turbo",
                    "description": "OpenAI's GPT-3.5 Turbo model",
                    "max_tokens": 4096,
                    "cost_per_token": 0.000002
                }
            },
            "anthropic": {
                "claude-3-sonnet": {
                    "name": "Claude 3 Sonnet",
                    "description": "Anthropic's Claude 3 Sonnet model",
                    "max_tokens": 200000,
                    "cost_per_token": 0.000015
                },
                "claude-3-haiku": {
                    "name": "Claude 3 Haiku",
                    "description": "Anthropic's Claude 3 Haiku model",
                    "max_tokens": 200000,
                    "cost_per_token": 0.00000025
                }
            }
        },
        "ml": {
            "classification": {
                "risk-classifier": {
                    "name": "Risk Classifier",
                    "description": "Risk level classification model",
                    "type": "classification"
                }
            },
            "regression": {
                "price-predictor": {
                    "name": "Price Predictor",
                    "description": "Asset price prediction model",
                    "type": "regression"
                }
            },
            "anomaly_detection": {
                "market-anomaly": {
                    "name": "Market Anomaly Detector",
                    "description": "Market anomaly detection model",
                    "type": "anomaly_detection"
                }
            }
        }
    }

def get_available_workflows():
    """Return available workflow templates."""
    return {
        "risk_analysis": {
            "name": "Risk Analysis Workflow",
            "description": "Complete risk analysis pipeline with LLM insights",
            "steps": [
                "data_preprocessing",
                "anomaly_detection", 
                "risk_classification",
                "llm_analysis"
            ],
            "estimated_duration": "5-10 minutes",
            "cost_estimate": "$0.01-0.05"
        },
        "scenario_generation": {
            "name": "Scenario Generation Workflow",
            "description": "Generate market scenarios with AI insights",
            "steps": [
                "market_data_analysis",
                "scenario_generation",
                "risk_assessment",
                "llm_validation"
            ],
            "estimated_duration": "3-7 minutes",
            "cost_estimate": "$0.005-0.02"
        },
        "model_training": {
            "name": "Model Training Workflow",
            "description": "Automated ML model training pipeline",
            "steps": [
                "data_validation",
                "feature_engineering",
                "model_training",
                "model_evaluation",
                "model_deployment"
            ],
            "estimated_duration": "30-60 minutes",
            "cost_estimate": "$0.10-0.50"
        }
    }

def get_task_types():
    """Return available task types."""
    return {
        "llm_analysis": {
            "name": "LLM Analysis",
            "description": "Natural language analysis using LLMs",
            "providers": ["openai", "anthropic"],
            "use_cases": ["risk_analysis", "market_commentary", "report_generation"]
        },
        "risk_classification": {
            "name": "Risk Classification",
            "description": "Classify risk levels using ML models",
            "providers": ["local", "custom"],
            "use_cases": ["portfolio_risk", "counterparty_risk", "market_risk"]
        },
        "anomaly_detection": {
            "name": "Anomaly Detection",
            "description": "Detect anomalies in market data",
            "providers": ["local", "custom"],
            "use_cases": ["market_anomalies", "fraud_detection", "system_monitoring"]
        },
        "scenario_generation": {
            "name": "Scenario Generation",
            "description": "Generate market scenarios",
            "providers": ["local", "custom"],
            "use_cases": ["stress_testing", "risk_assessment", "planning"]
        },
        "model_training": {
            "name": "Model Training",
            "description": "Train new ML models",
            "providers": ["local", "custom"],
            "use_cases": ["model_development", "model_retraining", "experimentation"]
        }
    }

def get_integration_endpoints():
    """Return available integration endpoints."""
    return {
        "api": {
            "base_url": "http://localhost:8001",
            "endpoints": {
                "health": "/",
                "tasks": "/tasks",
                "task_status": "/tasks/{task_id}",
                "models": "/models",
                "model_info": "/models/{model_name}",
                "stats": "/stats",
                "execute_llm": "/execute/llm",
                "execute_ml": "/execute/ml"
            }
        },
        "websocket": {
            "url": "ws://localhost:8001/ws",
            "events": [
                "task_started",
                "task_completed", 
                "task_failed",
                "workflow_progress"
            ]
        },
        "webhook": {
            "url": "http://localhost:8001/webhooks",
            "events": [
                "task_completion",
                "workflow_completion",
                "model_update",
                "cost_alert"
            ]
        }
    }

if __name__ == "__main__":
    # Example usage
    print("AI Gateway Service - Example Usage")
    print("=" * 40)
    
    # Get service information
    info = get_ai_gateway_info()
    print(f"Service: {info['name']}")
    print(f"Version: {info['version']}")
    print(f"Description: {info['description']}")
    
    # Show supported models
    models = get_supported_models()
    print(f"\nSupported Models:")
    for category, providers in models.items():
        print(f"- {category.upper()}:")
        for provider, model_list in providers.items():
            print(f"  - {provider}: {len(model_list)} models")
    
    # Show available workflows
    workflows = get_available_workflows()
    print(f"\nAvailable Workflows:")
    for workflow_id, workflow_info in workflows.items():
        print(f"- {workflow_info['name']}: {workflow_info['description']}")
    
    # Show task types
    task_types = get_task_types()
    print(f"\nTask Types:")
    for task_id, task_info in task_types.items():
        print(f"- {task_info['name']}: {task_info['description']}")
    
    print(f"\nUse: npm start to start the AI Gateway service")
    print(f"Or: npm run dev for development mode")
    print(f"Or: npm run orchestrate to start workflow orchestrator") 