"""
AI Gateway Service for ESG Platform

This service provides AI/ML orchestration capabilities for the Gnanam ESG platform,
including LLM integration, model management, and automated risk analysis.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

import structlog
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import redis
from celery import Celery

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# =============================================================================
# MODELS AND TYPES
# =============================================================================

class ModelType(str, Enum):
    """Supported AI model types"""
    LLM = "llm"
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    CLUSTERING = "clustering"
    ANOMALY_DETECTION = "anomaly_detection"
    TIME_SERIES = "time_series"

class ProviderType(str, Enum):
    """AI service providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    CUSTOM = "custom"

class TaskStatus(str, Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class ModelConfig:
    """Configuration for AI models"""
    name: str
    type: ModelType
    provider: ProviderType
    version: str
    parameters: Dict[str, Any]
    cost_per_token: Optional[float] = None
    max_tokens: Optional[int] = None

@dataclass
class TaskResult:
    """Result of AI task execution"""
    task_id: str
    status: TaskStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    cost: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Pydantic models for API
class TaskRequest(BaseModel):
    """Request for AI task execution"""
    task_type: str
    model_config: ModelConfig
    input_data: Dict[str, Any]
    parameters: Optional[Dict[str, Any]] = None
    priority: int = Field(default=1, ge=1, le=10)

class TaskResponse(BaseModel):
    """Response for task creation"""
    task_id: str
    status: TaskStatus
    estimated_duration: Optional[int] = None

class TaskStatusResponse(BaseModel):
    """Response for task status check"""
    task_id: str
    status: TaskStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    progress: Optional[float] = None
    created_at: datetime
    updated_at: datetime

# =============================================================================
# AI GATEWAY SERVICE
# =============================================================================

class AIGatewayService:
    """Main AI Gateway service for orchestrating AI/ML operations"""
    
    def __init__(self):
        self.logger = structlog.get_logger(__name__)
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.celery_app = Celery('ai_gateway', broker='redis://localhost:6379/0')
        self.models: Dict[str, ModelConfig] = {}
        self.tasks: Dict[str, TaskResult] = {}
        
        # Initialize model registry
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize default model configurations"""
        self.models = {
            "gpt-4": ModelConfig(
                name="gpt-4",
                type=ModelType.LLM,
                provider=ProviderType.OPENAI,
                version="latest",
                parameters={"temperature": 0.7, "max_tokens": 1000},
                cost_per_token=0.00003,
                max_tokens=8192
            ),
            "claude-3": ModelConfig(
                name="claude-3-sonnet",
                type=ModelType.LLM,
                provider=ProviderType.ANTHROPIC,
                version="2024-02-15",
                parameters={"temperature": 0.7, "max_tokens": 1000},
                cost_per_token=0.000015,
                max_tokens=200000
            ),
            "risk-classifier": ModelConfig(
                name="risk-classifier",
                type=ModelType.CLASSIFICATION,
                provider=ProviderType.LOCAL,
                version="1.0.0",
                parameters={"threshold": 0.5}
            )
        }
        
    async def create_task(self, request: TaskRequest) -> TaskResponse:
        """Create a new AI task"""
        task_id = f"task_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{hash(str(request))}"
        
        # Store task in Redis
        task_data = {
            "task_id": task_id,
            "status": TaskStatus.PENDING,
            "request": request.dict(),
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.redis_client.hset(f"task:{task_id}", mapping=task_data)
        
        # Queue task for execution
        self.celery_app.send_task(
            "ai_gateway.execute_task",
            args=[task_id, request.dict()],
            priority=request.priority
        )
        
        self.logger.info("Task created", task_id=task_id, task_type=request.task_type)
        
        return TaskResponse(
            task_id=task_id,
            status=TaskStatus.PENDING,
            estimated_duration=60  # Default estimate
        )
    
    async def get_task_status(self, task_id: str) -> TaskStatusResponse:
        """Get the status of a task"""
        task_data = self.redis_client.hgetall(f"task:{task_id}")
        
        if not task_data:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return TaskStatusResponse(
            task_id=task_id,
            status=TaskStatus(task_data[b"status"].decode()),
            result=task_data.get(b"result", b"").decode() if task_data.get(b"result") else None,
            error=task_data.get(b"error", b"").decode() if task_data.get(b"error") else None,
            progress=float(task_data.get(b"progress", b"0").decode()),
            created_at=datetime.fromisoformat(task_data[b"created_at"].decode()),
            updated_at=datetime.fromisoformat(task_data.get(b"updated_at", task_data[b"created_at"]).decode())
        )
    
    async def execute_llm_task(self, model_config: ModelConfig, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute LLM-based task"""
        try:
            if model_config.provider == ProviderType.OPENAI:
                return await self._execute_openai_task(model_config, input_data)
            elif model_config.provider == ProviderType.ANTHROPIC:
                return await self._execute_anthropic_task(model_config, input_data)
            else:
                raise ValueError(f"Unsupported provider: {model_config.provider}")
        except Exception as e:
            self.logger.error("LLM task execution failed", error=str(e), model=model_config.name)
            raise
    
    async def _execute_openai_task(self, model_config: ModelConfig, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute OpenAI-based task"""
        # This would integrate with OpenAI API
        # For now, return mock response
        return {
            "response": f"OpenAI {model_config.name} response for: {input_data.get('prompt', '')}",
            "tokens_used": 100,
            "cost": 0.003
        }
    
    async def _execute_anthropic_task(self, model_config: ModelConfig, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Anthropic-based task"""
        # This would integrate with Anthropic API
        # For now, return mock response
        return {
            "response": f"Anthropic {model_config.name} response for: {input_data.get('prompt', '')}",
            "tokens_used": 150,
            "cost": 0.00225
        }
    
    async def execute_ml_task(self, model_config: ModelConfig, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute machine learning task"""
        try:
            if model_config.type == ModelType.CLASSIFICATION:
                return await self._execute_classification_task(model_config, input_data)
            elif model_config.type == ModelType.REGRESSION:
                return await self._execute_regression_task(model_config, input_data)
            elif model_config.type == ModelType.ANOMALY_DETECTION:
                return await self._execute_anomaly_detection_task(model_config, input_data)
            else:
                raise ValueError(f"Unsupported ML task type: {model_config.type}")
        except Exception as e:
            self.logger.error("ML task execution failed", error=str(e), model=model_config.name)
            raise
    
    async def _execute_classification_task(self, model_config: ModelConfig, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute classification task"""
        # Mock classification result
        return {
            "prediction": "high_risk",
            "confidence": 0.85,
            "probabilities": {
                "low_risk": 0.05,
                "medium_risk": 0.10,
                "high_risk": 0.85
            }
        }
    
    async def _execute_regression_task(self, model_config: ModelConfig, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute regression task"""
        # Mock regression result
        return {
            "prediction": 0.75,
            "confidence_interval": [0.70, 0.80]
        }
    
    async def _execute_anomaly_detection_task(self, model_config: ModelConfig, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute anomaly detection task"""
        # Mock anomaly detection result
        return {
            "is_anomaly": True,
            "anomaly_score": 0.92,
            "threshold": 0.8
        }
    
    async def get_model_info(self, model_name: str) -> ModelConfig:
        """Get information about a specific model"""
        if model_name not in self.models:
            raise HTTPException(status_code=404, detail="Model not found")
        return self.models[model_name]
    
    async def list_models(self) -> List[ModelConfig]:
        """List all available models"""
        return list(self.models.values())
    
    async def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return {
            "total_tasks": len(self.tasks),
            "completed_tasks": len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]),
            "failed_tasks": len([t for t in self.tasks.values() if t.status == TaskStatus.FAILED]),
            "total_cost": sum(t.cost or 0 for t in self.tasks.values()),
            "models_used": list(set(t.result.get("model", "") for t in self.tasks.values() if t.result))
        }

# =============================================================================
# FASTAPI APPLICATION
# =============================================================================

app = FastAPI(
    title="AI Gateway Service",
    description="AI/ML Orchestration Gateway for ESG Platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service
ai_service = AIGatewayService()

@app.on_event("startup")
async def startup_event():
    """Initialize service on startup"""
    logger.info("AI Gateway Service starting up")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("AI Gateway Service shutting down")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI Gateway Service is running", "version": "1.0.0"}

@app.post("/tasks", response_model=TaskResponse)
async def create_task(request: TaskRequest, background_tasks: BackgroundTasks):
    """Create a new AI task"""
    return await ai_service.create_task(request)

@app.get("/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """Get task status"""
    return await ai_service.get_task_status(task_id)

@app.get("/models")
async def list_models():
    """List all available models"""
    return await ai_service.list_models()

@app.get("/models/{model_name}")
async def get_model_info(model_name: str):
    """Get model information"""
    return await ai_service.get_model_info(model_name)

@app.get("/stats")
async def get_usage_stats():
    """Get usage statistics"""
    return await ai_service.get_usage_stats()

@app.post("/execute/llm")
async def execute_llm_task(request: TaskRequest):
    """Execute LLM task directly"""
    result = await ai_service.execute_llm_task(request.model_config, request.input_data)
    return {"result": result}

@app.post("/execute/ml")
async def execute_ml_task(request: TaskRequest):
    """Execute ML task directly"""
    result = await ai_service.execute_ml_task(request.model_config, request.input_data)
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 