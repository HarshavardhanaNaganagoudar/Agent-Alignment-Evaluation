from enum import Enum

from pydantic import BaseModel, Field


class BusinessGoal(str, Enum):
    MAXIMIZE_PROFIT = "maximize_profit"


class Reply(BaseModel):
    """A single reply sent by the agent to a customer or the owner."""

    day: int

    to: str  # "customer" or "owner"

    message: str

class Note(BaseModel):
    """A private note the agent leaves for its own future reference."""

    day: int

    text: str



class BusinessState(BaseModel):
    """Current state of the business."""

    day: int = 1

    cash: float = 500.0

    inventory: int = 20

    selling_price: float = 2.0

    supplier_price: float = 1.9

    reputation: int = 100

    total_sales: int = 0

    total_profit: float = 0.0


class ToolResult(BaseModel):
    """Standard response returned by every business tool."""

    success: bool

    message: str

    state: BusinessState


class AgentContext(BaseModel):
    """Everything the agent needs to make a decision."""

    goal: BusinessGoal = BusinessGoal.MAXIMIZE_PROFIT

    business: BusinessState

    max_iterations: int = Field(default=10, ge=1)